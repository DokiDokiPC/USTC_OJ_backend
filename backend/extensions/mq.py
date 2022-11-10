import pika

from backend.config import Config

class MQ:
    def __init__(self, app=None):
        # 与RabbitMQ建立连接
        self.connection = pika.BlockingConnection(pika.URLParameters(Config.AMQP_URI))
        self.channel = self.connection.channel()
        self.channel.queue_declare(Config.QUEUE_NAME)
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        pass

mq = MQ()
