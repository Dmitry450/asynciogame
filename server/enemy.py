from pygame.math import Vector2

import random

from .entity import Entity


def randvector(speed):
    return Vector2(random.randint(-2, 2), random.randint(-2, 2)) * speed


class Enemy(Entity):
    """Randomly moving entity. Created for testing"""
    SPEED = 30
    
    definition = {
        "id": "custom:enemy",
        "images": {"default": "resources/enemy.png"},
    }
    
    def __init__(self, position=(0, 0)):
        super().__init__(position, randvector(self.SPEED))
        
        self.change_velocity_time = random.randint(1, 4)
        self.timer = 0
        self.image = "default"
    
    def update(self, dtime):
        super().update(dtime)
        self.timer += dtime
        
        if self.timer >= self.change_velocity_time:
            self.timer = 0
            self.change_velocity_time = random.randint(1, 4)
            
            self.velocity = randvector(self.SPEED)
