import uuid
import json
import asyncio
import time


class EntityManager:
    """Manager for server-side entities"""
    registered = {}
    
    def __init__(self, game):
        self.entities = {}
        self.game = game
    
    def add_entity(self, entity, key=None):
        """Add entity. If key is None, generate random uuid"""
        if key is None:
            key = str(uuid.uuid1())
        
        self.entities[key] = entity
        
        self.game.push_event({
            "type": "entity.add",
            "entityid": key,
            "typeid": entity.definition["id"],
            "position": tuple(entity.get_position()),
            "velocity": tuple(entity.get_velocity()),
        })
    
    def get_entities(self):
        """Get json entities to send them to client"""
        entities = []
        
        for key in self.entities.keys():
            entities.append({
                "entityid": key,
                "typeid": self.entities[key].definition["id"],
                "position": tuple(self.entities[key].get_position()),
                "velocity": tuple(self.entities[key].get_velocity()),
            })
        
        return entities
    
    def del_entity(self, key):
        """Remove entity"""
        if self.entities.get(key) is None:
            return
        
        del self.entities[key]
        
        self.game.push_event({
            "type": "entity.delete",
            "entityid": key,
        })

    async def run_entities_update(self):
        """Update entities"""
        last_upd_time = time.time()

        while self.game.running:
            dtime = time.time() - last_upd_time
            last_upd_time += dtime
            
            await asyncio.sleep(self.game.config['entity.updtime'])
            
            for entity in self.entities.values():
                entity.update(dtime)
    
    async def run_entities_sync(self):
        """Synchronize entities with clients"""
        while self.game.running:
            await asyncio.sleep(self.game.config['entity.synctime'])
            
            for key in self.entities.keys():
                self.game.push_event({
                    "type": "entity.sync",
                    "entityid": key,
                    "position": tuple(self.entities[key].get_position()),
                    "velocity": tuple(self.entities[key].get_velocity()),
                })
