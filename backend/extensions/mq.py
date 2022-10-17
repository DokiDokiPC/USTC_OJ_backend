import pika

from backend.config import get_config

class MQ:
    def __init__(self, app=None):
        # 与RabbitMQ建立连接
        self.connection = pika.BlockingConnection(pika.URLParameters(get_config('AMQP_URI')))
        self.channel = self.connection.channel()
        self.channel.queue_declare(get_config('QUEUE_NAME'))
        if app is not None:
            self.init_app(app)
            
    def init_app(self, app):
        pass

mq = MQ()
