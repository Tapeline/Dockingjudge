"""Main application file"""

import asyncio
import json
import logging

import aio_pika
from aio_pika import Message
from aio_pika.abc import (AbstractIncomingMessage, AbstractRobustChannel,
                          AbstractRobustExchange, DeliveryMode)

from judgeservice import handle, settings
from judgeservice.configuration import Configuration
from judgeservice.exceptions import (JudgeletNotFoundException,
                                     RequestProcessingException)
from judgeservice.judgelet import JudgeletGroup


def _encode_message(message: dict) -> bytes:
    """Encode json message with appropriate encoding"""
    json_str = json.dumps(message)
    return json_str.encode(settings.IO_ENCODING)


def _decode_message(message: bytes) -> dict:
    """Decode json message with appropriate encoding"""
    json_str = message.decode(settings.IO_ENCODING)
    return json.loads(json_str)


def _validate_message(message: dict):
    """Perform incoming message validation"""
    if "id" not in message:
        raise RequestProcessingException("Id not in message")


class ServerApplication:
    """Application class"""
    def __init__(
            self,
            logging_level=logging.DEBUG,
            config_path: str = settings.CONFIG_PATH
    ):
        self._in_exchange = None
        self._out_exchange: AbstractRobustExchange | None = None
        self._in_queue = None
        self._channel: AbstractRobustChannel | None = None
        self._connection = None
        self._logging_level = logging_level
        config = Configuration(config_path)
        self._groups = config.load_config()

    async def connect(self) -> None:
        """Connect to RMQ and set up queues"""
        logging.info("Connecting to %s:5672...", settings.RMQ_ADDRESS)
        self._connection = await aio_pika.connect_robust(
            host=settings.RMQ_ADDRESS,
            port=5672,
            login=settings.RMQ_USER,
            password=settings.RMQ_PASSWORD
        )
        logging.info("Connected")
        self._channel = await self._connection.channel()
        logging.info("Channel received")
        self._in_exchange = await self._channel.declare_exchange(
            "solutions_exchange",
            durable=True
        )
        self._out_exchange = await self._channel.declare_exchange(
            "judge_answers_exchange",
            aio_pika.ExchangeType.DIRECT,
            durable=True
        )
        logging.info("Exchanges set up")
        self._in_queue = await self._channel.declare_queue(
            "solutions_to_check",
            durable=True
        )
        await self._in_queue.bind(
            self._in_exchange,
            routing_key="solution_to_check"
        )
        logging.info("Queue set up")

    def _get_group(self, compiler: str) -> JudgeletGroup | None:
        """Get group by compiler selector"""
        for group in self._groups:
            if group.selector.is_applicable(compiler):
                return group
        return None

    async def answer_error(self, request_data: dict, error_code: str, error: str) -> None:
        """Send error as answer to RMQ"""
        await self._out_exchange.publish(
            Message(_encode_message({
                "answer_to": request_data.get("id"),
                "is_successful": False,
                "details": error,
                "code": error_code
            }), delivery_mode=DeliveryMode.PERSISTENT),
            routing_key="solution_answer"
        )

    async def answer_success(self, request_data: dict, response_data: dict) -> None:
        """Send successful answer to RMQ"""
        await self._out_exchange.publish(
            Message(_encode_message({
                "answer_to": request_data.get("id"),
                "is_successful": True,
                "contents": response_data
            }), delivery_mode=DeliveryMode.PERSISTENT),
            routing_key="solution_answer"
        )

    async def handle_request(self, request_data: dict) -> None:
        """Main handling request function"""
        handle.validate_request(request_data)
        group = self._get_group(request_data["compiler"])
        if group is None:
            logging.warning("Unknown compiler label %s. Aborting",
                            request_data["compiler"])
            raise JudgeletNotFoundException(request_data["compiler"])
        judgelet = group.get_judgelet()
        if judgelet is None:
            logging.warning("No active judgelet for label %s. Aborting",
                            request_data["compiler"])
            raise JudgeletNotFoundException(request_data["compiler"])
        judgelet.notify_opened_connection()
        try:
            logging.info("Directing request %s to %s", request_data['id'], judgelet.address)
            response = await handle.handle_request(request_data, judgelet.address)
            judgelet.notify_closed_connection()
            await self.answer_success(request_data, response)
            return
        except RequestProcessingException as e:
            judgelet.notify_closed_connection()
            raise e

    async def handle_request_and_errors(self, request_data: dict) -> None:
        """Handle request and handle any errors that might occur during execution"""
        try:
            await self.handle_request(request_data)
        except RequestProcessingException as e:
            await self.answer_error(request_data, e.CODE, str(e))

    async def on_message(self, message: AbstractIncomingMessage) -> None:
        """Handle incoming message"""
        contents = _decode_message(message.body)
        try:
            _validate_message(contents)
        except RequestProcessingException as e:
            logging.exception("%s", e)
            return
        logging.info("Received request #%s", contents['id'])
        await self.handle_request_and_errors(contents)
        logging.info("Handled request #%s", contents['id'])

    async def run(self) -> None:
        """Run server application"""
        logging.info("Setting up...")
        await self.connect()
        logging.info("Setup complete")
        await self._in_queue.consume(self.on_message, no_ack=True)
        logging.info(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()
