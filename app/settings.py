"""Application settings."""

from urllib.parse import quote

from environs import Env

env = Env()
env.read_env()


class ConfigError(Exception):
    """Exception raised when configuration is broken."""


DATABASE_NAME = env.str('DATABASE_NAME')
DATABASE_HOST = env.str('DATABASE_HOST')
DATABASE_PORT = env.int('DATABASE_PORT')
DATABASE_USER = env.str('DATABASE_USER')
DATABASE_PASS = env.str('DATABASE_PASS')

DATABASE_DSN = f'postgresql://{DATABASE_USER}:{quote(DATABASE_PASS)}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'

REDIS_HOST = env.str('REDIS_HOST')
REDIS_PORT = env.str('REDIS_PORT')
REDIS_USER = env.str('REDIS_USER', None)
REDIS_PASS = env.str('REDIS_PASS', None)
REDIS_DB_NUM = env.int('REDIS_DB_NUM')
REDIS_IS_SENTINEL = env.bool('REDIS_IS_SENTINEL')
REDIS_SENTINEL_MASTER = env.str('REDIS_SENTINEL_MASTER', None)

if REDIS_IS_SENTINEL and not REDIS_SENTINEL_MASTER:
    raise ConfigError('REDIS_SENTINEL_MASTER env variable must be provided when REDIS_IS_SENTINEL is true')
