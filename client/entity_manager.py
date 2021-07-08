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
    
    def add_entity(self, typeid, entityid, position, velocity, animation=None):
        """Create new remote entity object"""
        entity = RemoteEntity(self.game, self.registered[typeid], position, velocity)
        
        if animation is not None:
            entity.sprite.set_animation(animation)
        
        self.entities[entityid] = entity
    
    def init_queue(self):
        """Initialize queue for entity updates"""
        self.entity_updates = asyncio.Queue()
    
    def del_entity(self, key):
        """Remove entity"""
        if self.entities.get(key) is None:
            return
        
        del self.entities[key]
        
    def update(self, dtime):
        """Update all entities"""
        for entity in self.entities.values():
            entity.update(dtime)
    
    async def run_entities_sync(self):
        """Synchronize entities with server"""
        while self.game.running:
            update = await self.entity_updates.get()
            
            self.entities[update["entityid"]].sync(update["position"], update["velocity"], update.get("animation"))
