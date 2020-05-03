"""Server"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from blockchain import Blockchain
from wallet import Wallet

app = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)
CORS(app)


@app.route('/', methods=['GET'])
def get_ui():
    return send_from_directory('ui', 'node.html')


@app.route('/wallet', methods=['POST'])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    return jsonify({'message': 'Saving the keys failed'}), 500


@app.route('/wallet', methods=['GET'])
def load_keys():
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    return jsonify({'message': 'Loading the keys failed'}), 500


@app.route('/balance', methods=['GET'])
def get_balance():
    balance = blockchain.get_balance()
    if balance is not None:
        response = {
            'message': 'Fetched balance successfully',
            'funds': balance
        }
        return jsonify(response), 200
    response = {
        'message': 'Loading balance failed',
        'wallet_set_up': wallet.private_key is not None
    }
    return jsonify(response), 500


@app.route('/transaction', methods=['POST'])
def add_transaction():
    if wallet.public_key is None:
        return jsonify({'message': 'No wallet set up'}), 400

    values = request.get_json()
    if not values:
        return jsonify({'message': 'No data found'}), 400

    required_fields = ['recipient', 'amount']
    if not all(field in values for field in required_fields):
        return jsonify({'message': 'Required data is missing'}), 400

    recipient = values['recipient']
    amount = values['amount']
    signature = wallet.sign_transaction(wallet.public_key,
                                        recipient,
                                        amount)
    success = blockchain.add_transaction(recipient,
                                         wallet.public_key,
                                         signature,
                                         amount)
    if success:
        response = {
            'message': 'Succesfully added transaction',
            'transaction': {
                'sender': wallet.public_key,
                'recipient': recipient,
                'amount': amount,
                'signature': signature
            },
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    return jsonify({'message': 'Creating a transaction failed'}), 500


@app.route('/transactions', methods=['GET'])
def get_open_transaction():
    transactions = blockchain.get_open_transactions()
    transactions = [tx.__dict__ for tx in transactions]
    response = {
        'message': 'Fetched transactions successfully',
        'transactions': transactions
    }
    return jsonify(transactions), 200


@app.route('/mine', methods=['POST'])
def mine():
    block = blockchain.mine_block()
    if block is not None:
        block = block.__dict__.copy()
        block['transactions'] = [tx.__dict__ for tx in block['transactions']]
        response = {
            'message': 'Block added successfully',
            'block': block,
            'funds': blockchain.get_balance(),
        }
        return jsonify(response), 201
    response = {
        'message': 'Adding a block fail',
        'wallet_set_up': wallet.public_key is not None,
    }
    return jsonify(response), 500


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_snapshot = blockchain.chain
    chain_snapshot = [block.__dict__.copy()
                      for block in chain_snapshot]
    for chain in chain_snapshot:
        chain['transactions'] = [tx.__dict__
                                 for tx in chain['transactions']]
    return jsonify(chain_snapshot), 200


if __name__ == '__main__':
    app.run(host='localhost', port='5000')
