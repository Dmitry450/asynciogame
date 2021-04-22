import asyncio

from pygame.math import Vector2


class LocalPlayer:
    """A local player to control"""
    SPEED = 80  # FIXME - Easy to cheat!!!
    
    def __init__(self, game, position=(0, 0), velocity=(0, 0)):
        self.position = Vector2(position)
        self.velocity = Vector2(velocity)
        
        self.game = game
        
        self.game.graphics.track_object = self
        
        self.image = None
    
    def update(self, dtime):
        """Update player position"""
        self.position += self.velocity * dtime
    
    def draw(self):
        """Draw player"""
        self.game.graphics.draw(self.image, self.position)
    
    def set_image(self, name):
        """Set image and load if neccasuary"""
        self.image = name
        
        self.game.graphics.load_image(name)

    def update_presses(self, **presses):
        """Update velocity based on pressed keys"""
        if presses['up']:
            self.velocity.y = -self.SPEED
        elif presses['down']:
            self.velocity.y = self.SPEED
        else:
            self.velocity.y = 0

        if presses['left']:
            self.velocity.x = -self.SPEED
        elif presses['right']:
            self.velocity.x = self.SPEED
        else:
            self.velocity.x = 0

    async def sync_player(self):
        """Sync player velocity and position with server"""
        while self.game.running:
            await asyncio.sleep(self.game.config['player.synctime'])
            # FIXME - easy to DOS-attack with synctime <= 0
            
            await self.game.connection.send({
                "type": "player.sync",
                "position": tuple(self.position),
                "velocity": tuple(self.velocity),
            })
