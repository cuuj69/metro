from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import time
import random

app = Flask(__name__)
CORS(app)

# In-memory transaction storage (use database in production)
transactions = [
    {
        'id': 'TXN001',
        'date': '15 Jan 2025',
        'description': 'Dividend Payment',
        'reference': 'DIV-2025-001',
        'amount': 12450.00,
        'type': 'credit',
        'status': 'completed'
    },
    {
        'id': 'TXN002',
        'date': '12 Jan 2025',
        'description': 'Property Rental Income',
        'reference': 'RENT-JAN-2025',
        'amount': 3200.00,
        'type': 'credit',
        'status': 'completed'
    },
    {
        'id': 'TXN003',
        'date': '10 Jan 2025',
        'description': 'Trustee Fee Payment',
        'reference': 'FEE-2025-01',
        'amount': -1500.00,
        'type': 'debit',
        'status': 'completed'
    },
    {
        'id': 'TXN004',
        'date': '8 Jan 2025',
        'description': 'Investment Transfer',
        'reference': 'INV-2025-045',
        'amount': -25000.00,
        'type': 'debit',
        'status': 'completed'
    },
    {
        'id': 'TXN005',
        'date': '5 Jan 2025',
        'description': 'Beneficiary Payment',
        'reference': 'BEN-2025-003',
        'amount': -5000.00,
        'type': 'debit',
        'status': 'completed'
    }
]

pending_transactions = {}

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """Get all transactions (completed and pending)"""
    try:
        all_transactions = transactions.copy()
        
        # Add pending transactions
        for txn_id, txn_data in pending_transactions.items():
            all_transactions.append(txn_data)
        
        # Sort by date (newest first)
        all_transactions.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
        
        return jsonify({
            'success': True,
            'transactions': all_transactions
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transfer', methods=['POST'])
def create_transfer():
    """Create a new transfer transaction"""
    try:
        data = request.json
        amount = float(data.get('amount', 0))
        to_account = data.get('toAccount', '')
        description = data.get('description', 'Transfer')
        reference = data.get('reference', '')
        
        if amount <= 0:
            return jsonify({'error': 'Invalid amount'}), 400
        
        # Generate transaction ID
        txn_id = f"TXN{random.randint(100000, 999999)}"
        
        # Create transaction in processing state
        transaction = {
            'id': txn_id,
            'date': datetime.now().strftime('%d %b %Y'),
            'description': description,
            'reference': reference or txn_id,
            'amount': -amount,  # Negative for debit
            'type': 'debit',
            'status': 'processing',
            'to_account': to_account,
            'timestamp': time.time()
        }
        
        # Add to pending transactions
        pending_transactions[txn_id] = transaction
        
        # Simulate processing delay (3-5 seconds)
        processing_delay = random.uniform(3, 5)
        
        # After delay, move to pending
        def move_to_pending():
            import time
            time.sleep(processing_delay)
            if txn_id in pending_transactions:
                pending_transactions[txn_id]['status'] = 'pending'
                pending_transactions[txn_id]['message'] = 'Transaction pending approval'
        
        # Run in background (in production, use proper task queue)
        import threading
        thread = threading.Thread(target=move_to_pending)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'transaction': transaction,
            'message': 'Transaction processing'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transaction/<txn_id>', methods=['GET'])
def get_transaction(txn_id):
    """Get specific transaction status"""
    try:
        # Check pending transactions
        if txn_id in pending_transactions:
            return jsonify({
                'success': True,
                'transaction': pending_transactions[txn_id]
            }), 200
        
        # Check completed transactions
        for txn in transactions:
            if txn['id'] == txn_id:
                return jsonify({
                    'success': True,
                    'transaction': txn
                }), 200
        
        return jsonify({'error': 'Transaction not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)

