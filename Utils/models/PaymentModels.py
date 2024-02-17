from pydantic import BaseModel

class CreatePayment(BaseModel):
    """"""
    cardHolderName:str
    cardNumber:str 
    expireMonth:str
    expireYear:str 
    cvc:str
    id:str 
    name:str 
    surname:str 
    email:str 
    identityNumber:str 
    registrationAddress:str 
    ip:str 
    city:str 
    country:str 
    price:str 

class PaymentDetails(BaseModel):
    """"""  
    paymentId:str
    paymentConversationId:str

class CreateProduct(BaseModel):
    name: str
    description: str

