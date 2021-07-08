from pygame.math import Vector2

from .entity import Entity


class Player(Entity):
    """A player entity"""
    definition = {
        "id": "builtin:player",
        "image": {
            "type": "image",
            "image": "resources/player.png",
        },
    }
    
    SIZE = (32, 32)
    
    def __init__(self,
                 position=(0, 0),
                 velocity=(0, 0)):
        super().__init__(position, velocity)
        
        self.mouse = {
            "pressed": False,
            "position": None,
        }
        
    def on_added(self, manager, id):
        super().on_added(manager, id)
        
        self.add_tag('player')
        self.add_tag('hittable')
    
    def set_mouse(self, mouse):
        if self.mouse["pressed"] and not mouse["pressed"]:
            self.on_mouse_release(mouse["position"])

        elif not self.mouse["pressed"] and mouse["pressed"]:
            self.on_mouse_press(mouse["position"])
        
        self.mouse = mouse

    def on_mouse_press(self, position):
        """self.manager.add_entity(Bullet(
            position=self.rect.center,
            src_entity=self,
            angle=Vector2(0, 0).angle_to(Vector2(position) - Vector2(self.rect.center)))
        )"""  # I'll rewrite this later for new addon system
        pass 

    def on_mouse_release(self, position):
        pass
