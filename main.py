import random
import time
import logging
from fastapi import FastAPI, HTTPException

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
