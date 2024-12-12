import pika


def send_message(message:str = 'Hello World!'):


    # Create a connection to the RabbitMQ server (D)
    parameters = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')
    connection = pika.BlockingConnection(parameters)

    # Create a channel 
    channel = connection.channel()

    # Create a queue in host
    channel.queue_declare(queue='test_queue', durable=True)

    # In this case we will use the default exchange, which requires the routing_key to be the same as the queue name
    # Name of queue match the routing_key. Name queue = my_queue , routing_key = my_queue (Default exchange)
    channel.basic_publish(exchange='', routing_key='test_queue', body=message)
    print(f"Sending message......")
    print(f"Message sent: {message}")
    connection.close()

def receive_message():

    # Create a connection to the RabbitMQ server 
    parameters = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')
    connection = pika.BlockingConnection(parameters)

    # This is the callback function that will be called when a message is received
    def print_message_cb(ch, method, properties, body):
        message_str = body.decode('utf-8')
        print(f"Message received: {message_str}\nTo exit press Ctr + C")
    print(f"Getting the message from queue......")

    # Create a channel
    channel = connection.channel()
    channel.basic_consume(queue='test_queue', on_message_callback=print_message_cb, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    message = 'Hello World!'
    try:
        send_message(message)
        receive_message()
    except KeyboardInterrupt as k:
        print(f"Exiting the program....")
        exit()

