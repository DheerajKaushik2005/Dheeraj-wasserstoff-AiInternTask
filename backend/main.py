from fastapi import FastAPI, Request  # Make sure Request is imported
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/ask")
async def ask_question(request: Request):
    # your code logic here
    return {"answer": "Sample answer"}



