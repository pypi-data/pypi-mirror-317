import pytest
from unittest.mock import patch, MagicMock
from kitchenai_py.client import KitchenAIWrapper

@pytest.fixture
def mock_api():
    with patch('kitchenai_py.client.ApiClient'), patch('kitchenai_py.client.DefaultApi') as MockDefaultApi:
        mock_instance = MockDefaultApi.return_value
        mock_instance.kitchenai_core_api_default = MagicMock()
        mock_instance.kitchenai_core_api_query = MagicMock()
        # Add other necessary attributes here
        yield mock_instance

@pytest.fixture
def wrapper():
    return KitchenAIWrapper()

def test_health_check(wrapper, mock_api):
    mock_api.kitchenai_core_api_default.return_value = None
    result = wrapper.health_check()
    assert result == "API is healthy!"

def test_health_check_failure(wrapper, mock_api):
    mock_api.kitchenai_core_api_default.side_effect = Exception("API error")
    result = wrapper.health_check()
    assert "Failed to reach API" in result

def test_run_query(wrapper, mock_api):
    mock_api.kitchenai_core_api_query.return_value = "query result"
    result, _ = wrapper.run_query("test_label", "test_query")
    assert "executed successfully" in result

def test_run_query_failure(wrapper, mock_api):
    mock_api.kitchenai_core_api_query.side_effect = Exception("Query error")
    result, _ = wrapper.run_query("test_label", "test_query")
    assert "Error running query" in result

# @patch('kitchenai_py.client.requests.post')
# @patch('kitchenai_py.client.sseclient.SSEClient')
# def test_run_query_stream(MockSSEClient, MockRequestsPost, wrapper):
#     # Mock the SSE client and requests post
#     mock_event = MagicMock()
#     mock_event.event = "message"
#     mock_event.data = "stream data"
#     MockSSEClient.return_value.events.return_value = [mock_event]
#     MockRequestsPost.return_value.status_code = 200
#     MockRequestsPost.return_value.json.return_value = {"status": "success"}

#     # Run the streaming query
#     result, _ = wrapper.run_query("test_label", "test_query", stream=True)
#     assert "executed successfully" in result

def test_create_file(wrapper, mock_api):
    mock_api.kitchenai_core_api_file_upload.return_value = "file response"
    result, _ = wrapper.create_file("test_path", "test_name", "test_label")
    assert "created successfully" in result

def test_create_file_failure(wrapper, mock_api):
    mock_api.kitchenai_core_api_file_upload.side_effect = Exception("File error")
    result, _ = wrapper.create_file("test_path", "test_name", "test_label")
    assert "Error creating file" in result

def test_read_file(wrapper, mock_api):
    mock_api.kitchenai_core_api_file_get.return_value = "file data"
    result, _ = wrapper.read_file(1)
    assert "retrieved successfully" in result

def test_read_file_failure(wrapper, mock_api):
    mock_api.kitchenai_core_api_file_get.side_effect = Exception("Read error")
    result, _ = wrapper.read_file(1)
    assert "Error reading file" in result

def test_update_file(wrapper, mock_api):
    mock_api.kitchenai_core_api_file_update.return_value = "update response"
    result, _ = wrapper.update_file(1, "new_name")
    assert "updated successfully" in result

def test_update_file_failure(wrapper, mock_api):
    mock_api.kitchenai_core_api_file_update.side_effect = Exception("Update error")
    result, _ = wrapper.update_file(1, "new_name")
    assert "Error updating file" in result

def test_delete_file(wrapper, mock_api):
    mock_api.kitchenai_core_api_file_delete.return_value = None
    result = wrapper.delete_file(1)
    assert "deleted successfully" in result

def test_delete_file_failure(wrapper, mock_api):
    mock_api.kitchenai_core_api_file_delete.side_effect = Exception("Delete error")
    result = wrapper.delete_file(1)
    assert "Error deleting file" in result

def test_list_files(wrapper, mock_api):
    mock_api.kitchenai_core_api_files_get.return_value = ["file1", "file2"]
    result = wrapper.list_files()
    assert result == ["file1", "file2"]

def test_list_files_empty(wrapper, mock_api):
    mock_api.kitchenai_core_api_files_get.return_value = []
    result = wrapper.list_files()
    assert result == "No files found."

def test_get_all_embeds(wrapper, mock_api):
    mock_api.kitchenai_core_api_embeds_get.return_value = ["embed1", "embed2"]
    result = wrapper.get_all_embeds()
    assert result == ["embed1", "embed2"]

def test_get_all_embeds_empty(wrapper, mock_api):
    mock_api.kitchenai_core_api_embeds_get.return_value = []
    result = wrapper.get_all_embeds()
    assert result == "No embeds found."

def test_create_embed(wrapper, mock_api):
    mock_api.kitchenai_core_api_embed_create.return_value = "embed response"
    result, _ = wrapper.create_embed("text", "label")
    assert "created successfully" in result

def test_create_embed_failure(wrapper, mock_api):
    mock_api.kitchenai_core_api_embed_create.side_effect = Exception("Embed error")
    result, _ = wrapper.create_embed("text", "label")
    assert "Error creating embed" in result

def test_delete_embed(wrapper, mock_api):
    mock_api.kitchenai_core_api_embed_delete.return_value = None
    result = wrapper.delete_embed(1)
    assert "deleted successfully" in result

def test_delete_embed_failure(wrapper, mock_api):
    mock_api.kitchenai_core_api_embed_delete.side_effect = Exception("Delete error")
    result = wrapper.delete_embed(1)
    assert "Error deleting embed" in result

def test_list_labels(wrapper, mock_api):
    mock_api.kitchenai_core_api_labels.return_value = ["label1", "label2"]
    result = wrapper.list_labels()
    assert result == ["label1", "label2"]

def test_list_labels_empty(wrapper, mock_api):
    mock_api.kitchenai_core_api_labels.return_value = []
    result = wrapper.list_labels()
    assert result == "No labels found."