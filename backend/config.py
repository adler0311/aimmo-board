import sys
import os
import logging


class Config:
    DEBUG = True


class LocalConfig(Config):
    MONGO_URI = 'mongodb://localhost:27017/aimmo-board?connect=false'


class DevConfig(Config):
    MONGO_URI = 'mongomock://127.0.0.1:27017/aimmo-board?connect=false'


def get_current_config() -> Config:
    mode = os.environ.get('MODE', 'dev')  # local, dev
    logging.debug('current mode is {}'.format(mode))
    this_module = sys.modules[__name__]
    return getattr(this_module, '%sConfig' % mode.capitalize())
