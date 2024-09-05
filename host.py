from flask import Flask, request, jsonify
from Functions.database_host import *
from Functions.classes import Account

app = Flask(__name__)

# Inisialisasi database saat aplikasi dimulai
createDatabase()

# Route untuk menambahkan akun baru
@app.route('/_addAccount', methods=['POST'])
def _addAccount():
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
@app.route('/_checkAccount/<username>/<password>', methods=['GET'])
def _checkAccount(username, password):
    account = getAccount(username)
    if account and account.password == password:
        return jsonify({"exists": True}), 200
    else:
        return jsonify({"exists": False}), 200

# Route untuk memeriksa keberadaan pertanyaan keamanan
@app.route('/_checkSecurity/<username>/<security_question>/<security_answer>', methods=['GET'])
def _checkSecurity(username, security_question, security_answer):
    account = getAccount(username)
    if account and account.security_question == security_question and account.security_answer == security_answer:
        return jsonify({"exists": True}), 200
    else:
        return jsonify({"exists": False}), 200

# Route untuk memperbarui saldo akun
@app.route('/_updateBalance', methods=['POST'])
def _updateBalance():
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
@app.route('/_getAccount/<username>', methods=['GET'])
def _getAccount(username):
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
@app.route('/_editAccount', methods=['POST'])
def _editAccount():
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
@app.route('/_deleteAccount/<username>', methods=['DELETE'])
def _deleteAccount(username):
    try:
        account = getAccount(username)
        deleteAccount(account)
        
        return jsonify({"message": "Account deleted successfully!"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
    
# Route untuk memeriksa ketersediaan username
@app.route('/_isUsernameAvailable/<username>', methods=['GET'])
def _isUsernameAvailable(username):
    account = getAccount(username)
    if account:
        return jsonify({"available": False}), 200
    else:
        return jsonify({"available": True}), 200

# Route untuk menambahkan transaksi baru
@app.route('/_addTransaction', methods=['POST'])
def _addTransaction():
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
@app.route('/_getTransaction/<username>', methods=['GET'])
def _getTransaction(username):
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
@app.route('/_editTransaction', methods=['POST'])
def _editTransaction():
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
    
# Route untuk menghapus transaksi
@app.route('/_deleteTransaction', methods=['POST'])
def _deleteTransaction():
    try:
        data = request.json
        username = data.get('username')
        transaction_id = data.get('transaction_id')
        
        # Pastikan akun ada di database sebelum menghapus transaksi

        account = getAccount(username)
        deleteTransaction(account, transaction_id)
        
        return jsonify({"message": "Transaction deleted successfully!"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Route untuk menambahkan chat
@app.route('/_addChats', methods=['POST'])
def _addChats():
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
@app.route('/_addLog', methods=['POST'])
def _addLog():
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
