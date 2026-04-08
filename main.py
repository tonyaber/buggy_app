import random
import time
import logging
from fastapi import FastAPI, HTTPException
import re
# logging to file

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


app = FastAPI()

@app.get("/")
def home():
    logging.info("GET / called")
    return {"status": "ok"}

@app.get("/sometimes-fails")
def sometimes_fails():
    dice = random.random()

    if dice < 0.3:
        logging.error("Database connection failed")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    if dice < 0.5:
        logging.warning("Slow response detected")
        time.sleep(3)

    return {"result": "success"}

@app.get("/auth")
def auth():
    logging.warning("Unauthorized access attempt")
    raise HTTPException(status_code=401, detail="Unauthorized")

LOG_PATTERN = re.compile(
    r'(?P<timestamp>\d{4}-\d{2}-\d{2} '
    r'\d{2}:\d{2}:\d{2},\d{3}) '
    r'(?P<level>INFO|WARNING|ERROR) '
    r'(?P<message>.+)'
)

@app.get("/internal/logs")
def get_logs(limit: int = 100):
    result = []

    with open("logs/app.log") as f:
        for line in f.readlines()[-limit:]:
            match = LOG_PATTERN.match(line)
            if not match:
                continue

            data = match.groupdict()
            data["status"] = {
                "ERROR": 500,
                "WARNING": 400,
                "INFO": 200
            }.get(data["level"], 200)

            result.append(data)

    return result