import asyncio

from server.game import Game


game = Game()

asyncio.run(game.main())
