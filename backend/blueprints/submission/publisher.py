from time import sleep
import signal
import logging
import json

import pika
from pika.exceptions import AMQPChannelError, ConnectionOpenAborted, ConnectionClosedByBroker, AMQPConnectionError

from backend.config import get_config


# 这个函数将作为子进程被调用, 父进程需要向子进程传入Pipe的接收端, 当需要发送时, 父进程使用Pipe发送端send判题请求
def publisher(pipe_recv_end):
    # 设置log格式和级别
    LOG_FORMAT = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s'
    LOGGER = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    
    QUEUE = 'judge_request_queue'  # 队列名
    AMQP_URI = get_config('AMQP_URI')

    publish_properties = pika.BasicProperties(
        app_id='publisher',
        content_type='application/json',
        delivery_mode=pika.DeliveryMode.Transient
    )
    
    # 父进程调用p.terminate()向子进程发送SIGTERM信号, 我们使用signal.signal注册一个新的handler,
    # raise一个自定义的SigtermException, 这样可以手动捕获
    class SigtermException(Exception):
        pass
    
    def sigterm_handler(_signal, _frame):
        raise SigtermException('Got SIGTERM')
    
    signal.signal(signal.SIGTERM, sigterm_handler)
    
    # 连接有可能中断, 所以外面套了一层死循环, 当捕获到异常, 可以continue重新连接, 也可以break结束
    while True:
        try:
            LOGGER.info(f'Connection to {AMQP_URI}')
            connection = pika.BlockingConnection(pika.URLParameters(AMQP_URI))
            LOGGER.info('Connection opened')
            
            LOGGER.info('Creating a new channel')
            channel = connection.channel()
            LOGGER.info('Channel opened')
            
            LOGGER.info(f'Declaring queue {QUEUE}')
            channel.queue_declare(QUEUE)
            LOGGER.info('Queue declared')
            
            try:
                # 死循环, 一直处理父进程send过来的消息
                while True:
                    message = pipe_recv_end.recv()  # 取消息, 若空则阻塞, 直到父进程send
                    channel.basic_publish(
                        exchange='',
                        routing_key=QUEUE,
                        body=json.dumps(message, ensure_ascii=False),
                        properties=publish_properties
                    )
            except SigtermException:
                LOGGER.info('Stopping')
                LOGGER.info('Closing the channel')
                channel.close()
                LOGGER.info('Closing the connection')
                connection.close()
                LOGGER.info('Closing the pipe')
                pipe_recv_end.close()
                break
        
        except AMQPChannelError as err:
            LOGGER.error(f'Channel was closed: {err}')
            break
        
        except ConnectionOpenAborted as err:
            LOGGER.error(f'Connection open failed, reopening in 5 seconds: {err}')
            sleep(5)
        
        except ConnectionClosedByBroker as err:
            LOGGER.warning(f'Connection was closed by broker, reopening in 5 seconds: {err}')
            sleep(5)
        
        except AMQPConnectionError as err:
            LOGGER.warning(f'Connection closed, reopening in 5 seconds: {err}')
            sleep(5)
    
    LOGGER.info('Publisher stopped')
