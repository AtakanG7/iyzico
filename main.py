from typing import Union
from fastapi import FastAPI
from Utils.iyzico import IyzicoPayHandler
from fastapi.middleware.cors import CORSMiddleware
import json
iyzico_handler = IyzicoPayHandler()

app = FastAPI()
# Allow all origins in this example (replace '*' with your specific allowed origins)
origins = ["*"]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("")
def read_root():
    return {"Hello": "World"}


@app.get("/user/payment")
async def create_payment():
    return await iyzico_handler.create_payment(
        cardHolderName="Atakan",
        cardNumber="5890040000000016",
        expireMonth="2",
        expireYear="2026",
        registerCard=0,
        cvc=123
    )


@app.get("/user/payments/initialize-check-out-form")
async def create_payment():
    response = await iyzico_handler.initiazlizeCheckOutForm()
    jsonResponse = json.loads(response)
    return jsonResponse
    
@app.get("/user/payments/retrieve-check-out-form")
async def create_payment(token):
    return await iyzico_handler.retrieveCheckOutForm(token=token)
