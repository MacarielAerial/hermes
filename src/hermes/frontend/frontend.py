import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:80"

def register_user(email, password):
    try:
        response = requests.post(
            f"{BASE_URL}/register/",
            json={"email": email, "password": password}
        )
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json(), response.status_code
    except requests.RequestException as e:
        return {"error": str(e)}, getattr(e.response, 'status_code', 500)

def login_user(email, password):
    try:
        response = requests.post(
            f"{BASE_URL}/login/",
            json={"email": email, "password": password}
        )
        response.raise_for_status()
        return response.json(), response.status_code
    except requests.RequestException as e:
        return {"error": str(e)}, getattr(e.response, 'status_code', 500)

def create_item(user_id, name, quantity, token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(
            f"{BASE_URL}/users/{user_id}/items/",
            headers=headers,
            json={"name": name, "quantity": int(quantity)}
        )
        response.raise_for_status()
        return response.json(), response.status_code
    except requests.RequestException as e:
        return {"error": str(e)}, getattr(e.response, 'status_code', 500)

def login_page():
    st.header("Login", divider=False)
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", type="primary"):
        result, status_code = login_user(email, password)
        if status_code == 200 and "access_token" in result:
            st.session_state.token = result["access_token"]
            st.session_state.user_id = result.get("user_id", "1")  # Fallback to "1" if user_id is not provided
            st.success("Logged in successfully!")
            st.rerun()  # Use st.rerun() instead of st.experimental_rerun()
        else:
            st.error(f"Login failed: {result.get('error', 'Unknown error')}")

def register_page():
    st.header("Register", divider=False)
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")
    if st.button("Register", type="primary"):
        result, status_code = register_user(email, password)
        if status_code == 201:
            st.success("Registration successful! Please log in.")
        else:
            st.error(f"Registration failed: {result.get('error', 'Unknown error')}")

def create_item_page():
    st.header("Create Item", divider=False)
    name = st.text_input("Item Name")
    quantity = st.number_input("Quantity", min_value=0, step=1)
    if st.button("Create Item", type="primary"):
        result, status_code = create_item(st.session_state.user_id, name, quantity, st.session_state.token)
        if status_code == 201:
            st.success(f"Item '{name}' created successfully!")
        else:
            st.error(f"Failed to create item: {result.get('error', 'Unknown error')}")

def main():
    st.set_page_config(page_title="Event Stock Exchange", layout="centered")

    # Custom CSS for improved readability and design
    st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 4px;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border-radius: 4px;
        color: #333333;  /* Dark text color for input */
    }
    h1, h2, h3, p {
        color: #333333;
    }
    .stTabs {
        background-color: #ffffff;
        border-radius: 4px;
        padding: 1rem;
    }
    .stTab {
        background-color: #f0f2f6;
        color: #333333;
        border-radius: 4px 4px 0 0;
    }
    .stTab[aria-selected="true"] {
        background-color: #4CAF50;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Event Stock Exchange")

    if "token" not in st.session_state:
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            login_page()
        with tab2:
            register_page()
    else:
        create_item_page()
        if st.button("Logout", type="secondary"):
            del st.session_state.token
            del st.session_state.user_id
            st.rerun()

if __name__ == "__main__":
    main()