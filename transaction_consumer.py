from kafka import KafkaConsumer
import json
import joblib
import numpy as np

class TransactionConsumer:
    def __init__(self, consumer_id, bootstrap_servers=['localhost:9092']):
        self.consumer_id = consumer_id
        self.consumer = KafkaConsumer(
            'transactions-topic',
            bootstrap_servers=bootstrap_servers,
            group_id='transaction_processors',
            auto_offset_reset='earliest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self.model = joblib.load('fraud_detection_model.joblib')
        
    def process_transaction(self, transaction):
        features = np.array([
            [
                transaction['amount'],
                transaction['distance_from_home'],
                transaction['time_since_last_transaction']
            ]
        ])
        
        prediction = self.model.predict(features)[0]
        probability = self.model.predict_proba(features)[0][1]
        
        result = {
            'transaction_id': transaction['transaction_id'],
            'predicted_fraud': int(prediction),
            'fraud_probability': round(probability, 3),
            'actual_fraud': transaction['actual_fraud'],
            'correct_prediction': prediction == transaction['actual_fraud']
        }
        return result
        
    def run(self):
        print(f"Consumer {self.consumer_id} started. Processing transactions...")
        try:
            for message in self.consumer:
                transaction = message.value
                result = self.process_transaction(transaction)
                
                print(f"\nConsumer {self.consumer_id} - Partition {message.partition}:")
                print(f"Transaction ID: {result['transaction_id']}")
                print(f"Predicted Fraud: {'Yes' if result['predicted_fraud'] else 'No'}")
                print(f"Fraud Probability: {result['fraud_probability']:.1%}")
                print(f"Actual Fraud: {'Yes' if result['actual_fraud'] else 'No'}")
                print(f"Prediction {'Correct' if result['correct_prediction'] else 'Incorrect'}")
                
        except KeyboardInterrupt:
            self.consumer.close()