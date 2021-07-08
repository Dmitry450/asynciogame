import os
import importlib
import logging


def load_addons(game, names=None):
    try:
        if names is None:
            names = os.listdir(os.path.join('server', 'addons'))

    except FileNotFoundError:
        logging.error('load_addons: no addons directory found')

    for name in names:
        if not os.path.exists(os.path.join('server', 'addons', name, '.addon')):
            logging.info(f'load_addons: skipping directory {name} because it\'s not an addon')
            continue

        module = importlib.import_module(f'server.addons.{name}')

        try:
            module.on_load(game)

        except AttributeError:
            logging.error(f'load_addons: addon {name} has no on_load function')

        except Exception as e:
            logging.error(f'load_addons: exception when loading addon {name} - {e.__class__.__name__}: {str(e)}')

        else:
            logging.info(f'load_addons: loaded addon {name}')
