import asyncio
import json

from .entity_manager import EntityManager
from .local_player import LocalPlayer


class Connection:
    """Interface for client-server connection"""
    
    def __init__(self, game, reader, writer):
        self.game = game
        
        self.reader, self.writer = reader, writer
        
        self.disconnected = asyncio.Event()
        
        self.event_queue = asyncio.Queue()
    
    async def init(self):
        """Do initial stuff when connected to server"""
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
        
        for entity in (await self.read())["entries"]:
            if entity["entityid"] == self.game.playername:
                self.game.local_player = LocalPlayer(self.game, EntityManager.registered["builtin:player"])
                self.game.entity_manager.entities[self.game.playername] = self.game.local_player
                continue  # Skip ourself
            self.game.entity_manager.add_entity(**entity)
        
        # Need to do it here so EntityManager's queue was associated with our event loop
        self.game.entity_manager.init_queue()
        
        asyncio.create_task(self.loop_send())
        asyncio.create_task(self.loop_read())
    
    async def loop_send(self):
        """Send all client events while connected"""
        while not self.disconnected.is_set() and self.game.running:
            await self.send(await self.event_queue.get())

    async def loop_read(self):
        """Read and process all server events while connected"""
        while not self.disconnected.is_set() and self.game.running:
            data = await self.read()
            
            if data["type"] == "client.disconnect":
                await self.disconnect(data["reason"])

            elif data["type"] == "entity.sync":
                if data["entityid"] == self.game.playername:
                    self.game.local_player.sync(animation=data.get("animation"))
                    continue  # Skip ourself
                self.game.entity_manager.entity_updates.put_nowait(data)
            
            elif data["type"] == "entity.add":
                self.game.entity_manager.add_entity(
                    typeid=data["typeid"],
                    entityid=data["entityid"],
                    position=data["position"],
                    velocity=data["velocity"],
                    animation=data.get("animation"))
            
            elif data["type"] == "entity.delete":
                self.game.entity_manager.del_entity(data["entityid"])
            
            elif data["type"] == "sound.play":
                sound = data["sound"]
                
                if self.game.playername in sound.get("exclude_players", []):
                    continue
                
                if sound["type"] in ("attached_to_position", "attached_to_entity"):
                    if sound["type"] == "attached_to_entity":
                        sound["position"] = self.game.entity_manager.entities[sound["entity"]].position
                    
                    sound["type"] = "attached"

                self.game.audio.play_sound(sound)
            
            elif data["type"] == "background.set_color":
                self.game.graphics.set_bg_color(data["color"])
            
            elif data["type"] == "background.set_image":
                self.game.graphics.set_bg_image(data["name"])
            
            elif data["type"] == "ground.set":
                self.game.graphics.set_ground(
                    surfdef=data.get("surfdef"),
                    image_name=data.get("image_name"),
                    position=data.get("position", (0, 0)),
                )

            elif data["type"] == "error":
                print(f"Error from server: {data['text']}")
                await self.disconnect(data['text'])

            else:
                print(f"Unknown data from server: {data['type']}")
                await self.disconnect(f"Unknown message type: {data['type']}")
    
    async def send(self, data):
        """Send json data to server"""
        try:
            self.writer.write(json.dumps(data).encode())
            
            self.writer.write(b'\n')
            
            await self.writer.drain()
        except ConnectionResetError as e:
            await self.disconnect(str(e))
        
    async def disconnect(self, reason=""):
        """Drop connection"""
        print(f"Disconnected from server, reason: {reason}")
        
        self.writer.close()
        await self.writer.wait_closed()
        
        self.disconnected.set()
    
    async def read(self):
        """Read json data from server"""
        try:
            return json.loads(await self.reader.readline())
        except json.JSONDecodeError:
            return {"type": "error", "text": "json decode error when receiving message"}
