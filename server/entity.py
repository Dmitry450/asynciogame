from pygame.math import Vector2
from pygame import Rect

from .entity_manager import EntityManager


class Entity:
    """A server-side entity"""
    definition = {
        "id": "builtin:entity_base",
        "images": {},
    }
    
    SIZE = (10, 10)
    
    def __init__(self, position=(0, 0), velocity=(0, 0)):
        self.rect = Rect(*position, *self.SIZE)
        self.velocity = Vector2(velocity)
        self.image = None
    
    def update(self, dtime):
        """Update entity"""
        self.rect.center += self.velocity * dtime
    
    def set_position(self, position=(0, 0)):
        """Set entity position"""
        self.rect.center = position
    
    def set_velocity(self, velocity=(0, 0)):
        """Set entity velocity"""
        self.velocity = Vector2(velocity)

    def get_position(self):
        """Get entity position"""
        return self.rect.center
    
    def get_velocity(self):
        """Get entity velocity"""
        return tuple(self.velocity)
    
    @classmethod
    def register(cls):
        """Register entity definition"""
        EntityManager.registered[cls.definition["id"]] = cls
    
    
