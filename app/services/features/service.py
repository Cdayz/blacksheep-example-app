"""Features service."""

import dataclasses
from typing import Optional

import msgpack

from app.database import PostgresConnectionPool, RedisConnectionPool
from app.services.features.types import AppFeatures


class FeaturesService:
    """Service for fetch application features from database and cache."""

    def __init__(self, pg: PostgresConnectionPool, redis: RedisConnectionPool):
        """Initialize service with postgres and redis connections."""
        self.pg = pg
        self.redis = redis

    async def get_features(self, app_name: str) -> AppFeatures:
        """Fetch features by app name."""
        features = await self.get_from_redis(app_name)

        if features:
            return features

        features = await self.get_from_database(app_name)
        await self.save_in_redis(features)

        return features

    async def get_from_database(self, app_name: str) -> AppFeatures:
        """Fetch features from database by app name."""
        query = "SELECT feature_name, is_enabled FROM features WHERE application = $1"

        async with self.pg.connection() as conn:
            rows = await conn.fetch(query, app_name)

            result = AppFeatures(app=app_name, features={})

            for feature_name, is_enabled in rows:
                result.features[feature_name] = is_enabled

            return result

    def cache_key(self, app_name: str) -> str:
        """Generate cache key by app name."""
        return f'APP_FEATURES_{app_name}'

    async def get_from_redis(self, app_name: str) -> Optional[AppFeatures]:
        """Fetch features from cache by app name."""
        async with self.redis.connection() as conn:
            data = await conn.get(self.cache_key(app_name))

            if data is None:
                return None

            dct = msgpack.unpackb(data)

            return AppFeatures(app=dct['app'], features=dct['features'])

    async def save_in_redis(self, features: AppFeatures):
        """Store features in cache."""
        async with self.redis.connection() as conn:
            data_bytes = msgpack.packb(dataclasses.asdict(features))
            await conn.setex(
                key=self.cache_key(features.app),
                seconds=10,  # TTL of key
                value=data_bytes,
            )
