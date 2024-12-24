# storage_service.py

import asyncio
import hashlib
import json
import logging
import time
import os




class StorageService:
    def __init__(
        self,
        node,
        storage_dir="storage_chunks",
        cleanup_interval=60,
        republish_interval=3600,
    ):
        self.node = node
        self.loop = asyncio.get_event_loop()
        self.cleanup_task = None
        self.republish_task = None

        # Initialize the logger instance
        self.logger = logging.getLogger(__name__)

        # Define storage directories
        self.storage_dir = storage_dir
        self.chunks_dir = os.path.join(self.storage_dir, "chunks")
        self.sub_chunks_dir = os.path.join(self.storage_dir, "sub_chunks")

        # Ensure directories exist
        os.makedirs(self.chunks_dir, exist_ok=True)
        os.makedirs(self.sub_chunks_dir, exist_ok=True)

        self.cleanup_interval = cleanup_interval
        self.republish_interval = republish_interval

        # Initialize chunk store
        self.chunk_store = {}
        self.metadata_file = os.path.join(self.storage_dir, "chunk_store_meta.json")
        self.load_chunk_store()

        self.logger.info(f"Initialized StorageService for node {self.node.node_id}")

    async def start(self):
        # Start periodic tasks with custom intervals
        self.cleanup_task = asyncio.create_task(
            self.cleanup_expired_chunks(self.cleanup_interval)
        )
        self.republish_task = asyncio.create_task(
            self.republish_chunks(self.republish_interval)
        )
        self.logger.info(f"StorageService started periodic tasks for {self.node.node_id}")

    async def stop(self):
        if self.cleanup_task:
            self.cleanup_task.cancel()
            try:
                await self.cleanup_task
            except asyncio.CancelledError:
                pass
            self.logger.info(f"StorageService cleanup task stopped for {self.node.node_id}")

        if self.republish_task:
            self.republish_task.cancel()
            try:
                await self.republish_task
            except asyncio.CancelledError:
                pass
            self.logger.info(
                f"StorageService republish task stopped for {self.node.node_id}"
            )

        self.save_chunk_store()
        self.logger.info(f"StorageService chunk_store saved for {self.node.node_id}")

    def save_chunk_store(self):
        with open(self.metadata_file, "w") as f:
            # Convert expiration times to strings for JSON serialization
            chunk_store_data = {k: str(v) for k, v in self.chunk_store.items()}
            json.dump(chunk_store_data, f)
        self.logger.debug(f"Saved chunk_store metadata: {chunk_store_data}")

    def load_chunk_store(self):
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, "r") as f:
                chunk_store_data = json.load(f)
                # Convert expiration times back to floats
                self.chunk_store = {k: float(v) for k, v in chunk_store_data.items()}
            self.logger.debug(f"Loaded chunk_store metadata: {chunk_store_data}")
        else:
            self.chunk_store = {}

    async def handle_store_file_tcp(self, message, reader, writer):
        """
        Handle an incoming STORE_FILE request over TCP.
        """
        file_hash = message.get("file_hash")
        file_size = message.get("file_size")
        ttl = message.get("ttl", 86400)
        if file_hash and file_size:
            data = await reader.readexactly(file_size)
            calculated_hash = hashlib.sha256(data).hexdigest()
            if calculated_hash == file_hash:
                self.save_chunk_to_file(file_hash, data)
                expiration_time = time.time() + ttl
                self.chunk_store[file_hash] = expiration_time
                self.logger.info(f"Stored file {file_hash} from TCP connection")
                # Send acknowledgment
                response = {"status": "OK"}
                response_data = json.dumps(response).encode("utf-8")
                writer.write(
                    len(response_data).to_bytes(4, byteorder="big") + response_data
                )
                await writer.drain()
            else:
                self.logger.warning(f"File hash mismatch for {file_hash} over TCP")
                # Send error response
                response = {"status": "ERROR", "message": "Hash mismatch"}
                response_data = json.dumps(response).encode("utf-8")
                writer.write(
                    len(response_data).to_bytes(4, byteorder="big") + response_data
                )
                await writer.drain()
        else:
            self.logger.warning("Invalid STORE_FILE message over TCP")
            # Send error response
            response = {"status": "ERROR", "message": "Invalid request"}
            response_data = json.dumps(response).encode("utf-8")
            writer.write(len(response_data).to_bytes(4, byteorder="big") + response_data)
            await writer.drain()


    async def handle_tcp_connection(self, reader, writer, initial_message_json=None):
        """
        Handle an incoming TCP connection, possibly with an initial message already read.
        """
        try:
            if initial_message_json:
                message_json = initial_message_json
            else:
                data = await reader.readexactly(4)
                message_length = int.from_bytes(data, byteorder="big")
                message_data = await reader.readexactly(message_length)
                message_json = message_data.decode("utf-8")

            message = json.loads(message_json)
            message_type = message.get("message_type")
            if message_type == "STORE_CHUNK":
                await self.handle_store_chunk_tcp(message, reader, writer)
            # Handle other storage message types...
            else:
                self.logger.warning(
                    f"Unknown storage message type over TCP: {message_type}"
                )
        except Exception as e:
            self.logger.error(
                f"Error handling TCP connection in storage service: {e}", exc_info=True
            )
            response = {"status": "ERROR", "message": str(e)}
            response_data = json.dumps(response).encode("utf-8")
            writer.write(len(response_data).to_bytes(4, byteorder="big") + response_data)
            await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()


    async def handle_retrieve_file_tcp(self, message, reader, writer):
        """
        Handle an incoming RETRIEVE_FILE request over TCP.
        """
        file_hash = message.get("file_hash")
        if file_hash:
            file_path = os.path.join(self.storage_dir, file_hash)
            if os.path.exists(file_path):
                self.logger.debug(f"Serving file {file_hash} over TCP.")
                # Read the file data
                with open(file_path, "rb") as f:
                    file_data = f.read()
                response = {
                    "status": "OK",
                    "file_size": len(file_data),
                }
                response_data = json.dumps(response).encode("utf-8")
                writer.write(
                    len(response_data).to_bytes(4, byteorder="big") + response_data
                )
                await writer.drain()
                writer.write(file_data)
                await writer.drain()
            else:
                self.logger.warning(f"Requested file {file_hash} not found.")
                response = {"status": "ERROR", "message": "File not found"}
                response_data = json.dumps(response).encode("utf-8")
                writer.write(
                    len(response_data).to_bytes(4, byteorder="big") + response_data
                )
                await writer.drain()
        else:
            self.logger.warning("Invalid RETRIEVE_FILE message over TCP.")
            response = {"status": "ERROR", "message": "Invalid request"}
            response_data = json.dumps(response).encode("utf-8")
            writer.write(len(response_data).to_bytes(4, byteorder="big") + response_data)
            await writer.drain()



    async def handle_store_chunk_tcp(self, message, reader, writer):
        """
        Handle an incoming STORE_CHUNK request over TCP.
        """
        chunk_hash = message.get("chunk_hash")
        chunk_size = message.get("chunk_size")
        ttl = message.get("ttl", 86400)
        if chunk_hash and chunk_size:
            data = await reader.readexactly(chunk_size)
            calculated_hash = hashlib.sha256(data).hexdigest()
            if calculated_hash == chunk_hash:
                self.save_chunk_to_file(chunk_hash, data)
                expiration_time = time.time() + ttl
                self.chunk_store[chunk_hash] = expiration_time
                self.logger.info(f"Stored chunk {chunk_hash} from TCP connection")
                # Send acknowledgment
                response = {"status": "OK"}
                response_data = json.dumps(response).encode("utf-8")
                writer.write(
                    len(response_data).to_bytes(4, byteorder="big") + response_data
                )
                await writer.drain()
            else:
                self.logger.warning(f"Chunk hash mismatch for {chunk_hash} over TCP")
                # Send error response
                response = {"status": "ERROR", "message": "Hash mismatch"}
                response_data = json.dumps(response).encode("utf-8")
                writer.write(
                    len(response_data).to_bytes(4, byteorder="big") + response_data
                )
                await writer.drain()
        else:
            self.logger.warning("Invalid STORE_CHUNK message over TCP")
            # Send error response
            response = {"status": "ERROR", "message": "Invalid request"}
            response_data = json.dumps(response).encode("utf-8")
            writer.write(
                len(response_data).to_bytes(4, byteorder="big") + response_data
            )
            await writer.drain()

    async def handle_retrieve_chunk_tcp(self, message, reader, writer):
        """
        Handle an incoming RETRIEVE_CHUNK request over TCP.
        """
        chunk_hash = message.get("chunk_hash")
        if (
            chunk_hash in self.chunk_store
            and time.time() < self.chunk_store[chunk_hash]
        ):
            data = self.read_chunk_from_file(chunk_hash)
            if data:
                # Send response header
                response = {"status": "OK", "chunk_size": len(data)}
                response_data = json.dumps(response).encode("utf-8")
                writer.write(
                    len(response_data).to_bytes(4, byteorder="big") + response_data
                )
                await writer.drain()
                # Send the chunk data
                writer.write(data)
                await writer.drain()
            else:
                response = {"status": "ERROR", "message": "Chunk data not found"}
                response_data = json.dumps(response).encode("utf-8")
                writer.write(
                    len(response_data).to_bytes(4, byteorder="big") + response_data
                )
                await writer.drain()
        else:
            response = {"status": "ERROR", "message": "Chunk not available"}
            response_data = json.dumps(response).encode("utf-8")
            writer.write(
                len(response_data).to_bytes(4, byteorder="big") + response_data
            )
            await writer.drain()

    # Implement other methods such as save_chunk_to_file, read_chunk_from_file, etc.

    def save_chunk_to_file(self, file_hash: str, data: bytes) -> None:
        """
        Save a chunk or file to the storage directory.
        """
        file_path = os.path.join(self.storage_dir, file_hash)
        with open(file_path, "wb") as f:
            f.write(data)
        self.logger.debug(f"Saved file {file_hash} to local storage.")

    def read_chunk_from_file(self, chunk_hash):
        file_path = os.path.join(self.chunks_dir, chunk_hash)
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                data = f.read()
            self.logger.debug(f"Read chunk {chunk_hash} from {file_path}")
            return data
        else:
            self.logger.debug(f"Chunk file {file_path} does not exist")
            return None

    async def cleanup_expired_chunks(self, interval=60):
        """
        Periodically checks for expired entries in the chunk_store and removes them.
        """
        while True:
            try:
                await asyncio.sleep(interval)
                current_time = time.time()
                expired_chunks = [
                    chunk_hash
                    for chunk_hash, exp_time in self.chunk_store.items()
                    if current_time >= exp_time
                ]
                for chunk_hash in expired_chunks:
                    self.delete_chunk(chunk_hash)
                    self.logger.debug(f"Deleted expired chunk {chunk_hash}")
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in cleanup_expired_chunks: {e}")

    def delete_chunk(self, chunk_hash):
        # Remove from chunk_store and delete the file
        if chunk_hash in self.chunk_store:
            del self.chunk_store[chunk_hash]
        file_path = os.path.join(self.chunks_dir, chunk_hash)
        if os.path.exists(file_path):
            os.remove(file_path)
            self.logger.debug(f"Deleted chunk file {chunk_hash}")

    async def republish_chunks(self, interval=3600):
        """
        Periodically republish chunks to ensure availability.
        """
        while True:
            try:
                await asyncio.sleep(interval)
                self.logger.debug("Running republish_chunks task")
                current_time = time.time()
                for chunk_hash, expiration_time in self.chunk_store.items():
                    if current_time < expiration_time:
                        # Republish the chunk
                        data = self.read_chunk_from_file(chunk_hash)
                        if data:
                            remaining_ttl = expiration_time - current_time
                            await self.store_chunk(
                                chunk_hash, data, ttl=remaining_ttl
                            )
                            self.logger.debug(
                                f"Republished chunk {chunk_hash} with TTL {remaining_ttl}"
                            )
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in republish_chunks: {e}")

    async def store_chunk(self, chunk_hash: str, chunk_data: bytes, ttl=86400) -> None:
        """
        Store a chunk using TCP connections to other nodes.
        """
        self.save_chunk_to_file(chunk_hash, chunk_data)
        expiration_time = time.time() + ttl
        self.chunk_store[chunk_hash] = expiration_time

        # Find k closest nodes to the chunk_hash
        k = self.node.routing_table.k
        closest_nodes = await self.node.find_nodes(chunk_hash)

        if not closest_nodes:
            self.logger.warning(
                f"{self.node.node_id}: No nodes available to store chunk {chunk_hash}"
            )
            return

        # Send the chunk to each node via TCP
        for node in closest_nodes:
            try:
                await self.send_chunk_over_tcp(node, chunk_hash, chunk_data, ttl)
                self.logger.debug(
                    f"Sent chunk {chunk_hash} to node {node.node_id} over TCP"
                )
            except Exception as e:
                self.logger.error(
                    f"Failed to send chunk {chunk_hash} to node {node.node_id} over TCP: {e}"
                )

    async def send_chunk_over_tcp(self, node, chunk_hash, chunk_data, ttl):
        """
        Send a chunk to a node over TCP.
        """
        reader, writer = await asyncio.open_connection(
            node.ip, node.tcp_port
        )
        try:
            message = {
                "message_type": "STORE_CHUNK",
                "chunk_hash": chunk_hash,
                "chunk_size": len(chunk_data),
                "ttl": ttl,
            }
            message_data = json.dumps(message).encode("utf-8")
            writer.write(len(message_data).to_bytes(4, byteorder="big") + message_data)
            await writer.drain()
            writer.write(chunk_data)
            await writer.drain()
            # Read acknowledgment
            data = await reader.readexactly(4)
            response_length = int.from_bytes(data, byteorder="big")
            response_data = await reader.readexactly(response_length)
            response = json.loads(response_data.decode("utf-8"))
            if response.get("status") != "OK":
                raise Exception(
                    f"Failed to store chunk on node {node.node_id}: {response.get('message')}"
                )
        finally:
            writer.close()
            await writer.wait_closed()

    async def retrieve_chunk_from_network(self, chunk_hash):
        """
        Retrieve a chunk from the network using TCP connections.
        """
        closest_nodes = await self.node.find_nodes(chunk_hash)
        for node in closest_nodes:
            try:
                chunk_data = await self.request_chunk_over_tcp(node, chunk_hash)
                if chunk_data:
                    if hashlib.sha256(chunk_data).hexdigest() == chunk_hash:
                        return chunk_data
                    else:
                        self.logger.warning(
                            f"Received corrupt chunk from node {node.node_id}"
                        )
            except Exception as e:
                self.logger.error(
                    f"Error retrieving chunk from node {node.node_id}: {e}"
                )
        return None

    async def request_chunk_over_tcp(self, node, chunk_hash):
        """
        Request a chunk from a node over TCP.
        """
        reader, writer = await asyncio.open_connection(
            node.ip, node.tcp_port
        )
        try:
            message = {"message_type": "RETRIEVE_CHUNK", "chunk_hash": chunk_hash}
            message_data = json.dumps(message).encode("utf-8")
            writer.write(len(message_data).to_bytes(4, byteorder="big") + message_data)
            await writer.drain()
            # Read response header
            data = await reader.readexactly(4)
            response_length = int.from_bytes(data, byteorder="big")
            response_data = await reader.readexactly(response_length)
            response = json.loads(response_data.decode("utf-8"))
            if response.get("status") == "OK":
                chunk_size = response.get("chunk_size")
                chunk_data = await reader.readexactly(chunk_size)
                return chunk_data
            else:
                self.logger.warning(
                    f"Failed to retrieve chunk {chunk_hash} from node {node.node_id}: {response.get('message')}"
                )
                return None
        finally:
            writer.close()
            await writer.wait_closed()

    async def store_file(self, file_hash: str, file_data: bytes, ttl=86400) -> None:
        """
        Stores a file (e.g., an image) in the distributed storage system.
        """
        # Save the file locally
        self.save_chunk_to_file(file_hash, file_data)
        expiration_time = time.time() + ttl
        self.chunk_store[file_hash] = expiration_time

        # Find k closest nodes to the file_hash
        k = self.node.routing_table.k
        closest_nodes = await self.node.find_nodes(file_hash)

        if not closest_nodes:
            self.logger.warning(
                f"{self.node.node_id}: No nodes available to store file {file_hash}"
            )
            return

        # Send the file to each node via TCP
        for node in closest_nodes:
            try:
                await self.send_file_over_tcp(node, file_hash, file_data, ttl)
                self.logger.debug(f"Sent file {file_hash} to node {node.node_id} over TCP")
            except Exception as e:
                self.logger.error(
                    f"Failed to send file {file_hash} to node {node.node_id} over TCP: {e}"
                )


    async def send_file_over_tcp(self, node, file_hash, file_data, ttl):
        """
        Send a file to a node over TCP.
        """
        reader, writer = await asyncio.open_connection(node.ip, node.tcp_port)
        try:
            message = {
                "message_type": "STORE_FILE",
                "file_hash": file_hash,
                "file_size": len(file_data),
                "ttl": ttl,
            }
            message_data = json.dumps(message).encode("utf-8")
            writer.write(len(message_data).to_bytes(4, byteorder="big") + message_data)
            await writer.drain()
            writer.write(file_data)
            await writer.drain()
            # Read acknowledgment
            data = await reader.readexactly(4)
            response_length = int.from_bytes(data, byteorder="big")
            response_data = await reader.readexactly(response_length)
            response = json.loads(response_data.decode("utf-8"))
            if response.get("status") != "OK":
                raise Exception(
                    f"Failed to store file on node {node.node_id}: {response.get('message')}"
                )
        finally:
            writer.close()
            await writer.wait_closed()

    async def retrieve_file_from_network(self, file_hash: str) -> bytes:
        """
        Retrieve a file from the network using its file hash.

        Returns the file data as bytes if found, otherwise None.
        """
        # Check if the file exists locally
        file_path = os.path.join(self.storage_dir, file_hash)
        if os.path.exists(file_path):
            self.logger.debug(f"File {file_hash} found locally.")
            with open(file_path, "rb") as f:
                return f.read()

        # Find the closest nodes to the file hash
        closest_nodes = await self.node.find_nodes(file_hash)
        if not closest_nodes:
            self.logger.warning(f"No nodes found close to file hash {file_hash}.")
            return None

        # Attempt to retrieve the file from each node
        for node in closest_nodes:
            try:
                self.logger.debug(
                    f"Attempting to retrieve file {file_hash} from node {node.node_id}."
                )
                file_data = await self.request_file_over_tcp(node, file_hash)
                if file_data:
                    # Save the file locally
                    self.save_chunk_to_file(file_hash, file_data)
                    # Update chunk store
                    expiration_time = time.time() + 86400  # Set TTL to 24 hours
                    self.chunk_store[file_hash] = expiration_time
                    self.logger.debug(
                        f"Retrieved and stored file {file_hash} from node {node.node_id}."
                    )
                    return file_data
            except Exception as e:
                self.logger.error(
                    f"Failed to retrieve file {file_hash} from node {node.node_id}: {e}"
                )

        self.logger.warning(f"Failed to retrieve file {file_hash} from any node.")
        return None


    async def request_file_over_tcp(self, node, file_hash: str) -> bytes:
        """
        Request a file from a node over TCP.

        Returns the file data as bytes if successful, otherwise None.
        """
        try:
            reader, writer = await asyncio.open_connection(node.ip, node.tcp_port)
            try:
                message = {
                    "message_type": "RETRIEVE_FILE",
                    "file_hash": file_hash,
                }
                message_data = json.dumps(message).encode("utf-8")
                writer.write(len(message_data).to_bytes(4, byteorder="big") + message_data)
                await writer.drain()

                # Read response header
                header_data = await reader.readexactly(4)
                response_length = int.from_bytes(header_data, byteorder="big")
                response_data = await reader.readexactly(response_length)
                response = json.loads(response_data.decode("utf-8"))

                if response.get("status") == "OK":
                    file_size = response.get("file_size")
                    if file_size is None:
                        raise Exception("File size not specified in response.")

                    # Read the file data
                    file_data = await reader.readexactly(file_size)
                    calculated_hash = hashlib.sha256(file_data).hexdigest()
                    if calculated_hash != file_hash:
                        raise Exception("File hash mismatch during retrieval.")
                    return file_data
                else:
                    self.logger.warning(
                        f"Node {node.node_id} responded with error: {response.get('message')}"
                    )
                    return None
            finally:
                writer.close()
                await writer.wait_closed()
        except Exception as e:
            self.logger.error(
                f"Error requesting file {file_hash} from node {node.node_id}: {e}"
            )
            return None

