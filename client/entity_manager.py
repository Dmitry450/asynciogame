import asyncio
import json
import time

from .entity import RemoteEntity


class EntityManager:
    registered = {}
    
    def __init__(self, game):
        self.entities = {}
        self.game = game
        self.entity_updates = None
        self.player = None
    
    def add_entity(self, typeid, entityid, position, velocity):
        entity = RemoteEntity(self.game, position, velocity)
        entity.set_image(self.registered[typeid]["image"])
        
        self.entities[entityid] = entity
    
    def init_queue(self):
        self.entity_updates = asyncio.Queue()
    
    def del_entity(self, key):
        if self.entities.get(key) is None:
            return
        
        del self.entities[key]
    
    def draw(self):
        for entity in self.entities.values():
            entity.draw()
    
    async def run_entities_update(self):
        last_upd_time = time.time()
        while self.game.running:
            await asyncio.sleep(0)  # Let other tasks to run
            
            dtime = time.time() - last_upd_time
            last_upd_time += dtime
            
            if self.player is not None:
                self.player.update(dtime)
            
            for entity in self.entities.values():
                entity.update(dtime)
    
    async def run_entities_sync(self):
        while self.game.running:
            update = await self.entity_updates.get()
            
            self.entities[update["entityid"]].sync(update["position"], update["velocity"])
