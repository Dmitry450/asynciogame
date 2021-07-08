from .enemy import Enemy


def on_load(game):
    Enemy.register()
    
    game.entity_manager.add_entity(Enemy())
