from typing import Union
from fastapi import FastAPI
from Utils.iyzico import IyzicoPayHandler
from fastapi.middleware.cors import CORSMiddleware
from Utils.models.PaymentModels import CreatePayment, CreateProduct, PaymentDetails
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


@app.post("/user/payment")
async def create_payment(payment: CreatePayment):
    print("payment")
    print(payment)
    response = await iyzico_handler.create_payment(
        cardHolderName=payment.cardHolderName,
        cardNumber=payment.cardNumber,
        expireMonth=payment.expireMonth,
        expireYear=payment.expireYear,
        cvc=payment.cvc,
        id=payment.id,
        name=payment.name,
        surname=payment.surname,
        email=payment.email,
        identityNumber=payment.identityNumber,
        registrationAddress=payment.registrationAddress,
        ip=payment.ip,
        city=payment.city,
        country=payment.country,
        price=payment.price
    )
    print("response")
    print(response)
    return response

@app.post("/user/payment/details")
async def get_payment_details(payment: PaymentDetails):
    print("paymentId")
    print(payment)
    response = await iyzico_handler.get_payment_details(
        paymentId=payment.paymentId,
        paymentConversationId=payment.paymentConversationId
    )
    print("response")
    print(response)
    return response


@app.get("/user/payments/initialize-check-out-form")
async def create_payment():
    response = await iyzico_handler.initiazlizeCheckOutForm()
    return response
    
@app.get("/user/payments/retrieve-check-out-form")
async def create_payment(token):
    return await iyzico_handler.retrieveCheckOutForm(token=token)


@app.post("/user/subscription/product/create")
async def create_product(data: CreateProduct):
    return await iyzico_handler.create_sub_product(data.name, data.description)
