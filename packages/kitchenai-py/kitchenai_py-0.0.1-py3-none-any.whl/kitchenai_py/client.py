# kitchenai_wrapper.py

import json
from kitchenai_python_sdk.api_client import ApiClient
from kitchenai_python_sdk.api.default_api import DefaultApi
from kitchenai_python_sdk.configuration import Configuration
from kitchenai_python_sdk.models.embed_schema import EmbedSchema
from kitchenai_python_sdk.models.file_object_schema import FileObjectSchema
from kitchenai_python_sdk.models.query_schema import QuerySchema
import uuid
import requests
import sseclient
import threading

class KitchenAIWrapper:
    def __init__(self, host="http://localhost:8001"):
        self.BASE_URL = host
        self.configuration = Configuration(host=host)

    def health_check(self):
        """Check the health of the API."""
        with ApiClient(self.configuration) as api_client:
            api_instance = DefaultApi(api_client)
            try:
                api_instance.kitchenai_core_api_default()
                return "API is healthy!"
            except Exception as e:
                return f"Failed to reach API: {e}"

    def run_query(self, label, query, metadata="", stream=False):
        """Run a query using the Query Handler with optional streaming."""
        metadata_p = json.loads(metadata) if metadata else {}
        schema = QuerySchema(query=query, metadata=metadata_p)

        if stream:
            # Generate a unique stream_id
            stream_id = str(uuid.uuid4())
            print(f"Generated stream_id: {stream_id}")

            # Connect to the stream in a separate thread
            sse_thread = threading.Thread(target=self.connect_to_stream, args=(stream_id,))
            sse_thread.start()

            # Send the query request with streaming enabled
            self.send_query_request(label, query, stream_id)

            # Wait for the SSE thread to finish (optional)
            sse_thread.join()
        else:
            with ApiClient(self.configuration) as api_client:
                api_instance = DefaultApi(api_client)
                try:
                    result = api_instance.kitchenai_core_api_query(label, schema)
                    return f"Query '{label}' executed successfully!", result
                except Exception as e:
                    return f"Error running query: {e}"

    def connect_to_stream(self, stream_id):
        """Connect to the stream endpoint and listen for events."""
        sse_url = f"{self.BASE_URL}/events/?channel={stream_id}"
        print(f"Connecting to SSE stream at {sse_url}...")

        try:
            with requests.get(sse_url, stream=True) as response:
                if response.status_code != 200:
                    print(f"Failed to connect to SSE stream: {response.status_code}")
                    return

                # Listen for events using SSEClient
                client = sseclient.SSEClient(response)
                for event in client.events():
                    print(f"Received event: {event.event}, data: {event.data}")
        except Exception as e:
            print(f"Error connecting to SSE: {e}")

    def send_query_request(self, label, query, stream_id):
        """Send a POST request to the query endpoint with the provided stream_id."""
        query_url = f"{self.BASE_URL}/query/{label}/"
        payload = {
            "query": query,
            "stream": True,
            "stream_id": stream_id,
        }
        print(f"Sending query to {query_url} with stream_id: {stream_id}...")

        try:
            response = requests.post(query_url, json=payload)
            if response.status_code == 200:
                print("Query initiated successfully:", response.json())
            else:
                print(f"Query failed: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Error sending query request: {e}")

    def run_agent(self, label, query, metadata=""):
        """Run an agent using the Agent Handler."""
        metadata_p = json.loads(metadata) if metadata else {}
        schema = QuerySchema(query=query, metadata=metadata_p)
        try:
            self.api_instance.kitchenai_contrib_kitchenai_sdk_kitchenai_agent_handler(label, schema)
            return f"Agent '{label}' executed successfully!"
        except Exception as e:
            return f"Error running agent: {e}"

    def create_file(self, file_path, name, ingest_label, metadata=""):
        """Create a file."""
        metadata_p = json.loads(metadata) if metadata else {}
        with open(file_path, 'rb') as file:
            file_content = file.read()
            with ApiClient(self.configuration) as api_client:
                api_instance = DefaultApi(api_client)
                schema = FileObjectSchema(name=name, ingest_label=ingest_label, metadata=metadata_p)
                try:
                    api_response = api_instance.kitchenai_core_api_file_upload(file=(name, file_content), data=schema)
                    return f"File '{name}' created successfully!", api_response
                except Exception as e:
                    return f"Error creating file: {e}"

    def read_file(self, file_id):
        """Read a file by ID."""
        with ApiClient(self.configuration) as api_client:
            api_instance = DefaultApi(api_client)
            try:
                file_data = api_instance.kitchenai_core_api_file_get(file_id)
                return f"File ID '{file_id}' retrieved successfully!", file_data
            except Exception as e:
                return f"Error reading file: {e}"

    def update_file(self, file_id, name=None, ingest_label=None, metadata=""):
        """Update a file by ID."""
        metadata_p = json.loads(metadata) if metadata else {}
        schema = FileObjectSchema(name=name, ingest_label=ingest_label, metadata=metadata_p)
        with ApiClient(self.configuration) as api_client:
            api_instance = DefaultApi(api_client)
            try:
                api_response = api_instance.kitchenai_core_api_file_update(file_id, data=schema)
                return f"File ID '{file_id}' updated successfully!", api_response
            except Exception as e:
                return f"Error updating file: {e}"

    def delete_file(self, file_id):
        """Delete a file by ID."""
        with ApiClient(self.configuration) as api_client:
            api_instance = DefaultApi(api_client)
            try:
                api_instance.kitchenai_core_api_file_delete(file_id)
                return f"File ID '{file_id}' deleted successfully!"
            except Exception as e:
                return f"Error deleting file: {e}"

    def list_files(self):
        """List all files."""
        with ApiClient(self.configuration) as api_client:
            api_instance = DefaultApi(api_client)
            try:
                files = api_instance.kitchenai_core_api_files_get()
                return files if files else "No files found."
            except Exception as e:
                return f"Error fetching files: {e}"

    def get_all_embeds(self):
        """Get all embeds."""
        with ApiClient(self.configuration) as api_client:
            api_instance = DefaultApi(api_client)
            try:
                embeds = api_instance.kitchenai_core_api_embeds_get()
                return embeds if embeds else "No embeds found."
            except Exception as e:
                return f"Error fetching embeds: {e}"

    def create_embed(self, text, ingest_label, metadata=""):
        """Create an embed."""
        metadata_p = json.loads(metadata) if metadata else {}
        schema = EmbedSchema(text=text, ingest_label=ingest_label, metadata=metadata_p)
        with ApiClient(self.configuration) as api_client:
            api_instance = DefaultApi(api_client)
            try:
                response = api_instance.kitchenai_core_api_embed_create(schema)
                return f"Embed created successfully!", response
            except Exception as e:
                return f"Error creating embed: {e}"

    def delete_embed(self, embed_id):
        """Delete an embed by ID."""
        with ApiClient(self.configuration) as api_client:
            api_instance = DefaultApi(api_client)
            try:
                api_instance.kitchenai_core_api_embed_delete(embed_id)
                return f"Embed ID '{embed_id}' deleted successfully!"
            except Exception as e:
                return f"Error deleting embed: {e}"

    def list_labels(self):
        """List all custom kitchenai labels."""
        with ApiClient(self.configuration) as api_client:
            api_instance = DefaultApi(api_client)
            try:
                labels = api_instance.kitchenai_core_api_labels()
                return labels if labels else "No labels found."
            except Exception as e:
                return f"Error fetching labels: {e}"