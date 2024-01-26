import iyzipay
import json
import os

# Assuming 'config.json' is in the same directory as your script
config_path = os.path.join(os.path.dirname(__file__), 'config.json')

try:
    with open(config_path, 'r') as file:
        CONFIG = json.load(file)
except FileNotFoundError:
    print("Error: 'config.json' not found. Make sure the file exists in the correct location.")


class IyzicoPayHandler():
    """
        A class for interfacing with Iyzipay payment service. It offers various functionalities 
        to facilitate payment operations such as creating subscriptions, sending invoices, 
        and handling credentials and configurations.

        Methods:
        save_card: Saves card
    """

    async def __init__(self) -> None:
        self.options = CONFIG['options']

    async def create_card_and_user(self, cardAlias, cardHolderName, cardNumber, expireMonth, expireYear, email):
        """
            Saves the card information and creates a user that can be found later as cardUserKey.

            Arguments: 
                - cardAlias : Name of the card
                - cardHolderName :  Name that is on the card
                - cardNumber : Number of the card
                - expireMonth : Last month of the card
                - expireYear : Last year of the card
                - email : Email of the user
        """
        card_information = {
            'cardAlias': cardAlias,
            'cardHolderName': cardHolderName,
            'cardNumber': cardNumber,
            'expireMonth': expireMonth,
            'expireYear': expireYear,
            'email' : email
        }

        request = {
            'locale': 'tr',
            'card': card_information
        }

        card = iyzipay.Card().create(request, self.options)

        print(card.read().decode('utf-8'))

    async def delete_card(self, cardToken, cardUserKey):
        """
            Removes the spesific card from users iyzipay history

            Arguments:
                - cardToken : Identifier to the card
                - cardUserKey : Idenrifier to the user
        """
        request = {
            'locale': 'tr',
            'cardToken': cardToken,
            'cardUserKey': cardUserKey
        }

        card = iyzipay.Card().delete(request, self.options)

        return card.read().decode('utf-8')

    async def retrieve_cards(self, cardUserKey):
        """
            Retrieves all the cards that are belong to a spesific user

            Arguments: 
                - cardUserKey : Identifier to a unique user
        """
        request = {
            'locale': 'tr',
            'cardUserKey': cardUserKey
        }

        card_list = iyzipay.CardList().retrieve(request, self.options)

        return card_list.read().decode('utf-8')
    
    async def create_payment(self, cardHolderName= None, cardNumber= None, expireMonth= None, expireYear= None, cvc= None, registerCard= None):

        payment_card = {
            'cardHolderName': 'John Doe',
            'cardNumber': '5528790000000008',
            'expireMonth': '12',
            'expireYear': '2030',
            'cvc': '123',
            'registerCard': '0'
        }

        buyer = {
            'id': 'BY789',
            'name': 'John',
            'surname': 'Doe',
            'gsmNumber': '+905350000000',
            'email': 'email@email.com',
            'identityNumber': '74300864791',
            'lastLoginDate': '2015-10-05 12:43:35',
            'registrationDate': '2013-04-21 15:12:09',
            'registrationAddress': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
            'ip': '85.34.78.112',
            'city': 'Istanbul',
            'country': 'Turkey',
            'zipCode': '34732'
        }

        address = {
            'contactName': 'Jane Doe',
            'city': 'Istanbul',
            'country': 'Turkey',
            'address': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
            'zipCode': '34732'
        }

        basket_items = [
            {
                'id': 'BI101',
                'name': 'Binocular',
                'category1': 'Collectibles',
                'itemType': 'PHYSICAL',
                'price': '1'
            }
        ]

        request = {
            'locale': 'tr',
            'price': '1',
            'paidPrice': '1.2',
            'currency': 'TRY',
            'installment': '1',
            'basketId': 'B67832',
            'paymentChannel': 'WEB',
            'paymentGroup': 'PRODUCT',
            'paymentCard': payment_card,
            'buyer': buyer,
            'shippingAddress': address,
            'billingAddress': address,
            'basketItems': basket_items
        }

        payment = iyzipay.Payment().create(request, self.options)

        return payment

    async def create_sub_product(self, name, description):
        """ 
            - Creates a product in iyzipay. This is needed to create plans for your business.
            
            Arguments: 
                - name : Name of the product
                - descriptipn : Description of the product
            
            Return:
                {
                    "status": "success",
                    "systemTime": 1686785492734,
                    "data": {
                        "referenceCode": "ac3afdd2-69af-4ca6-a284-46bf8540a954", # This field is needed if product details will be updated, deleted
                        "createdDate": 1686785492730,
                        "name": "Product Name",
                        "description": "Product Description",
                        "status": "ACTIVE",
                        "pricingPlans": []
                    }
                } 
        """

        request = {
            "locale": "tr",
            "name": name,
            "description": description
        }

        report = iyzipay.IyziLinkProduct().create(request, self.options)
        return report.read().decode('utf-8')
    
    async def create_sub_plan(self, productReferenceCode, name, price, currencyCode, paymentInterval, paymentIntervalCount, planpaymentType= "RECURRING"):
        """ 
            - Creates a plan in iyzipay. This is needed to create payment process for your business.
            Arguments: 
                - name : Name of the plan which should be descriptive
                - productReferenceCode : The product reference code which will be attached to the plan
                - price : Price of the plan
                - currencyCode : Currency in which payment will be received. It can be TL, USD, EUR. Make sure that currencies other than TL are defined in your account.
                - paymentInterval : Determines the period in which recurring payments will be received. It can take the values DAILY, WEEKLY, MONTHLY, YEARLY.
                - paymentIntervalCount : It determines the frequency of the payment period. For example, if the paymentInterval value is WEEKLY and the paymentIntervalCount value is 2, payments will be received every 2 weeks.
                - planpaymentType : Specifies the subscription type. RECURRING value must be entered.
            Return:
                {
                    "status": "success",... TODO ne geldiği güncellenmesi
                } 
        """

        request = {
            "locale": "tr",
            "productReferenceCode": productReferenceCode,
            "name": name,
            "price": price,
            "currencyCode": currencyCode,
            "paymentInterval": paymentInterval,
            "paymentIntervalCount": paymentIntervalCount,
            "planpaymentType": planpaymentType
        }

        report = iyzipay.IyziLinkProduct().create(request, self.options)
        return report.read().decode('utf-8')

    async def create_subscription(
            self,
            callbackUrl,
            pricingPlanReferenceCode,
            name,
            surname,
            email,
            gsmNumber,
            identityNumber,
            address,
            zipCode,
            city,
            country,
            contactName
            ):
        """TODO"""
        billingAdress = {
            "address": address,
            "zipCode": zipCode,
            "city": city,
            "country": country,
            "contactName": contactName,
        }

        shippingAddress = {
            "address": address,
            "zipCode": zipCode,
            "city": city,
            "country": country,
            "contactName": contactName,
        }

        request = {
            "locale": "tr",
            "callbackUrl": callbackUrl,
            "pricingPlanReferenceCode": pricingPlanReferenceCode,
            "name": name,
            "surname": surname,
            "email": email,
            "gsmNumber": gsmNumber, 
            "identityNumber": identityNumber,
            "billingAdress": billingAdress,
            "shippingAddress": shippingAddress
            
        }

        report = iyzipay.IyziLinkProduct().create(request, self.options)
        return report.read().decode('utf-8')
    
    async def activate_subscription(self, subscriptionReferenceCode):
        """
            Activates the created subscription

            Arguments:
                - subscriptionReferenceCode : Referance code to a subscription
        """
        request = { 
            "subscriptionReferenceCode": subscriptionReferenceCode
        }

        return None
    
    async def deactivate_subscription(self, subscriptionReferenceCode):
        """
            Deactivates the activated subscription

            Arguments:
                - subscriptionReferenceCode : Referance code to a subscription
        """
        request = { 
            "subscriptionReferenceCode": subscriptionReferenceCode
        }
        
    async def update_subscription_card(self, subscriptionReferenceCode, callBackUrl):
        """
            Deactivates the activated subscription

            Arguments:
                - subscriptionReferenceCode : Referance code to a subscription
                - callBackUrl : This is where the response will be returned
        """
        request = { 
            "subscriptionReferenceCode": subscriptionReferenceCode,
            "callBackUrl": callBackUrl
        }

    async def get_subscription_info(self, subscriptionReferenceCode):
        """
            Fetches the data of the subscriber

            Arguments:
                - subscriptionReferenceCode : Referance code to a subscription
        """
        request = { 
            "subscriptionReferenceCode": subscriptionReferenceCode,
        }