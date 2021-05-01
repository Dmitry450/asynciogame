import asyncio
import json
import time

from .entity import RemoteEntity


class EntityManager:
    """Manager for remote entities"""
    registered = {}
    
    def __init__(self, game):
        self.entities = {}
        self.game = game
        self.entity_updates = None
        self.player = None
    
    def add_entity(self, typeid, entityid, position, velocity, image):
        """Create new remote entity object"""
        entity = RemoteEntity(self.game, self.registered[typeid], position, velocity)
        entity.set_image(image)
        
        self.entities[entityid] = entity
    
    def init_queue(self):
        """Initialize queue for entity updates"""
        self.entity_updates = asyncio.Queue()
    
    def del_entity(self, key):
        """Remove entity"""
        if self.entities.get(key) is None:
            return
        
        del self.entities[key]
    
    def draw(self):
        """Draw all entities"""
        for entity in self.entities.values():
            entity.draw()
        
    def update(self, dtime):
        """Update all entities"""
        if self.player is not None:
            self.player.update(dtime)
        
        for entity in self.entities.values():
            entity.update(dtime)
            
    
    async def run_entities_sync(self):
        """Synchronize entities with server"""
        while self.game.running:
            update = await self.entity_updates.get()
            
            self.entities[update["entityid"]].sync(update["position"], update["velocity"], update["image"])
