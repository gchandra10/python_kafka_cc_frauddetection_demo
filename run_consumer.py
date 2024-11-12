import sys
from transaction_consumer import TransactionConsumer

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_consumer.py <consumer_id>")
        sys.exit(1)
        
    consumer_id = sys.argv[1]
    consumer = TransactionConsumer(consumer_id)
    consumer.run()  