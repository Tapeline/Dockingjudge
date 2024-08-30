import json

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost', credentials=pika.PlainCredentials(
        username="rm_user", password="rm_password"
    )))
channel = connection.channel()

channel.exchange_declare(
    exchange='solutions_exchange',
    exchange_type='direct'
)
channel.exchange_declare(exchange='judge_answers_exchange', durable=True)

result = channel.queue_declare(queue='receive')
channel.queue_bind(exchange='judge_answers_exchange', queue='receive', routing_key='solution_answer')

message = {
    "id": "abc123",
    "code": {
        "type": "string",
        "code": "try:\n    print(int(input()) ** 2)\nexcept ValueError:\n    print('err')"
    },
    "compiler": "python",
    "suite": {
        "precompile": [
            {
                "type": "no_import"
            }
        ],
        "groups": [
            {
                "name": "A",
                "depends_on": [],
                "points": 20,
                "scoring_rule": "polar",
                "cases": [
                    {
                        "validators": [
                            {
                                "type": "stdout",
                                "args": {"expected": "9"}
                            }
                        ],
                        "stdin": "3\n",
                        "files_in": {},
                        "files_out": [],
                        "time_limit": 2,
                        "mem_limit_mb": 0
                    }
                ]
            },
            {
                "name": "B",
                "depends_on": ["A"],
                "points": 30,
                "scoring_rule": "polar",
                "cases": [
                    {
                        "validators": [
                            {
                                "type": "stdout",
                                "args": {"expected": "err"}
                            }
                        ],
                        "stdin": "a\n",
                        "files_in": {},
                        "files_out": [],
                        "time_limit": 2,
                        "mem_limit_mb": 0
                    }
                ]
            }
        ]
    }
}
message_str = json.dumps(message)
channel.basic_publish(exchange='solutions_exchange',
                      routing_key='solution_to_check',
                      body=message_str.encode("utf-8"))

print(' [*] Waiting for answer. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f" [x] {body.decode('utf-8')}")
    exit(0)


channel.basic_consume(
    queue='receive', on_message_callback=callback, auto_ack=True)

channel.start_consuming()
