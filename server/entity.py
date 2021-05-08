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
        self.manager = None
        self.tags = set()
        self.id = None
    
    def on_added(self, manager, id):
        """Called when entity added to EntityManager"""
        self.manager = manager
        self.id = id
    
    def update(self, dtime):
        """Update entity"""
        self.rect.topleft += self.velocity * dtime
    
    def set_position(self, position=(0, 0)):
        """Set entity position"""
        self.rect.topleft = position
    
    def set_velocity(self, velocity=(0, 0)):
        """Set entity velocity"""
        self.velocity = Vector2(velocity)

    def get_position(self):
        """Get entity position"""
        return self.rect.topleft
    
    def get_velocity(self):
        """Get entity velocity"""
        return tuple(self.velocity)
    
    def add_tag(self, tag):
        """Add tag to entity"""
        if self.manager is not None:
            self.tags.add(tag)
            self.manager.tag_entity(self, tag)
    
    def remove_tag(self, tag):
        """Remove tag from entity"""
        if self.manager is not None and tag in self.tags:
            self.tags.remove(tag)
            self.manager.untag_entity(self, tag)
    
    def clear_tags(self):
        """Remove all tags from entity"""
        if self.manager is not None:
            for tag in self.tags:
                self.manager.untag_entity(self, tag)
    
    @classmethod
    def register(cls):
        """Register entity definition"""
        EntityManager.registered[cls.definition["id"]] = cls
    
    
