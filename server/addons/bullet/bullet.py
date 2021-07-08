from server.projectile import Projectile


class Bullet(Projectile):
    definition = {
        "id": "custom:bullet",
        "image": {
            "type": "image",
            "image": "resources/bullet.png",
        },
    }
    
    SIZE = (8, 8)
    
    def on_hit(self, entity):
        self.manager.del_entity(self.id)
