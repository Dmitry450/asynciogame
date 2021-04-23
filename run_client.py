#!/usr/bin/env python3
import sys
import asyncio

from client.game import Game


if len(sys.argv) != 1 + 3:
    print("Wrong arguments count. Expected <address> <port> <playername>")
    raise SystemExit(1)


*addr, name = sys.argv[1:]

game = Game(name)

asyncio.run(game.connect(addr))
