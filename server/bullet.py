from .projectile import Projectile


class Bullet(Projectile):
    definition = {
        "id": "custom:bullet",
        "images": {"default": "resources/bullet.png"},
    }
    
    SIZE = (8, 8)
    
    def __init__(self, position=(0, 0), src_entity=None, angle=90):
        super().__init__(position, src_entity, angle)
        
        self.image = "default"
    
    def on_hit(self, entity):
        self.manager.del_entity(self.id)
