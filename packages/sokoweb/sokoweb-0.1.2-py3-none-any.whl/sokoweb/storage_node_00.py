# storage_node.py
import asyncio
from .node import Node
from .storage_service import StorageService
from .messages import Message
import logging
import json

logger = logging.getLogger(__name__)


class StorageNode(Node):
    def __init__(
        self,
        ip,
        port,
        key_pair=None,
        node_id=None,
        advertise_ip=None,
        alpha=3,
        k=20,
        credit_manager=None,
        storage_dir="storage_chunks",
        cleanup_interval=60,
        republish_interval=3600,
        tcp_port=None,  # Add tcp_port parameter
    ):
        super().__init__(
            ip=ip,
            port=port,
            key_pair=key_pair,
            node_id=node_id,
            advertise_ip=advertise_ip,
            alpha=alpha,
            k=k,
            credit_manager=credit_manager,
        )
        self.tcp_port = tcp_port or (self.port + 500)  # Default TCP port
        self.tcp_server = None
        self.storage_service = StorageService(
            self,
            storage_dir=storage_dir,
            cleanup_interval=cleanup_interval,
            republish_interval=republish_interval,
        )
        logger.info(f"Initialized StorageNode at {self.ip}:{self.port} with TCP port {self.tcp_port}")

    async def start(self, bootstrap_nodes=None):
        # Start the TCP server first
        await self.start_tcp_server()

        # Start the storage service
        await self.storage_service.start()

        # Now call super().start()
        await super().start(bootstrap_nodes=bootstrap_nodes)



    async def stop(self):
        # Stop the storage service tasks
        await self.storage_service.stop()
        # Stop the TCP server
        if self.tcp_server:
            self.tcp_server.close()
            await self.tcp_server.wait_closed()
            logger.info(f"TCP server stopped for node {self.node_id}")

        # Stop the underlying node
        await super().stop()

    async def start_tcp_server(self):
        self.tcp_server = await asyncio.start_server(
            self.handle_tcp_connection, self.bind_ip, self.tcp_port
        )
        self.logger.info(f"TCP server started on {self.bind_ip}:{self.tcp_port}")




    async def handle_tcp_connection(self, reader, writer):
        try:
            addr = writer.get_extra_info("peername")
            self.logger.debug(f"Accepted TCP connection from {addr}")

            # Read the length of the incoming message
            data = await reader.readexactly(4)
            message_length = int.from_bytes(data, byteorder="big")

            # Read the message
            message_data = await reader.readexactly(message_length)
            message_json = message_data.decode("utf-8")
            message = Message.from_json(message_json)

            # Handle the message using the existing message handler
            await self.handle_message(message, addr)

            # Send acknowledgment
            response = {"status": "OK"}
            response_data = json.dumps(response).encode("utf-8")
            writer.write(len(response_data).to_bytes(4, byteorder="big") + response_data)
            await writer.drain()

        except Exception as e:
            self.logger.error(f"Error handling TCP connection: {e}", exc_info=True)
            # Optionally send an error response
            response = {"status": "ERROR", "message": str(e)}
            response_data = json.dumps(response).encode("utf-8")
            writer.write(len(response_data).to_bytes(4, byteorder="big") + response_data)
            await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()
