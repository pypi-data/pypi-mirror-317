import os
import logging
from json import dumps
from dotenv import load_dotenv
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage
from azure.core.exceptions import AzureError
from Helpers.Message import SERVICE_BUS_FAILED

load_dotenv()
logging.basicConfig(level=logging.INFO)

class ServicesBus:
    
    def __init__(self):
        self.CONNECTION_STRING = os.getenv('CONNECTION_STRING')
        self.QUEUE_NAME = os.getenv('QUEUE')

    async def send_message(self, message_json: dict) -> None:
        """Method to send a message to the Service Bus."""
        try:
            async with ServiceBusClient.from_connection_string(self.CONNECTION_STRING) as servicebus_client:
                async with servicebus_client.get_queue_sender(queue_name=self.QUEUE_NAME) as sender:
                    message = ServiceBusMessage(dumps(message_json))
                    await sender.send_messages(message)

        except AzureError as e:
            logging.error(f'{SERVICE_BUS_FAILED}: {e}')