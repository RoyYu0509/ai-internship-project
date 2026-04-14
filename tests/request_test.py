import pytest
from inferenceLM.data.request import RequestData
from inferenceLM.data.request_status import RequestStatus

# Test correct cases
def test_printing_matches():
    user_id: str = "awef"
    request_id: str = "awef"
    timestamp: float = 1.0
    status: RequestStatus = RequestStatus.PENDING
    prompt_text: str = "This is a test"
    
    request = RequestData(
        user_id=user_id,
        request_id=request_id,
        timestamp=timestamp,
        status=status,
        prompt_text=prompt_text
    )

    expected_output = f"RequestData(\nuser_id={user_id}, \nrequest_id={request_id}, \ntimestamp={timestamp}, \nstatus={status}, \nprompt_text={prompt_text} \n)"
    assert str(request) == expected_output


def test_serialization_correct():
    user_id: str = "awef"
    request_id: str = "awef"
    timestamp: float = 1.0
    status: RequestStatus = RequestStatus.PENDING
    prompt_text: str = "This is a test"
    
    request = RequestData(
        user_id=user_id,
        request_id=request_id,
        timestamp=timestamp,
        status=status,
        prompt_text=prompt_text
    )

    target_serialization_txt = '{"user_id":"awef","request_id":"awef","timestamp":1.0,"status":0,"prompt_text":"This is a test"}'
    assert request.serialization() == target_serialization_txt


def test_deserialization_correct():
    json_str = '{"user_id":"awef","request_id":"awef","timestamp":1.0,"status":0,"prompt_text":"This is a test"}'
    request = RequestData.deserialization(json_str)
    assert request.user_id == "awef"
    assert request.request_id == "awef"
    assert request.timestamp == 1.0
    assert request.status == RequestStatus.PENDING
    assert request.prompt_text == "This is a test"


def test_after_serialize_deserialize_matches():
    user_id: str = "awef"
    request_id: str = "awef"
    timestamp: float = 1.0
    status: RequestStatus = RequestStatus.PENDING
    prompt_text: str = "This is a test"
    
    request = RequestData(
        user_id=user_id,
        request_id=request_id,
        timestamp=timestamp,
        status=status,
        prompt_text=prompt_text
    )

    serialization_txt = request.serialization()
    deserialized_request = RequestData.deserialization(serialization_txt)

    assert deserialized_request.user_id == user_id
    assert deserialized_request.request_id == request_id
    assert deserialized_request.timestamp == timestamp
    assert deserialized_request.status == status
    assert deserialized_request.prompt_text == prompt_text


def test_request_status_default_is_pending():
    user_id: str = "awef"
    request_id: str = "awef"
    timestamp: float = 1.0
    prompt_text: str = "This is a test"
    
    request = RequestData(
        user_id=user_id,
        request_id=request_id,
        timestamp=timestamp,
        prompt_text=prompt_text
    )

    assert request.status == RequestStatus.PENDING


def test_deserialization_can_auto_convert_timestamp():
    json_str = '{"user_id":"awef","request_id":"awef","timestamp":"1.0","status":0,"prompt_text":"This is a test"}'
    request = RequestData.deserialization(json_str)
    assert request.timestamp == 1.0

# Test incorrect cases
def test_incorrect_deserialization_timestamp():
    json_str = '{"user_id":"awef","request_id":"awef","timestamp":"s","status":0,"prompt_text":"This is a test"}'
    with pytest.raises(ValueError):
        RequestData.deserialization(json_str)

def test_incorrect_deserialization_status():
    json_str = '{"user_id":"awef","request_id":"awef","timestamp":1.0,"status":"WRONG_STATUS","prompt_text":"This is a test"}'
    with pytest.raises(ValueError):
        RequestData.deserialization(json_str)

def test_missing_user_id():
    json_str = '{"request_id":"awef","timestamp":1.0,"status":0,"prompt_text":"This is a test"}'
    with pytest.raises(ValueError):
        RequestData.deserialization(json_str)

def test_missing_request_id():
    json_str = '{"user_id":"awef","timestamp":1.0,"status":0,"prompt_text":"This is a test"}'
    with pytest.raises(ValueError):
        RequestData.deserialization(json_str)

def test_missing_timestamp():
    json_str = '{"user_id":"awef","request_id":"awef","status":0,"prompt_text":"This is a test"}'
    with pytest.raises(ValueError):
        RequestData.deserialization(json_str)

def test_missing_prompt_text():
    json_str = '{"user_id":"awef","request_id":"awef","timestamp":1.0,"status":0}'
    with pytest.raises(ValueError):
        RequestData.deserialization(json_str)

