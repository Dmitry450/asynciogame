from .entity import Entity


class Player(Entity):
    """A player entity"""
    definition = {
        "id": "builtin:player",
        "image": "resources/player.png",
    }
    
    def __init__(self, name,
                 position=(0, 0),
                 velocity=(0, 0)):
        super().__init__(position, velocity)
        
        self.name = name
