import streamlit as st
import requests
import base64
import io
from PIL import Image

API_URL = "http://localhost:8888/process_request"

st.title("Database Chatbot")
st.write("Ask questions related to the database content.")

# Initialize session state variables
if 'user_query' not in st.session_state:
    st.session_state.user_query = ""

if 'response' not in st.session_state:
    st.session_state.response = ""

if 'plots' not in st.session_state:
    st.session_state.plots = {}

# Input field for the user query
user_query = st.text_input("Enter your query:", value=st.session_state.user_query, key='query_input')

def call_backend_api(query):
    try:
        headers = {"Content-Type": "application/json"}
        data = {"user_query": query, "request_id": "123"}
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raise exception for non-2xx status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while communicating with the backend: {e}")
        return None

# Enter button to trigger API call
if st.button("Enter"):
    if user_query:
        response = call_backend_api(user_query)
        if response:
            st.session_state.response = response.get('remarks', 'No remarks available')
            st.session_state.plots = response.get('plots', {})  # Expecting a dictionary of plots
        else:
            st.session_state.response = "No response received from the backend."
            st.session_state.plots = {}
        st.session_state.user_query = user_query

# Display the response
if st.session_state.response:
    st.write(f"Response: {st.session_state.response}")

# Display all graphical data if available
if st.session_state.plots:
    st.write("Graphical Representations:")
    for plot_type, base64_img in st.session_state.plots.items():
        if base64_img:
            st.write(f"Plot Type: {plot_type.capitalize()}")
            img_data = base64.b64decode(base64_img)
            img = Image.open(io.BytesIO(img_data))
            st.image(img, caption=f"Generated {plot_type.capitalize()} Plot")

# Clear button to reset input and response
if st.button("Clear"):
    st.session_state.user_query = ""
    st.session_state.response = ""
    st.session_state.plots = {}
    st.experimental_rerun()  # Refresh the app to clear the input field
