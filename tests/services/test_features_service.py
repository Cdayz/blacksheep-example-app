import pytest
import msgpack
import contextlib
import dataclasses

from unittest import mock

from app.services.features import FeaturesService, AppFeatures


class ConnectionMock(mock.AsyncMock):

    @contextlib.asynccontextmanager
    async def connection(self):
        yield self


@pytest.mark.asyncio
async def test_features_in_cache():
    pg = ConnectionMock()
    redis = ConnectionMock()
    service = FeaturesService(pg, redis)
    expected = AppFeatures(
        app='test',
        features={'f1': True, 'f2': False},
    )

    redis.get.return_value = msgpack.packb(dataclasses.asdict(expected))
    features = await service.get_features('test')

    assert expected == features
    redis.get.assert_called_with('APP_FEATURES_test')
    pg.fetch.assert_not_called()
    redis.setex.assert_not_called()


@pytest.mark.asyncio
async def test_features_not_in_cache():
    pg = ConnectionMock()
    redis = ConnectionMock()
    service = FeaturesService(pg, redis)
    expected = AppFeatures(
        app='test',
        features={'f1': True, 'f2': False},
    )

    redis.get.return_value = None
    pg.fetch.return_value = [['f1', True], ['f2', False]]

    features = await service.get_features('test')

    assert expected == features
    redis.get.assert_called_with('APP_FEATURES_test')
    pg.fetch.assert_called_with('SELECT feature_name, is_enabled FROM features WHERE application = $1', 'test')
    redis.setex.assert_called_with(
        key='APP_FEATURES_test',
        seconds=10,
        value=msgpack.packb(dataclasses.asdict(expected)),
    )
