import uvicorn
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from judgelet.application import JudgeletApplication
from judgelet.models import RunRequest, RunAnswer

app = FastAPI()
judgelet = JudgeletApplication()


@app.post("/run-suite")
async def run_suite(request: RunRequest) -> RunAnswer:
    return await judgelet.execute_request_and_handle_errors(request)


@app.get("/ping", response_class=PlainTextResponse)
async def ping():
    return "ok"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
