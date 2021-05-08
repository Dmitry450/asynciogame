import json
import asyncio

from .entity_manager import EntityManager


class Client:
    """Interface to server-client connection"""
    
    def __init__(self, game, reader, writer):
        self.game = game
        
        self.reader, self.writer = reader, writer
        
        self.entity = None
        
        self.name = writer.get_extra_info('peername')[0]
        
        self.connected = True
        
        self.event_queue = asyncio.Queue()

    async def init(self):
        """Do initial stuff when client connected"""
        request = await self.read()
        
        if self.game.has_player(request['name']):
            await self.send({
                "type": "client.auth",
                "success": False,
                "reason": f"Player '{request['name']}' already exists",
            })
            
            await self.disconnect(f"Player '{request['name']}' already exists")
            
            return
        
        self.entity = self.game.add_player(request['name'])
        self.name = request['name']
        
        await self.send({
            "type": "client.auth",
            "success": True,
        })
        
        await self.send({
            "type": "definitions.entities",
            "entries": [entity.definition for entity in EntityManager.registered.values()],
        })
        
        await self.send({
            "type": "entity.list",
            "entries": self.game.entity_manager.get_entities(),
        })
        
        self.game.clients[request['name']] = self
        
        print(f"{self.name} connected")
        
        asyncio.create_task(self.loop_send())
        asyncio.create_task(self.loop_read())
    
    async def loop_send(self):
        """Send all server events while connected"""
        while self.connected and self.game.running:
            await self.send(await self.event_queue.get())

    async def loop_read(self):
        """Read and process all client events while connected"""
        while self.connected and self.game.running:
            data = await self.read()
            
            if data["type"] == "client.disconnect":
                await self.disconnect(data["reason"])
            elif data["type"] == "player.sync":
                self.entity.set_position(data["position"])
                self.entity.set_velocity(data["velocity"])
                self.entity.set_mouse(data["mouse"])
            elif data["type"] == "error":
                await self.disconnect(data['text'])
            else:
                print(f"Unknown data from {self.name}: {data['type']}")
                await self.disconnect(f"Unknown message type: {data['type']}")

    async def send(self, data):
        """Send json data to client"""
        if not self.connected:
            return

        try:
            self.writer.write(json.dumps(data).encode())
            
            self.writer.write(b'\n')
            
            await self.writer.drain()
        except ConnectionResetError as e:
            await self.disconnect(str(e))
        
    async def disconnect(self, reason=""):
        """Drop connection"""
        print(f"{self.name} disconnected, reason: {reason}")
        
        self.writer.close()
        
        try:
            await self.writer.wait_closed()
        except ConnectionResetError:
            pass
        
        self.connected = False
        
        if self.entity is not None:
            self.game.disconnect_player(self.name)

    async def read(self):
        """Read json data from client"""
        try:
            data = await self.reader.readline()
            
            if not data:
                return {"type": "error", "text": "no data from client"}
            
            return json.loads(data)
        except json.JSONDecodeError:
            return {"type": "error", "text": "client sent incorrect message"}
        except ConnectionResetError:
            return {"type": "error", "text": "connection reset by peer"}
