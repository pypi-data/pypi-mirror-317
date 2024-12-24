import asyncio
import json
import logging

import aio_pika
from aio_pika import ExchangeType

class LoggerProvider:

    connection: aio_pika.robust_connection = None
    channel: aio_pika.channel = None
    exchange_name = None
    exchange: aio_pika.robust_exchange = None
    rabbitmq_host = None
    rabbitmq_user = None
    rabbitmq_password = None
    logger: logging.Logger = None

    @classmethod
    async def create(cls, rabbitmq_host, rabbitmq_user, rabbitmq_password, logger: logging.Logger):
        self = LoggerProvider()
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_user = rabbitmq_user
        self.rabbitmq_password = rabbitmq_password
        self.logger = logger
        await self.subscribe_channel()
        return self

    async def subscribe_channel(self):
        retries = 5
        for attempt in range(retries):
            try:
                self.connection = await aio_pika.connect_robust(
                    host=self.rabbitmq_host,
                    virtualhost='/',
                    login=self.rabbitmq_user,
                    password=self.rabbitmq_password
                )
                self.channel = await self.connection.channel()
                self.exchange_name = 'log'
                self.exchange = await self.channel.declare_exchange(name=self.exchange_name, type=ExchangeType.TOPIC, durable=True)
                self.logger.info("Connection and channel established successfully.")
                break
            except Exception as e:
                self.logger.error(f"Connection failed: {e}")
                if attempt < retries - 1:
                    self.logger.info("Retrying in 5 seconds...")
                    await asyncio.sleep(5)
                else:
                    self.logger.error("All retry attempts failed")
                    raise  # Important to raise an exception here to prevent further execution with a null connection

    async def publish(self, message_body, routing_key):
        if not self.connection or not self.channel:
            self.logger.error("No active connection or channel to publish message.")
            return
        self.logger.info(f"Publishing message to exchange {self.exchange_name} with routing key {routing_key}")
        await self.exchange.publish(
            aio_pika.Message(
                body=message_body.encode(),
                content_type="text/plain"
            ),
            routing_key=routing_key)
