import asyncio
import logging
from dotenv import load_dotenv
from ServicesBus.ServicesBus import ServicesBus

load_dotenv()

class TaskQueue:
    """Queue to manage tasks in order and asynchronously."""

    def __init__(self):
        self.service_bus = ServicesBus()
        self.queue = asyncio.Queue()
        

    def start_processing(self):
        """Start processing tasks in the background."""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        loop.create_task(self.process_tasks())


    async def enqueue(self, message: dict):
        """Add a task to the queue."""
        await self.queue.put(message)


    async def process_tasks(self):
        """Process tasks from the queue in order."""
        while True:
            message = await self.queue.get()
            try:
                await self.service_bus.send_message(message)
            except Exception as e:
                logging.error(f'Message queuing error: {e} | Message: {message}')
            finally:
                self.queue.task_done()


task_queue = TaskQueue()
task_queue.start_processing()