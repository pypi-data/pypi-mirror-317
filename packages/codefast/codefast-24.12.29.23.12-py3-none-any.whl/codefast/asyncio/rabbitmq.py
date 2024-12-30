import aio_pika
import json
import typing
from loguru import logger
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_exponential

class ConnectionConfig(BaseModel):
    url: str = Field(..., description="RabbitMQ connection URL")
    queue_name: str = Field(..., description="Queue name")
    connection_timeout: float = Field(
        default=30.0, description="Connection timeout in seconds")
    prefetch_count: int = Field(
        default=10, description="Number of messages to prefetch")

    class Config:
        frozen = True


class BaseProducer:
    def __init__(self, config: ConnectionConfig):
        self.config = config
        self.connection: typing.Optional[aio_pika.Connection] = None
        self.channel: typing.Optional[aio_pika.Channel] = None
        self.queue: typing.Optional[aio_pika.Queue] = None
        self._is_connected: bool = False

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def connect(self) -> None:
        try:
            if not self._is_connected:
                self.connection = await aio_pika.connect_robust(
                    self.config.url,
                    timeout=self.config.connection_timeout
                )
                self.channel = await self.connection.channel()
                self.queue = await self.channel.declare_queue(self.config.queue_name)
                self._is_connected = True
                logger.info(f"Connected to queue: {self.config.queue_name}")
        except Exception as e:
            self._is_connected = False
            logger.error(f"Connection error: {str(e)}")
            raise

    async def send_task(self, message: typing.Dict) -> None:
        try:
            await self.connect()
            await self.channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps(message).encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key=self.queue.name
            )
            logger.debug(f"Message sent: {message}")
        except Exception as e:
            logger.error(f"Failed to send message: {str(e)}")
            self._is_connected = False
            raise


class BaseConsumer:
    def __init__(self, config: ConnectionConfig):
        self.config = config
        self.connection: typing.Optional[aio_pika.Connection] = None
        self.channel: typing.Optional[aio_pika.Channel] = None
        self.queue: typing.Optional[aio_pika.Queue] = None
        self._is_connected: bool = False

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def connect(self) -> None:
        try:
            if not self._is_connected:
                self.connection = await aio_pika.connect_robust(
                    self.config.url,
                    timeout=self.config.connection_timeout
                )
                self.channel = await self.connection.channel()
                await self.channel.set_qos(prefetch_count=self.config.prefetch_count)
                self.queue = await self.channel.declare_queue(self.config.queue_name)
                self._is_connected = True
                logger.info(f"Connected to queue: {self.config.queue_name}")
        except Exception as e:
            self._is_connected = False
            logger.error(f"Connection error: {str(e)}")
            raise

    async def process_queue(self) -> typing.AsyncGenerator[bytes, None]:
        try:
            await self.connect()
            async with self.queue.iterator() as queue_iter:
                async for message in queue_iter:
                    try:
                        async with message.process():
                            yield message.body
                    except Exception as e:
                        logger.error(f"Error processing message: {str(e)}")
        except Exception as e:
            self._is_connected = False
            logger.error(f"Queue processing error: {str(e)}")
            raise


''' USAGE:

from loguru import logger

# Configure loguru logger
logger.add(
    "mq.log",
    rotation="500 MB",
    retention="10 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

# Create config with validation
config = ConnectionConfig(
    url="amqp://guest:guest@localhost/",
    queue_name="my_queue",
    connection_timeout=30.0,
    prefetch_count=10
)

# Producer
producer = BaseProducer(config)
await producer.send_task({"key": "value"})

# Consumer
async with BaseConsumer(config) as consumer:
    async for message in consumer.process_queue():
        # Process message
        logger.info(f"Received message: {message}")

'''
