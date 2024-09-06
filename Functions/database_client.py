import requests
from Functions.classes import Account

BASE_URL = 'https://pfmtugascaslabkendaliftui2024.loca.lt'

def _addAccount(account: Account) -> bool:
    url = f'{BASE_URL}/_addAccount'
    data = {
        'username': account.username,
        'password': account.password,
        'security_question': account.security_question,
        'security_answer': account.security_answer,
        'balance': account.balance
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False

def _checkAccount(username: str, password: str) -> bool:
    url = f'{BASE_URL}/_checkAccount/{username}/{password}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['exists']:
            return True
    except requests.exceptions.RequestException:
        return False

def _checkSecurity(username:str, security_question:int, security_answer:str) -> bool:
    url = f'{BASE_URL}/_checkSecurity/{username}/{security_question}/{security_answer}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['exists']:
            return True
    except requests.exceptions.RequestException:
        return False
    
def _updateBalance(username: str, new_balance: int) -> bool:
    url = f'{BASE_URL}/_updateBalance'
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

def _getAccount(username: str)-> dict:
    url = f'{BASE_URL}/_getAccount/{username}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

def _editAccount(account : Account)-> bool:
    url = f'{BASE_URL}/_editAccount'
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

def _deleteAccount(username: str)-> bool:
    url = f'{BASE_URL}/_deleteAccount'
    data = {
        'username': username
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False

def _isUsernameAvailable(username: str) -> bool:
    url = f'{BASE_URL}/_isUsernameAvailable/{username}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False

def _addTransaction(id: str, username: str, item: str, type: int, category: int, value: int, created_at: str, updated_at: str)-> bool:
    url = f'{BASE_URL}/_addTransaction'
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

def _getTransaction(username: str)-> dict:
    url = f'{BASE_URL}/_getTransaction/{username}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print (f"Error occurred: {e}")
        return None

def _editTransaction(username: str, transaction_id: str, item: str, type: int, category: int, value: int, created_at: str, updated_at: str)-> bool:
    url = f'{BASE_URL}/_editTransaction'
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
    
def _deleteTransaction(username: str, transaction_id: str)-> bool:
    url = f'{BASE_URL}/_deleteTransaction'
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
    
def _addLog(message:str)-> bool:
    url = f'{BASE_URL}/_addLog'
    data = {
        'message': message
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False
