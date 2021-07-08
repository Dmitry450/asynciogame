import asyncio

from .player import Player
from .client import Client
from .entity_manager import EntityManager
from .addons import load_addons


class Game:
    """Main game object"""
    config = {
        "entity.updtime": 1/20,
        "entity.synctime": 0.05,
    }
    
    def __init__(self):
        self.clients = {}
        
        Player.register()
        
        self.entity_manager = EntityManager(self)
        self.running = True
        
        load_addons(self)  # TODO - make config to enable/disable addons

    def on_client_connected(self, reader, writer):
        """Callback for asyncio.start_server"""
        client = Client(self, reader, writer)
        asyncio.create_task(client.init())

    def add_player(self, name):
        """Create new player entity"""
        player = Player()
        
        self.entity_manager.add_entity(player, name)
        
        return player

    def has_player(self, name):
        """Check is there already player on server with given name"""
        return self.entity_manager.entities.get(name) is not None
    
    def push_event(self, event):
        """Send event to all clients"""
        for client in self.clients.values():
            client.event_queue.put_nowait(event)
    
    def disconnect_player(self, name):
        """Remove player entity"""
        self.entity_manager.del_entity(name)
        
        if name in self.clients.keys():
            del self.clients[name]
        
    async def main(self):
        """Run all asyncio tasks and serve forever"""
        asyncio.create_task(self.entity_manager.run_entities_update())
        asyncio.create_task(self.entity_manager.run_entities_sync())
        
        server = await asyncio.start_server(
            self.on_client_connected, '127.0.0.1', 43210)
        
        async with server:
            await server.serve_forever()
