from inferenceLM.data.request_status import RequestStatus
from inferenceLM.engine.lm_engine import LMEngine
from inferenceLM.data.request import RequestData
from inferenceLM.data.tokenized_data import TokenizedData
import asyncio
import pytest
import asyncio
import pytest
from inferenceLM.request_receiver.request_receiver import RequestReceiver

@pytest.mark.asyncio
async def test_multiple_user_data_flow():
    pending_queue = asyncio.Queue()
    waiting_queue = []
    request_store = {}

    receiver = RequestReceiver("gpt2", pending_queue, request_store)
    lm_engine = LMEngine(pending_queue, waiting_queue, request_store)

    # 3 Users submit requests concurrently for 3 times
    inputs = []
    request_ids = []
    for i in range(3):
        user_input = [{"prompt_text": f"Prompt {i}", "user_id": f"user_{j}"} for j in range(3)]
        inputs.extend(user_input)
        coros = [receiver.submit_request(user_input[j]["prompt_text"], user_input[j]["user_id"]) for j in range(3)]
        request_ids.extend(await asyncio.gather(*coros))

    # Start the LM Engine to fetching requests and put them in waiting_queue
    lm_engine.open = True
    await lm_engine.run() # 在 background register task
    await pending_queue.join()

    assert len(waiting_queue) == 9, "All tokenized requests should be moved to waiting queue"

    # Check if waiting_queue contents are correct and in order
    for i in range(9):
        tokenized_data = waiting_queue[i]
        expected_prompt = f"Prompt {i//3}"
        expected_user_id = f"user_{i%3}"
        assert tokenized_data.tokens == receiver.tokenizer.encode(expected_prompt), f"Expected tokens for '{expected_prompt}', got {tokenized_data.tokens}"
        assert tokenized_data.request_id == request_ids[i], f"Expected request ID {request_ids[i]}, got {tokenized_data.request_id}"
        assert request_store[tokenized_data.request_id].user_id == expected_user_id, f"Expected user ID {expected_user_id}, got {request_store[tokenized_data.request_id].user_id}"
        assert request_store[tokenized_data.request_id].status == RequestStatus.WAITING, f"Expected status WAITING, got {request_store[tokenized_data.request_id].status}"


@pytest.mark.asyncio
async def test_data_flow():
    pending_queue = asyncio.Queue()
    waiting_queue = []
    request_store = {}

    receiver = RequestReceiver("gpt2", pending_queue, request_store)
    lm_engine = LMEngine(pending_queue, waiting_queue, request_store)

    # Submit requests
    ids = []
    incoming_requests = [{"prompt_text": f"Prompt {i}", "user_id": f"user_{i}"} for i in range(10)]
    for user_input in incoming_requests:
        id = await receiver.submit_request(user_input["prompt_text"], user_input["user_id"])
        ids.append(id)

    # Check requests are stored in request_store
    for i in range(10):
        request_id = ids[i]
        assert request_id in request_store, f"Request ID {request_id} should be in request_store"
        assert request_store[request_id].prompt_text == f"Prompt {i}", f"Prompt text for Request ID {request_id} should match"
        assert request_store[request_id].user_id == f"user_{i}", f"User ID for Request ID {request_id} should match"
        assert request_store[request_id].status == RequestStatus.PENDING, f"Status for Request ID {request_id} should be PENDING"

    # Start the LM Engine to fetching requests and put them in waiting_queue
    lm_engine.open = True
    await lm_engine.run()
    await pending_queue.join()  # Wait until all requests in pending_queue are processed
    assert len(waiting_queue) == 10, "All tokenized requests should be moved to waiting queue"
    
    # Check the tokenized data inside the waiting_queue matches the original requests
    for i in range(10):
        tokenized_data = waiting_queue[i]
        assert tokenized_data.request_id == ids[i], f"Request ID in waiting_queue should match"
        expected_tokens = receiver.tokenizer.encode(f"Prompt {i}")
        assert tokenized_data.tokens == expected_tokens, f"Tokens for Request ID {tokenized_data.request_id} in waiting_queue should match tokenizer output"
