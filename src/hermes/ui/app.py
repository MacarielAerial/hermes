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


def delete_user() -> None:
    st.subheader("Delete User")
    user_id = st.text_input("User ID (UUID)")
    if st.button("Delete User"):
        try:
            uuid.UUID(user_id)  # Validate UUID
            response = requests.post(f"{BASE_URL}/delete-user/{user_id}")
            if response.status_code == 200:
                st.success(response.json()["message"])
            elif response.status_code == 404:
                st.warning("User not found")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except ValueError:
            st.error("Invalid UUID format")


def create_item() -> None:
    st.subheader("Create Item")
    user_id = st.text_input("User ID (UUID)")
    name = st.text_input("Item Name")
    quantity = st.number_input("Quantity", min_value=0, step=1)
    if st.button("Create Item"):
        try:
            uuid.UUID(user_id)  # Validate UUID
            item_data = {"name": name, "quantity": quantity}
            response = requests.post(
                f"{BASE_URL}/create-item/{user_id}", json=item_data
            )
            if response.status_code == 201:
                st.success(response.json()["message"])
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except ValueError:
            st.error("Invalid UUID format")


def get_item() -> None:
    st.subheader("Get Item")
    item_id = st.text_input("Item ID (UUID)")
    if st.button("Get Item"):
        try:
            uuid.UUID(item_id)  # Validate UUID
            response = requests.get(f"{BASE_URL}/get-item/{item_id}")
            if response.status_code == 200:
                st.success(response.json()["message"])
            elif response.status_code == 404:
                st.warning("Item not found")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except ValueError:
            st.error("Invalid UUID format")


def delete_item() -> None:
    st.subheader("Delete Item")
    item_id = st.text_input("Item ID (UUID)")
    if st.button("Delete Item"):
        try:
            uuid.UUID(item_id)  # Validate UUID
            response = requests.post(f"{BASE_URL}/delete-item/{item_id}")
            if response.status_code == 200:
                st.success(response.json()["message"])
            elif response.status_code == 404:
                st.warning("Item not found")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except ValueError:
            st.error("Invalid UUID format")


def main() -> None:
    st.title("Event Stock Exchange Admin Portal")

    action = st.sidebar.selectbox(
        "Choose an action",
        (
            "Create User",
            "Get User",
            "Get All Users",
            "Delete User",
            "Create Item",
            "Get Item",
            "Delete Item",
        ),
    )

    if action == "Create User":
        create_user()
    elif action == "Get User":
        get_user()
    elif action == "Get All Users":
        get_users()
    elif action == "Delete User":
        delete_user()
    elif action == "Create Item":
        create_item()
    elif action == "Get Item":
        get_item()
    elif action == "Delete Item":
        delete_item()


if __name__ == "__main__":
    main()
