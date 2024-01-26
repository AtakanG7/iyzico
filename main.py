from typing import Union
from fastapi import FastAPI
from Utils.iyzico import IyzicoPayHandler
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
iyzico_handler = IyzicoPayHandler()
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

