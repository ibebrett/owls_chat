import asyncio
import time

MAX_NAME_LENGTH = 100
MAX_MESSAGE_LENGTH = 1000
MAX_LINE_LENGTH = 2048

class Client:
    def __init__(self, name, writer, reader):
        self.name = name
        self.writer = writer
        self.reader = reader
        self.last_message = None
        self.out_messages = []

class Server:
    def __init__(self):
        self.clients = {}
        
    async def handle_client(self, client):
        pass

    async def start(self, host_address, host_port):
        server = await asyncio.start_server(
            self.handle_client,
            host_address,
            host_port
        )

        async with server:
            await server.serve_forever()

    async def get_line(self, reader) -> str:
        res = (await reader.readline()).decode()
        return res

    async def write_line(self, writer, line: str):
        return writer.write(f'{line}\n'.encode())


    async def broadcast(self, message: str):
        for c in self.clients.values():
            await self.write_line(c.writer, message)

    async def handle_client(self, reader, writer):
        name = None
        try:
            await self.write_line(writer, "Welcome to owl chat, enter your name")
            name = (await self.get_line(reader)).strip()

            if len(name) > 100 or not name or name.startswith("/"):
                await self.write_line(writer, "bad name")
                return  # break if we don't like the name
        
            if name in self.clients:
                await self.write_line(writer, "Someone with that name is already here")
                return

            # double check as we have awaited since then
            if name in self.clients:
                return

            await self.write_line(writer, f"Welome {name}")
            client = Client(
                    name=name,
                    writer=writer,
                    reader=reader,
            )

            self.clients[name] = client

            while True:
                msg = (await self.get_line(reader)).strip()

                # handle commands, lets say they all start
                # with slash
                if msg == "/rollcall":
                    all_clients = ", ".join(self.clients.keys())
                    await self.broadcast(f'/rollcall: {all_clients}')
                else:
                    await self.broadcast(f'{name}: "{msg}"')

        finally:
            if name in self.clients:
                del self.clients[name]
            writer.close()
            await writer.wait_closed()


async def main_async():
    server = Server()
    await server.start('0.0.0.0', 8080)

def main():
    asyncio.run(main_async())
