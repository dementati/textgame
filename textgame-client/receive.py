import pika


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="hello")

    channel.basic_consume(
        queue="hello",
        auto_ack=True,
        on_message_callback=callback,
    )

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")


if __name__ == "__main__":
    main()