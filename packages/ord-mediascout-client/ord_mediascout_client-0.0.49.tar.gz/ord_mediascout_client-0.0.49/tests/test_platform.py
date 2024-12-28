import pytest

from ord_mediascout_client import EditPlatformWebApiDto


# НЕ работает в режиме "get or create", только "create" с новым url, потому url и название генерятся
@pytest.fixture(scope="module")
def create_platform(client, get__platform_data__dto):
    def _create_platform():
        request_data = get__platform_data__dto()

        response_data = client.create_platform(request_data)
        return response_data, request_data
    return _create_platform


def test__create_platform(client, get__platform_data__dto):
    request_data = get__platform_data__dto()

    response_data = client.create_platform(request_data)

    assert response_data is not None
    assert response_data.id is not None


def test__edit_platform(client, create_platform):
    created_platform, platform_data = create_platform()
    platform_data.name += "_edit_"
    request_data = EditPlatformWebApiDto(**platform_data.dict())

    response_data = client.edit_platform(created_platform.id, request_data)

    assert response_data is not None
    assert response_data.id is not None
    assert request_data.name == response_data.name
