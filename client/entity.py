from pygame.math import Vector2


class RemoteEntity:
    """A remote entity used for client-side prediction"""
    
    def __init__(self, game, definition, position=(0, 0), velocity=(0, 0)):
        self.position = Vector2(position)
        self.velocity = Vector2(velocity)
        
        self.image = None
        
        self.game = game
        
        self.definition = definition
    
    def sync(self, position=(0, 0), velocity=(0, 0), image=None):
        """Reset entity attributes"""
        self.position = Vector2(position)
        self.velocity = Vector2(velocity)
        
        self.set_image(image)
    
    def update(self, dtime):
        """Predict next position based on velocity"""
        self.position += self.velocity * dtime
    
    def draw(self):
        """Draw entity"""
        self.game.graphics.draw(self.image, self.position)
    
    def set_image(self, name):
        """Set entity image and load it if neccasuary"""
        if self.definition["images"].get(name) in (self.image, None):
            return
        
        img = self.definition["images"][name]
        
        if isinstance(img, dict):
            self.image = self.definition["images"][name]["id"]
        
            self.game.graphics.load_dict(img)

        else:
            self.image = img
            
            self.game.graphics.load_image(self.image)
