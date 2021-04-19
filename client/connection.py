import asyncio
import json

from .entity_manager import EntityManager
from .local_player import LocalPlayer


class Connection:
    
    def __init__(self, game, reader, writer):
        self.game = game
        
        self.reader, self.writer = reader, writer
        
        self.disconnected = asyncio.Event()
        
        self.event_queue = asyncio.Queue()
    
    async def init(self):
        await self.send({
            "type": "client.auth",
            "name": self.game.playername,
        })
        
        response = await self.read()
        
        if not response["success"]:
            print(f"Failed to connect to server: {response['reason']}")
            
            await self.disconnect()
            
            return
        
        entity_definitions = await self.read()
        
        EntityManager.registered = {entry["id"]: entry for entry in entity_definitions["entries"]}

        self.game.local_player.set_image(EntityManager.registered["builtin:player"]["image"])
        
        for entity in (await self.read())["entries"]:
            if entity["entityid"] == self.game.playername:
                continue  # Skip ourself
            self.game.entity_manager.add_entity(**entity)
        
        asyncio.create_task(self.loop_send())
        asyncio.create_task(self.loop_read())
    
    async def loop_send(self):
        while not self.disconnected.is_set() and self.game.running:
            await self.send(await self.event_queue.get())

    async def loop_read(self):
        while not self.disconnected.is_set() and self.game.running:
            data = await self.read()
            
            if data["type"] == "client.disconnnect":
                await self.disconnect(data["reason"])

            elif data["type"] == "entity.sync":
                if data["entityid"] == self.game.playername:
                    continue  # Skip ourself
                self.game.entity_manager.entity_updates.put_nowait(data)
            
            elif data["type"] == "entity.add":
                self.game.entity_manager.add_entity(
                    typeid=data["typeid"],
                    entityid=data["entityid"],
                    position=data["position"],
                    velocity=data["velocity"])
            
            elif data["type"] == "entity.delete":
                self.game.entity_manager.del_entity(data["entityid"])

            elif data["type"] == "error":
                print(f"Error from server: {data['text']}")
                await self.disconnect(data['text'])

            else:
                print(f"Unknown data from server: {data['type']}")
                await self.disconnect(f"Unknown message type: {data['type']}")
    
    async def send(self, data):
        try:
            self.writer.write(json.dumps(data).encode())
            
            self.writer.write(b'\n')
            
            await self.writer.drain()
        except ConnectionResetError as e:
            await self.disconnect(str(e))
        
    async def disconnect(self, reason=""):
        print(f"Disconnected from server, reason: {reason}")
        
        self.writer.close()
        await self.writer.wait_closed()
        
        self.disconnected.set()
    
    async def read(self):
        try:
            return json.loads(await self.reader.readline())
        except json.JSONDecodeError:
            return {"type": "error", "text": "json decode error when receiving message"}
