import asyncio

from .player import Player
from .enemy import Enemy
from .client import Client
from .entity_manager import EntityManager


class Game:
    config = {
        "entity.updtime": 1/20,
        "entity.synctime": 0.05,
    }
    
    def __init__(self):
        self.clients = {}
        
        Player.register()
        Enemy.register()
        
        self.entity_manager = EntityManager(self)
        self.entity_manager.add_entity(Enemy())
        self.running = True

    def on_client_connected(self, reader, writer):
        client = Client(self, reader, writer)
        asyncio.create_task(client.init())

    def add_player(self, name):
        player = Player(name)
        
        self.entity_manager.add_entity(player, name)
        
        return player

    def has_player(self, name):
        return self.entity_manager.entities.get(name) is not None
    
    def push_event(self, event):
        for client in self.clients.values():
            client.event_queue.put_nowait(event)
    
    def disconnect_player(self, name):
        self.entity_manager.del_entity(name)
        
        if name in self.clients.keys():
            del self.clients[name]
        
    async def main(self):
        asyncio.create_task(self.entity_manager.run_entities_update())
        asyncio.create_task(self.entity_manager.run_entities_sync())
        
        server = await asyncio.start_server(
            self.on_client_connected, '127.0.0.1', 43210)
        
        async with server:
            await server.serve_forever()
