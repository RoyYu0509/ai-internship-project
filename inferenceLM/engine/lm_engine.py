import asyncio
from inferenceLM.data.request_status import RequestStatus
from inferenceLM.data.tokenized_data import TokenizedData
from typing import List, Dict
from inferenceLM.data.request import RequestData

class LMEngine:
    """
    This class is responsible for:
        从 waiting queue 里拿 tokenized data -> run LM inference  
    
    Attributes:
        pending_queue (asyncio.Queue): Reference to a shared waiting queue with Request Receiver.
        waiting_queue (List[TokenizedData]): A list shared with Scheduler to store tokenized data waiting for processing.
    """
    pending_queue: asyncio.Queue[TokenizedData]
    waiting_queue: List[TokenizedData]
    request_store: Dict[str, RequestData]
    open: bool

    def __init__(self, pending_queue: asyncio.Queue, waiting_queue: List[TokenizedData], request_store: Dict[str, RequestData]):
        self.pending_queue = pending_queue
        self.waiting_queue = waiting_queue
        self.request_store = request_store
        self.open = False

    async def get_request(self) -> TokenizedData:
        """
        Get a TokenizedData from the shared pending_queue, put it in to the waiting_queue.
        Update the request status to WAITING.

        Returns:
            tokenized_data (TokenizedData): The TokenizedData retrieved from the pending_queue.
        """
        if not self.open:
            raise Exception("LM Engine is not open. Please start the engine before getting requests.")
        
        tokenized_data = await self.pending_queue.get()
        self.pending_queue.task_done() # Mark the task as done after processing the tokenized data
        return tokenized_data
    
    async def keep_fetching_requests(self):
        """
        Keep fetching tokenized data from the pending queue and put it in the waiting queue.
        Update the request status to WAITING.
        """
        while True:
            if not self.open:
                raise Exception("LM Engine is not open. Please start the engine before running it.")

            if len(self.waiting_queue) > 10:
                await asyncio.sleep(0.1)  # 保证 waiting buffer 中不要积压太多 request.
                continue

            tokenized_data = await self.get_request()
            request_id = tokenized_data.request_id
            self.request_store[request_id].status = RequestStatus.WAITING

            self.waiting_queue.append(tokenized_data)

    async def run(self):
        """
        Start the LM Engine to keep fetching requests and run inference.
        """
        if not self.open:
            raise Exception("LM Engine is not open. Please start the engine before running it.")
        
        asyncio.create_task(self.keep_fetching_requests()) 
        #TODO: Add Inference code here

    def kill(self):
        """
        Shut down the LM Engine and kill any active jobs.
        """
        self.open = False
