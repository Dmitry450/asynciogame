from pygame.math import Vector2


class RemoteEntity:
    """A remote entity used for client-side prediction"""
    
    def __init__(self, game, definition, position=(0, 0), velocity=(0, 0)):
        self.last_position = Vector2(position)
        
        self.position = Vector2(position)
        self.velocity = Vector2(velocity)
        
        self.sprite = game.graphics.create_sprite(definition["image"])
        
        self.game = game
        
        self.definition = definition
    
    def sync(self, position=(0, 0), velocity=(0, 0), animation=None):
        """Update entity attributes"""
        self.position.update(position)
        self.velocity.update(velocity)
        
        if animation is not None:
            # This will cause exception if sprite is not AnimatedImage instance
            self.sprite.set_animation(animation)
        
        self.update_sprite_position()
    
    def update(self, dtime):
        """Predict next position based on velocity"""
        self.position += self.velocity * dtime
        
        self.update_sprite_position()
    
    def update_sprite_position(self):
        self.last_position = (self.position + self.last_position) / 2
        self.sprite.set_pos(self.last_position)
    
    def __del__(self):
        self.sprite.kill()
