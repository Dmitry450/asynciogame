from pygame.math import Vector2

from .entity_manager import EntityManager


class Entity:
    """A server-side entity"""
    definition = {
        "id": "builtin:entity_base",
        "image": None,
    }
    
    def __init__(self, position=(0, 0), velocity=(0, 0)):
        self.position = Vector2(position)
        self.velocity = Vector2(velocity)
    
    def update(self, dtime):
        """Update entity"""
        self.position += self.velocity * dtime
    
    def set_position(self, position=(0, 0)):
        """Set entity position"""
        self.position = Vector2(position)
    
    def set_velocity(self, velocity=(0, 0)):
        """Set entity velocity"""
        self.velocity = Vector2(velocity)

    def get_position(self):
        """Get entity position"""
        return self.position
    
    def get_velocity(self):
        """Get entity velocity"""
        return self.velocity
    
    @classmethod
    def register(cls):
        """Register entity definition"""
        EntityManager.registered[cls.definition["id"]] = cls
    
    
