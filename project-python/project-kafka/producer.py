import time
import random
from confluent_kafka import Producer

# Kafka configuration
conf = {
    'bootstrap.servers': '10.192.36.21:9092',
}

# Create producer
producer = Producer(conf)

# Delivery callback
def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Delivery failed: {err}")
    else:
        print(f"✅ Sent to {msg.topic()} [{msg.partition()}]: {msg.value().decode('utf-8')}")

# Sample pool of random messages
messages = [
    "Hello Kafka!",
    "Random event occurred.",
    "Sensor reading: " + str(random.randint(20, 100)),
    "System log entry.",
    "User login detected.",
    "Heartbeat OK",
    "Event ID: " + str(random.randint(1000, 9999)),
    "Memory usage high",
    "Temperature warning",
    "Disk check complete"
]

# Continuously send random messages
try:
    while True:
        msg = random.choice(messages)
        producer.produce("test", msg.encode('utf-8'), callback=delivery_report)
        producer.poll(0)  # Trigger delivery callback
        time.sleep(2)     # Wait 2 seconds before sending the next one

except KeyboardInterrupt:
    print("\n🛑 Stopping producer...")

finally:
    producer.flush()  # Ensure all messages are delivered

