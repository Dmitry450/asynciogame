from pygame.math import Vector2

import random

from .entity import Entity


def randvector(speed):
    return Vector2(random.randint(-2, 2), random.randint(-2, 2)) * speed


class Enemy(Entity):
    """Randomly moving entity. Created for testing"""
    SPEED = 30
    SIZE = (32, 32)
    
    definition = {
        "id": "custom:enemy",
        "image": {
            "type": "animated_image",
            "image": "resources/enemy.png",
            "tiles_x": 2,
            "tiles_y": 1,
            "animations": {
                "main": {
                    "time_per_frame": 0.5,
                    "frames": [(0, 0), (1, 0)],
                }
            },
            "initial_animation": "main",
        },
    }
    
    def __init__(self, position=(0, 0)):
        super().__init__(position, randvector(self.SPEED))
        
        self.change_velocity_time = random.randint(1, 4)
        self.timer = 0
        self.animation = "main"
    
    def on_added(self, manager, id):
        super().on_added(manager, id)
        
        self.add_tag('hittable')
    
    def update(self, dtime):
        super().update(dtime)
        self.timer += dtime
        
        if self.timer >= self.change_velocity_time:
            self.timer = 0
            self.change_velocity_time = random.randint(1, 4)
            
            self.velocity = randvector(self.SPEED)
