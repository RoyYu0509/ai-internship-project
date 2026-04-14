from inferenceLM.data.request_status import RequestStatus
from inferenceLM.engine.lm_engine import LMEngine
from inferenceLM.data.request import RequestData
from inferenceLM.data.tokenized_data import TokenizedData
import asyncio
import pytest

def test_lm_engine_is_default_shutdown():
    pending_queue = asyncio.Queue()
    waiting_queue = []
    request_store = {}
    lm_engine = LMEngine(pending_queue, waiting_queue, request_store)
    assert not lm_engine.open, "LM Engine should be closed by default"

@pytest.mark.asyncio
async def test_lm_engine_cant_get_request_when_closed():
    pending_queue = asyncio.Queue()
    waiting_queue = []
    request_store = {}

    await pending_queue.put("test_tokenized_data")
    lm_engine = LMEngine(pending_queue, waiting_queue, request_store)
    with pytest.raises(Exception, match='LM Engine is not open. Please start the engine before getting requests.'):
        await lm_engine.get_request()

@pytest.mark.asyncio
async def test_lm_engine_cant_run_when_closed():
    pending_queue = asyncio.Queue()
    waiting_queue = []
    request_store = {}

    lm_engine = LMEngine(pending_queue, waiting_queue, request_store)
    with pytest.raises(Exception, match="LM Engine is not open. Please start the engine before running it."):
        await lm_engine.run()


@pytest.mark.asyncio
async def test_lm_engine_put_request_in_waiting_queue():
    pending_queue = asyncio.Queue()
    waiting_queue = []
    request_store = {}
    tokenized_requests = [TokenizedData(f"test_tokenized_data_{i}", [i]) for i in range(5)]

    lm_engine = LMEngine(pending_queue, waiting_queue, request_store)
    lm_engine.open = True

    for tokenized_request in tokenized_requests:
        await pending_queue.put(tokenized_request)
        request_store[tokenized_request.request_id] = RequestData(
            prompt_text="test_prompt",
            user_id="test_user",
            request_id=tokenized_request.request_id,
            timestamp=0.0,
        )
    
    await lm_engine.run()
    await pending_queue.join()

    assert len(waiting_queue) == len(tokenized_requests), "All tokenized requests should be moved to waiting queue"
    for tokenized_request in waiting_queue:
        assert tokenized_request in tokenized_requests, f"{tokenized_request} should be in the original tokenized requests"
    

@pytest.mark.asyncio
async def test_lm_engine_updates_request_status_to_waiting():
    pending_queue = asyncio.Queue()
    waiting_queue = []
    request_store = {}
    tokenized_request = TokenizedData("test_tokenized_data", [0])

    lm_engine = LMEngine(pending_queue, waiting_queue, request_store)
    lm_engine.open = True

    await pending_queue.put(tokenized_request)
    request_store[tokenized_request.request_id] = RequestData(
        prompt_text="test_prompt",
        user_id="test_user",
        request_id=tokenized_request.request_id,
        timestamp=0.0,
    )
    
    await lm_engine.run()
    await pending_queue.join()

    assert request_store[tokenized_request.request_id].status == RequestStatus.WAITING, "Request status should be updated to WAITING"
