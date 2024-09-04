from flask import Flask, request, jsonify
from Functions.database_host import *
from Functions.classes import Account

app = Flask(__name__)

# Inisialisasi database saat aplikasi dimulai
createDatabase()

# Route untuk menambahkan akun baru
@app.route('/add_account', methods=['POST'])
def add_account():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        security_question = data.get('security_question')
        security_answer = data.get('security_answer')
        balance = data.get('balance', 0)  # Default balance ke 0 jika tidak ada
        
        # Pastikan semua argumen yang diperlukan disediakan
        account = Account(username=username, password=password, security_question=security_question, security_answer=security_answer, balance=balance)
        
        addAccount(account)
        
        return jsonify({"message": "Account added successfully!"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    
# Route untuk memeriksa keberadaan akun
@app.route('/check_account/<username>/<password>', methods=['GET'])
def check_account(username, password):
    account = getAccount(username)
    if account and account.password == password:
        return jsonify({"exists": True}), 200
    else:
        return jsonify({"exists": False}), 200

# Route untuk memeriksa keberadaan pertanyaan keamanan
@app.route('/check_security/<username>/<security_question>/<security_answer>', methods=['GET'])
def check_security(username, security_question, security_answer):
    account = getAccount(username)
    if account and account.security_question == security_question and account.security_answer == security_answer:
        return jsonify({"exists": True}), 200
    else:
        return jsonify({"exists": False}), 200

# Route untuk memperbarui saldo akun
@app.route('/update_balance', methods=['POST'])
def update_balance():
    try:
        data = request.json
        username = data.get('username')
        new_balance = data.get('balance')
        
        # Pastikan akun ada di database sebelum memperbarui saldo
        
        account = getAccount(username)
        updateBalance(account, new_balance)
        
        return jsonify({"message": "Balance updated successfully!"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Route untuk mendapatkan data akun
@app.route('/get_account/<username>', methods=['GET'])
def get_account(username):
    account = getAccount(username)
    if account:
        return jsonify({
            "username": account.username,
            "balance": account.balance,
            "created_at": account.created_at,
            "updated_at": account.updated_at
        })
    else:
        return jsonify({"message": "Account not found!"}), 404
    
# Route untuk mengedit akun
@app.route('/edit_account', methods=['POST'])
def edit_account():
    try:
        data = request.json
        username = data.get('username')

        account = getAccount(username)
        account.password = data.get('password')
        account.security_question = data.get('security_question')
        account.security_answer = data.get('security_answer')
        account.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        editAccount(account)
        addLog(account, "Account edited")
        
        return jsonify({"message": "Account edited successfully!"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Route untuk menghapus akun
@app.route('/delete_account/<username>', methods=['DELETE'])
def delete_account(username):
    try:
        account = getAccount(username)
        deleteAccount(account)
        
        return jsonify({"message": "Account deleted successfully!"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
    
# Route untuk memeriksa ketersediaan username
@app.route('/is_username_available/<username>', methods=['GET'])
def is_username_available(username):
    account = getAccount(username)
    if account:
        return jsonify({"available": False}), 200
    else:
        return jsonify({"available": True}), 200

# Route untuk menambahkan transaksi baru
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    try:
        data = request.json
        id = data.get('id')
        username = data.get('username')
        item = data.get('item')
        type = data.get('type')
        category = data.get('category')
        value = data.get('value')
        created_at = data.get('created_at')
        updated_at = data.get('updated_at')
        
        # Pastikan akun ada di database sebelum menambahkan transaksi

        account = getAccount(username)
        addTransaction(id, account, item, type, category, value, created_at, updated_at)
        
        return jsonify({"message": "Transaction added successfully!"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Route untuk mendapatkan data transaksi
@app.route('/get_transaction/<username>', methods=['GET'])
def get_transaction(username):
    try:

        account = getAccount(username)
        # Mengambil data transaksi dari database
        df = getTransaction(account)
        
        # Mengubah DataFrame menjadi format JSON
        transactions = df.to_dict(orient='records')
        
        return jsonify(transactions), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
    
# Route untuk mengedit transaksi
@app.route('/edit_transaction', methods=['POST'])
def edit_transaction():
    try:
        data = request.json
        username = data.get('username')
        transaction_id = data.get('transaction_id')
        item = data.get('item')
        type = data.get('type')
        category = data.get('category')
        value = data.get('value')
        created_at = data.get('created_at')
        updated_at = data.get('updated_at')
        
        # Pastikan akun ada di database sebelum mengedit transaksi

        account = getAccount(username)
        editTransaction(account, transaction_id, item, type, category, value, created_at, updated_at)
        
        return jsonify({"message": "Transaction edited successfully!"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Route untuk menambahkan chat
@app.route('/add_chats', methods=['POST'])
def add_chats():
    try:
        data = request.json
        id = data.get('id')
        username = data.get('username')
        message_type = data.get('message_type')
        message = data.get('message')
        
        # Pastikan akun ada di database sebelum menambahkan chat
        addChats(username, message_type, message, id)
        
        return jsonify({"message": "Chat added successfully!"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Route untuk menambahkan log
@app.route('/add_log', methods=['POST'])
def add_log():
    try:
        data = request.json
        message = data.get('message')
        
        addLog(message)
        
        return jsonify({"message": "Log added successfully!"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Jalankan server Flask
if __name__ == '__main__':
    app.run(debug=True)
