import math

from pygame.math import Vector2

from .entity import Entity


class Projectile(Entity):
    """Abstract class for adding projectiles"""
    SPEED = 200
    
    def __init__(self, position=(0, 0), src_entity=None, angle=90):
        super().__init__(position, Vector2(self.SPEED, 0).rotate(angle))
        
        self.src_entity = src_entity

    def update(self, dtime):
        super().update(dtime)

        if self.manager is not None:
            for entity in self.manager.get_tagged('hittable'):
                if entity is not self.src_entity and entity.rect.colliderect(self.rect):
                    self.on_hit(entity)
    
    def on_hit(self, entity):
        """Called when projectile hit an entity"""
        pass
