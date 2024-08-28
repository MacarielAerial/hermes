import uuid

import requests
import streamlit as st

# Set the base URL
BASE_URL = "http://localhost:80"


def create_user() -> None:
    st.subheader("Create User")
    email = st.text_input("Email")
    if st.button("Create"):
        response = requests.post(f"{BASE_URL}/create-user", json={"email": email})
        if response.status_code == 201:
            st.success(response.json()["message"])
        else:
            st.error(f"Error: {response.status_code} - {response.text}")


def get_user() -> None:
    st.subheader("Get User")
    user_id = st.text_input("User ID (UUID)")
    if st.button("Get User"):
        try:
            uuid.UUID(user_id)  # Validate UUID
            response = requests.get(f"{BASE_URL}/get-user/{user_id}")
            if response.status_code == 200:
                st.success(response.json()["message"])
            elif response.status_code == 404:
                st.warning("User not found")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except ValueError:
            st.error("Invalid UUID format")


def get_users() -> None:
    st.subheader("Get All Users")
    if st.button("Get All Users"):
        response = requests.get(f"{BASE_URL}/get-users")
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error(f"Error: {response.status_code} - {response.text}")


def main() -> None:
    st.title("Event Stock Exchange Admin Portal")

    action = st.sidebar.selectbox(
        "Choose an action", ("Create User", "Get User", "Get All Users")
    )

    if action == "Create User":
        create_user()
    elif action == "Get User":
        get_user()
    elif action == "Get All Users":
        get_users()


if __name__ == "__main__":
    main()
