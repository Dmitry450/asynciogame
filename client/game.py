import asyncio

import pygame

from .entity_manager import EntityManager
from .local_player import LocalPlayer
from .connection import Connection
from .graphics import Graphics
from .async_clock import AsyncClock


class Game:
    SIZE = (800, 640)
    
    config = {
        "player.synctime": 0.05,
    }
    
    def __init__(self, name):
        pygame.init()
        
        self.screen = pygame.display.set_mode(self.SIZE)
        self.bg = pygame.Surface(self.SIZE)
        self.bg.fill('#4444FF')
        
        self.graphics = Graphics(self.screen)
        
        self.graphics.draw_offset = pygame.math.Vector2(self.SIZE) / 2
        
        self.caption = "AsyncioNetgame"
        
        pygame.display.set_caption(self.caption)
        
        self.connection = None
        
        self.entity_manager = EntityManager(self)
        
        self.playername = name
        
        self.local_player = self.entity_manager.player = LocalPlayer(self)
        
        self.running = True
    
    async def connect(self, addr):
        self.connection = Connection(self, *await asyncio.open_connection(*addr))
        
        await self.connection.init()
        
        if not self.connection.disconnected.is_set():
            self.caption = f"AsyncioNetgame: {':'.join(addr)}"
            await self.main()
    
    async def game_loop(self):
        presses = {'up': False, 'down': False, 'left': False, 'right': False}
        timer = AsyncClock()
        
        while self.running:
            await timer.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        presses['up'] = True

                    elif event.key == pygame.K_s:
                        presses['down'] = True
                    
                    elif event.key == pygame.K_a:
                        presses['left'] = True
                    
                    elif event.key == pygame.K_d:
                        presses['right'] = True
                
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        presses['up'] = False

                    elif event.key == pygame.K_s:
                        presses['down'] = False
                    
                    elif event.key == pygame.K_a:
                        presses['left'] = False
                    
                    elif event.key == pygame.K_d:
                        presses['right'] = False
                
                elif event.type == pygame.QUIT:
                    print('Quit event received')
                    
                    pygame.quit()
                    
                    self.running = False
                    
                    await self.connection.send({
                        "type": "client.disconnect",
                        "reason": "client asked disconnect",
                    })
                    
                    self.connection.disconnected.set()
                    
                    return
                
            self.local_player.update_presses(**presses)
            
            self.graphics.update_camera()
            
            self.screen.blit(self.bg, (0, 0))
            
            self.local_player.draw()
            
            self.entity_manager.draw()
            
            pygame.display.flip()
            
            #pygame.display.set_caption(self.caption + f' {timer.get_fps()}')
            # Shows wrong count. TODO - fix that


    async def main(self):
        asyncio.create_task(self.entity_manager.run_entities_sync())
        asyncio.create_task(self.entity_manager.run_entities_update())
        asyncio.create_task(self.game_loop())
        asyncio.create_task(self.local_player.sync_player())
        
        await self.connection.disconnected.wait()
