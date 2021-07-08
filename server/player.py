from pygame.math import Vector2

from .entity import Entity


class PlayerController:
    """Defines player behavior on some events (for example, mouse presses)"""
    
    def __init__(self, player):
        self.player = player
    
    def on_added(self):
        """Called when player added to manager"""
        pass
    
    def on_mouse_press(self, position):
        """Called when player presses mouse"""
        pass
    
    def on_mouse_release(self, position):
        """Called when player releases mouse"""
        pass
    
    def update(self, dtime):
        """Called on every player update"""
        pass


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
        
        self.controllers = {}
    
    def add_controller(self, name, controller_t, *args, **kwargs):
        self.controllers[name] = controller_t(self, *args, **kwargs)
        
    def on_added(self, manager, id):
        super().on_added(manager, id)
        
        for controller in self.controllers.values():
            controller.on_added()
    
    def set_mouse(self, mouse):
        if self.mouse["pressed"] and not mouse["pressed"]:
            self.on_mouse_release(mouse["position"])

        elif not self.mouse["pressed"] and mouse["pressed"]:
            self.on_mouse_press(mouse["position"])
        
        self.mouse = mouse

    def on_mouse_press(self, position):
        for controller in self.controllers.values():
            controller.on_mouse_press(position)

    def on_mouse_release(self, position):
        for controller in self.controllers.values():
            controller.on_mouse_release(position)
    
    def update(self, dtime):
        super().update(dtime)
        
        for controller in self.controllers.values():
            controller.update(dtime)
