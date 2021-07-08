import asyncio
import logging

from .player import Player
from .client import Client
from .entity_manager import EntityManager
from .addons import load_addons


class GameController:
    """Controls game logic"""
    
    def __init__(self, game):
        self.game = game
    
    def update(self, dtime):
        pass


class Game:
    """Main game object"""
    config = {
        "entity.updtime": 1/20,
        "entity.synctime": 0.05,
        "game.updtime": 1/20,
    }
    
    class Api:
        
        def __init__(self, game):
            self.game = game
            
            self.handlers = {
                'on_player_join': [],
                'on_player_leave': [],
            }
        
        def play_sound(self, name, volume=1.0, exclude_players=None):
            """Play specified sound for all players except exclude_players.
            If exclude_players is None, play sound for everyone
            """
            sound = {
                "type": "normal",
                "name": name,
                "volume": volume,
            }
            
            if exclude_players is not None:
                sound["exclude_players"] = exclude_players
            
            self.game.push_event({
                "type": "sound.play",
                "sound": sound,
            })
        
        def play_sound_at(self, name, entity=None, position=None,
                          volume=1.0, fade_dist=1, min_volume=0.1):
            """Play scpecified sound at specified position or entitys position.
            fade_dist specifies distance from player to sound source to start fading away.
            If calculated (client side) sound volume lower than min_volume, its volume changed to 0
            """
            if entityid is None and position is None:
                logging.warning("Game.Api.play_sound_at: expected entity or position argument (both are None)")
                return
            
            sound = {
                "name": name,
                "volume": volume,
                "fade_dist": fade_dist,
                "min_volume": min_volume,
            }
            
            if exclude_players is not None:
                sound["exclude_players"] = exclude_players
            
            if position is not None:
                sound["type"] = "attached_to_position"
                sound["position"] = position
            
            else:
                sound["type"] = "attached_to_entity"
                sound["entity"] = entity.id
        
        def register_handler(self, name):
            if name in self.handlers.keys():
                logging.warning(f"Game.Api.register_handler: handler {name} already exists")
                return
            
            self.handlers[name] = []
        
        def add_handlers(self, **kwargs):
            for name in kwargs.keys():
                if self.handlers.get(name) is None:
                    logging.warning(f"Game.Api.add_handlers: no such handler {name}. "
                                    "If you want to add custom handler, please call register_handler first")
                
                else:
                    self.handlers[name].append(kwargs[name])
        
        def call_handlers(self, name, *args, **kwargs):
            if self.handlers.get(name) is None:
                logging.warning(f"Game.Api.call_handlers: no such handler: {name}")
            
            for handler in self.handlers[name]:
                try:
                    handler(*args, **kwargs)
                
                except Exception:
                    logging.exception(f"Game.Api.call_handlers: exception occured in {name} handler")
    
    def __init__(self):
        self.clients = {}
        
        self.controllers = {}
        
        Player.register()
        
        self.entity_manager = EntityManager(self)
        self.running = True
        
        self.api = self.Api(self)
        
        load_addons(self)  # TODO - make config to enable/disable addons
    
    def add_controller(self, name, controller_t, *args, **kwargs):
        self.controllers[name] = controller_t(self, *args, **kwargs)

    def on_client_connected(self, reader, writer):
        """Callback for asyncio.start_server"""
        client = Client(self, reader, writer)
        asyncio.create_task(client.init())

    def add_player(self, name):
        """Create new player entity"""
        player = Player()
        
        self.entity_manager.add_entity(player, name)
        
        self.api.call_handlers('on_player_join', player)
        
        return player

    def has_player(self, name):
        """Check is there already player on server with given name"""
        return self.entity_manager.entities.get(name) is not None
    
    def push_event(self, event):
        """Send event to all clients"""
        for client in self.clients.values():
            client.event_queue.put_nowait(event)
    
    def disconnect_player(self, name):
        """Remove player entity"""
        player = self.entity_manager.entities[name]
        
        self.api.call_handlers('on_player_leave', player)
        
        self.entity_manager.del_entity(name)
        
        del self.clients[name]
    
    async def logic_main(self):
        """Global game logic"""
        while self.running:
            await asyncio.sleep(self.config["game.updtime"])
            
            for controller in self.controllers.values():
                controller.update(self.config["game.updtime"])
        
    async def main(self):
        """Run all asyncio tasks and serve forever"""
        asyncio.create_task(self.entity_manager.run_entities_update())
        asyncio.create_task(self.entity_manager.run_entities_sync())
        asyncio.create_task(self.logic_main())
        
        server = await asyncio.start_server(
            self.on_client_connected, '127.0.0.1', 43210)
        
        async with server:
            await server.serve_forever()
