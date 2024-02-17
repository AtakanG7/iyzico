import streamlit as st
import requests
import json

# Define function to display page content
def simple_payment():
    st.subheader("Simple Payment")
    # Dummy data
    dummy_data = {
        "cardHolderName": "John Doe",
        "cardNumber": "4123111111111117",
        "expireMonth": "12",
        "expireYear": "25",
        "cvc": "123",
        "id": "1", 
        "name": "John",
        "surname": "Doe",
        "email": "john.doe@example.com",
        "identityNumber": "74300864791",
        "registrationAddress": "123 Main Street",
        "ip": "192.168.1.1",
        "city": "New York",
        "country": "USA",
        "price": "10000"
    }

    if 'useDummy' not in st.session_state:
        st.session_state.useDummy = False

    if st.sidebar.button("Fill dummy"):
        st.session_state['useDummy'] = True
    card_holder_name = st.text_input("Card Holder Name", value=dummy_data['cardHolderName'] if st.session_state['useDummy'] else None)
    card_number = st.text_input("Card Number", value=dummy_data['cardNumber'] if st.session_state['useDummy'] else 5168880000000002)
    expire_month = st.number_input("Expire Month", min_value=1, max_value=12, value=int(dummy_data['expireMonth']) if st.session_state['useDummy'] else 1)
    expire_year = st.number_input("Expire Year", min_value=24, max_value=99, value=int(dummy_data['expireYear']) if st.session_state['useDummy'] else 24)
    cvc = st.text_input("CVC", value=dummy_data['cvc'] if st.session_state['useDummy'] else 555)
    id = st.text_input("ID", value=dummy_data['id'] if st.session_state['useDummy'] else 1)
    name = st.text_input("Name", value=dummy_data['name'] if st.session_state['useDummy'] else "None")
    surname = st.text_input("Surname", value=dummy_data['surname'] if st.session_state['useDummy'] else "None")
    email = st.text_input("Email", value=dummy_data['email'] if st.session_state['useDummy'] else "None")
    identity_number = st.text_input("Identity Number", value=dummy_data['identityNumber'] if st.session_state['useDummy'] else 74300864791)
    registration_address = st.text_input("Registration Address", value=dummy_data['registrationAddress'] if st.session_state['useDummy'] else "None")
    ip = st.text_input("IP", value=dummy_data['ip'] if st.session_state['useDummy'] else "None")
    city = st.text_input("City", value=dummy_data['city'] if st.session_state['useDummy'] else "None")
    country = st.text_input("Country", value=dummy_data['country'] if st.session_state['useDummy'] else "None")
    price = st.text_input("Price", value=dummy_data['price'] if st.session_state['useDummy'] else 0)

    # Perform checks if needed
    # For example, you can check if the card number is numeric and has a valid length
    if not card_number.isdigit() or len(card_number) != 16:
        st.error("Invalid card number. Please enter a 16-digit numeric value.")
    elif not 0 < expire_month <= 12:
        st.error("Invalid expiry month. Please enter a value between 1 and 12.")
    elif not 24 <= expire_year <= 99:
        st.error("Invalid expiry year. Please enter a value between 24 and 99.")
    elif not cvc.isdigit() or len(cvc) != 3:
        st.error("Invalid CVC. Please enter a 3-digit numeric value.")
    elif not id.isdigit():
        st.error("Invalid ID. Please enter a numeric value.")
    elif not identity_number.isdigit() or len(identity_number) < 5:
        st.error("Invalid identity number. Please enter at least 5 digits.")
    else:
        # All fields are valid, make the API request
        payload = {
            "cardHolderName": str(card_holder_name),
            "cardNumber": str(card_number),
            "expireMonth": str(expire_month),
            "expireYear": str(expire_year),
            "cvc": str(cvc),
            "id": str(id),
            "name": str(name),
            "surname": str(surname),
            "email": str(email),
            "identityNumber": str(identity_number),
            "registrationAddress": str(registration_address),
            "ip": str(ip),
            "city": str(city),
            "country": str(country),
            "price": str(price)
        }
        if st.button("Make Transaction"):
            response = requests.post("http://localhost:8000/user/payment", json=payload)
            formattedResponse = json.loads(response.json())
            price = formattedResponse.get("price")
            if formattedResponse.get("status") == "success":
                st.success(f"You just paid {price}TL",icon="✅")
            else:
                st.error(f"Iyzico says: {formattedResponse['errorMessage']}")
            st.write(formattedResponse)

def check_out_form_payment():
    st.subheader("Check Out Form Payment")
    st.write("This is the about page.")

# Create sidebar navigation
page_options = {
    "Simple Payment": simple_payment,
    "About": check_out_form_payment
}

selected_page = st.sidebar.radio("Payments", list(page_options.keys()))

# Display selected page
page_options[selected_page]()
