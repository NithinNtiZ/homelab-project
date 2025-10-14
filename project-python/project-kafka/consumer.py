from confluent_kafka import Consumer, KafkaError

# Kafka consumer configuration
conf = {
    'bootstrap.servers': '10.192.36.21:9092',       # Kafka broker address
    'group.id': 'my-python-consumer-group',      # Unique consumer group id
    'auto.offset.reset': 'earliest'              # Start from beginning if no offset found
}

# Create Consumer instance
consumer = Consumer(conf)

# Subscribe to topic
consumer.subscribe(['test'])

print("📥 Listening for messages on 'test' topic... (Press Ctrl+C to stop)")

try:
    while True:
        msg = consumer.poll(1.0)  # Wait for message or timeout

        if msg is None:
            continue  # No message, loop again
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue  # End of partition, continue polling
            else:
                print(f"❌ Error: {msg.error()}")
                break
        else:
            print(f"✅ Received message: {msg.value().decode('utf-8')}")

except KeyboardInterrupt:
    print("\n🛑 Stopping consumer...")

finally:
    # Close the consumer to commit final offsets and clean up
    consumer.close()
