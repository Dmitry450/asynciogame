import asyncio

from pygame.math import Vector2


class LocalPlayer:
    SPEED = 80
    
    def __init__(self, game, position=(0, 0), velocity=(0, 0)):
        self.position = Vector2(position)
        self.velocity = Vector2(velocity)
        
        self.game = game
        
        self.game.graphics.track_object = self
        
        self.image = None
    
    def update(self, dtime):
        self.position += self.velocity * dtime
    
    def draw(self):
        self.game.graphics.draw(self.image, self.position)
    
    def set_image(self, name):
        self.image = name
        
        self.game.graphics.load_image(name)

    def update_presses(self, **presses):
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
        while self.game.running:
            await asyncio.sleep(self.game.config['player.synctime'])
            
            await self.game.connection.send({
                "type": "player.sync",
                "position": tuple(self.position),
                "velocity": tuple(self.velocity),
            })
