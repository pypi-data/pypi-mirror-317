import grpc
from AINetworkDagSdk.proto.ai_network_dag_pb2 import Publication, Subscription, Content, ContentRequest
from AINetworkDagSdk.proto.ai_network_dag_pb2_grpc import AINetworkMerkleDAGStub
import os
from concurrent import futures

class AINetworkDagSdk:
    def __init__(self, server_address):
        self.channel = grpc.insecure_channel(server_address)
        self.stub = AINetworkMerkleDAGStub(self.channel)

    def add(self, message, data, children):
        request = Content(message=message, data=data, children=children)
        response = self.stub.add(request)
        print(f"Add response: CID = {response.cid}")
        return response.cid

    def get(self, cid):
        request = ContentRequest(cid=cid)
        response = self.stub.get(request)
        print(f"Get response: Message = {response.message}, Data Length = {len(response.data)}")
        return response

    def publish(self, topic, instruction):
        request = Publication(topic=topic, instruction=instruction)
        response = self.stub.publish(request)
        print(f"Publish response: {response.success}")

    def subscribe(self, topic, node_pk, on_message_callback=None):
        request = Subscription(topic=topic, node_pk=node_pk)
        stream = self.stub.subscribe(request)
        print(f"Successfully subscribed to topic: {topic} for {node_pk}")
        try:
            for response in stream:
                print(f"Received message on topic '{topic}': {response}")
                if on_message_callback:
                    on_message_callback(response)
                    
        except grpc.RpcError as e:
            print(f"Error during subscription: {e.details()}")

    def close(self):
        self.channel.close()

    def uploadFile(self, file_path, chunk_size = 4 * 1024 * 1023):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "rb") as file:
            file_data = file.read()

        # Split data into chunks
        chunks = [file_data[i:i + chunk_size] for i in range(0, len(file_data), chunk_size)]
        chunk_cids = []

        print(f"Uploading file '{file_path}' in {len(chunks)} chunks...")

        for index, chunk in enumerate(chunks):
            chunk_cid = self.add(f"chunk_{index}", chunk, [])
            print(f"Chunk {index + 1}/{len(chunks)} uploaded with CID: {chunk_cid}")
            chunk_cids.append(chunk_cid)

        # Add root node linking all chunks
        root_message = os.path.basename(file_path)
        root_cid = self.add(root_message, b"", chunk_cids)
        print(f"Root node uploaded with CID: {root_cid}")
        return root_cid

    def downloadFile(self, root_cid, output_path=None):
        # Retrieve the root node
        root_response = self.get(root_cid)

        if not root_response.children:
            raise ValueError("Root node has no children (no chunks linked).")

        chunks = []
        print(f"Downloading {len(root_response.children)} chunks for file '{root_response.message}'...")

        for index, child_cid in enumerate(root_response.children):
            chunk_response = self.get(child_cid)
            print(f"Retrieved chunk {index + 1}/{len(root_response.children)}")
            chunks.append(chunk_response.data)

        # Reconstruct the file
        reconstructed_data = b"".join(chunks)

        # If output_path is not provided, use the original file name
        if output_path is None:
            output_path = root_response.message

        with open(output_path, "wb") as output_file:
            output_file.write(reconstructed_data)

        print(f"File reconstructed and saved to: {output_path}")
        
        return output_path

if __name__ == "__main__":
    server_address = "localhost:50051"
    ai_network_dag_sdk = AINetworkDagSdk(server_address)

    try:
        # Add and Get examples
        cid = ai_network_dag_sdk.add("Test Message", None, [])
        ai_network_dag_sdk.get(cid)

        # Publish and Subscribe examples
        ai_network_dag_sdk.subscribe("test_topic")
        ai_network_dag_sdk.publish("test_topic", "Hello, gRPC!")

        # Add Data example
        test_file_path = "test_data.txt"
        with open(test_file_path, "w") as f:
            f.write("This is some test data.")
        with open(test_file_path, "rb") as f:
            file_data = f.read()
        ai_network_dag_sdk.add("Test File", file_data, [])

        # Upload File example
        large_file_path = "large_test_file.txt"
        with open(large_file_path, "w") as f:
            f.write("A" * (10 * 1024 * 1024))  # 10MB file
        # chunk_size = 4 * 1024 * 1023  # 4MB chunks
        root_cid = ai_network_dag_sdk.uploadFile(large_file_path)

        # Download File example
        download_path = "downloaded_large_test_file.txt"
        ai_network_dag_sdk.downloadFile(root_cid, download_path)

    finally:
        ai_network_dag_sdk.close()
