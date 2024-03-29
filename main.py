from fastapi import FastAPI, HTTPException
import json
import uvicorn
from typing import Optional
from pathlib import Path

from src.lambda_function import lambda_handler

app = FastAPI()


@app.get("/invoke")
async def invoke():
    try:
        response = lambda_handler({}, None)
        return json.loads(response['body'])
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing request without event: {str(e)}")


@app.get("/invoke/{event_name}")
async def invoke_with_event(event_name: str):
    file_path = Path(f"./events/{event_name}.json")
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Event not found")

    try:
        with open(file_path, "r") as file:
            event = json.load(file)
        response = lambda_handler(event, None)
        return json.loads(response['body'])
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Event not found or error processing the event: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
