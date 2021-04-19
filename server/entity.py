from pygame.math import Vector2

from .entity_manager import EntityManager


class Entity:
    definition = {
        "id": "builtin:entity_base",
        "image": None,
    }
    
    def __init__(self, position=(0, 0), velocity=(0, 0)):
        self.position = Vector2(position)
        self.velocity = Vector2(velocity)
    
    def update(self, dtime):
        self.position += self.velocity * dtime
    
    def set_position(self, position=(0, 0)):
        self.position = Vector2(position)
    
    def set_velocity(self, velocity=(0, 0)):
        self.velocity = Vector2(velocity)

    def get_position(self):
        return self.position
    
    def get_velocity(self):
        return self.velocity
    
    @classmethod
    def register(cls):
        EntityManager.registered[cls.definition["id"]] = cls
    
    
