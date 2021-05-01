import asyncio

from pygame.math import Vector2

from .entity import RemoteEntity


class LocalPlayer(RemoteEntity):
    """A local player to control"""
    SPEED = 80  # FIXME - Easy to cheat!!!
    
    def __init__(self, game, definition, position=(0, 0), velocity=(0, 0)):
        super().__init__(game, definition, position, velocity)
        
        game.graphics.track_object = self
    
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
