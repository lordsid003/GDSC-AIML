import streamlit as st
from model import CarChatbot


st.title("The Car Whisperer 🚗")
st.text("Tell me your preferences, and I'll suggest the perfect car for you!")


bot = CarChatbot()


user_message = st.text_input("Enter your preferences:", placeholder="E.g., I want an electric SUV under $30,000.")

  
if st.button("Get Recommendations"):
    if user_message:
        response = bot.chat(user_message)
        st.text_area("Car Recommendations", response, height=300)
    else:
        st.warning("Please enter your preferences!")