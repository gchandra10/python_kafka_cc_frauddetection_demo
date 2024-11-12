import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

class TransactionGenerator:
    def __init__(self, bootstrap_servers=['localhost:9092']):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
    def generate_transaction(self, fraud_probability=0.1):
        # Generate either valid or fraudulent transaction
        is_fraud = random.random() < fraud_probability
        
        if is_fraud:
            amount = random.uniform(800, 5000)
            distance = random.uniform(50, 1000)
            time_diff = random.uniform(0, 5)
        else:
            amount = random.uniform(10, 1000)
            distance = random.uniform(0, 50)
            time_diff = random.uniform(5, 60)
            
        transaction = {
            'transaction_id': str(random.randint(1000000, 9999999)),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'amount': round(amount, 2),
            'distance_from_home': round(distance, 2),
            'time_since_last_transaction': round(time_diff, 2),
            'actual_fraud': 1 if is_fraud else 0  # For training/validation
        }
        return transaction

    def run(self):
        try:
            while True:
                transaction = self.generate_transaction()
                self.producer.send('transactions-topic', value=transaction)
                print(f"Generated transaction: {transaction}")
                time.sleep(random.uniform(0.5, 2))
        except KeyboardInterrupt:
            self.producer.close()