import requests
from Functions.variables import Account

BASE_URL = 'https://pfmtugascaslabkendaliftui2024.loca.lt'

def add_account(account: Account) -> bool:
    url = f'{BASE_URL}/add_account'
    data = {
        'username': account.username,
        'password': account.password,
        'security_question': account.security_question,
        'security_answer': account.security_answer,
        'balance': account.balance
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return True
    except requests.exceptions.RequestException:
        return False

def check_account(username: str, password: str) -> bool:
    url = f'{BASE_URL}/check_account/{username}/{password}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['exists']:
            return True
    except requests.exceptions.RequestException:
        return False

def check_security(username:str, security_question:int, security_answer:str) -> bool:
    url = f'{BASE_URL}/check_security/{username}/{security_question}/{security_answer}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['exists']:
            return True
    except requests.exceptions.RequestException:
        return False
    
def update_balance(username: str, new_balance: int) -> bool:
    url = f'{BASE_URL}/update_balance'
    data = {
        'username': username,
        'balance': new_balance
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False

def get_account(username: str)-> dict:
    url = f'{BASE_URL}/get_account/{username}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

def edit_account(account : Account)-> bool:
    url = f'{BASE_URL}/edit_account'
    data = {
        'username': account.username,
        'password': account.password,
        'security_question': account.security_question,
        'security_answer': account.security_answer
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False

def delete_account(username: str)-> bool:
    url = f'{BASE_URL}/delete_account'
    data = {
        'username': username
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False

def is_username_available(username: str) -> bool:
    url = f'{BASE_URL}/is_username_available/{username}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False

def add_transaction(id: str, username: str, item: str, type: int, category: int, value: int, created_at: str, updated_at: str)-> bool:
    url = f'{BASE_URL}/add_transaction'
    data = {
        'id': id,
        'username': username,
        'item': item,
        'type': type,
        'category': category,
        'value': value,
        'created_at': created_at,
        'updated_at': updated_at
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False

def get_transaction(username: str)-> dict:
    url = f'{BASE_URL}/get_transaction/{username}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print (f"Error occurred: {e}")
        return None

def edit_transaction(username: str, transaction_id: str, item: str, type: int, category: int, value: int, created_at: str, updated_at: str)-> bool:
    url = f'{BASE_URL}/edit_transaction'
    data = {
        'id': transaction_id,
        'username': username,
        'item': item,
        'type': type,
        'category': category,
        'value': value,
        'created_at': created_at,
        'updated_at': updated_at
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False
    
def delete_transaction(username: str, transaction_id: str)-> bool:
    url = f'{BASE_URL}/delete_transaction'
    data = {
        'username': username,
        'id': transaction_id
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False

def add_chats(username: str, message_type: str, message: str, id:str)-> bool:
    url = f'{BASE_URL}/add_chats'
    data = {
        'id': id,
        'username': username,
        'message_type': message_type,
        'message': message
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False
    
def add_log(message:str)-> bool:
    url = f'{BASE_URL}/add_log'
    data = {
        'message': message
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False
