import pytest

# from tests.conftest import print_obj
from .conftest import FEED__ELEMENTS

from ord_mediascout_client import (
    GetContainerWebApiDto,
    GetFeedElementsWebApiDto,
    EditAdvertisingContainerRequest,
)


@pytest.fixture(scope="module")
def create_container(client, get__feed_elements_data__dto, get__container_data__dto):
    def _create_container():
        feed_data = get__feed_elements_data__dto()
        request_data = get__container_data__dto(
            feedNativeCustomerId=feed_data.feedNativeCustomerId,
            nativeCustomerId=feed_data.feedElements[0].nativeCustomerId
        )

        response_data = client.create_container(request_data)
        return response_data
    return _create_container


@pytest.fixture(scope="module")
def create_feed_element(client, get__feed_elements_data__dto):
    def _create_feed_element():
        request_data = get__feed_elements_data__dto()

        response_data = client.create_feed_elements(request_data)
        return response_data
    return _create_feed_element


@pytest.fixture(scope="module")
def create_feed_elements_bulk(client, get__bulk_feed_elements_data__dto):
    def _create_feed_elements_bulk():
        request_data = get__bulk_feed_elements_data__dto()

        response_data = client.create_feed_elements_bulk(request_data)
        return response_data
    return _create_feed_elements_bulk


def test__create_feed_element(client, get__feed_elements_data__dto):
    request_data = get__feed_elements_data__dto()

    response_data = client.create_feed_elements(request_data)

    assert len(response_data) > 0
    assert response_data[0].id is not None
    assert response_data[0].feedId is not None
    assert response_data[0].status is not None
    assert response_data[0].feedName == request_data.feedName
    assert response_data[0].feedNativeCustomerId == request_data.feedNativeCustomerId
    assert response_data[0].nativeCustomerId == request_data.feedElements[0].nativeCustomerId
    assert response_data[0].description == request_data.feedElements[0].description
    assert response_data[0].advertiserUrls == request_data.feedElements[0].advertiserUrls


def test__create_container(client, get__feed_elements_data__dto, get__container_data__dto):
    feed_data = get__feed_elements_data__dto()
    request_data = get__container_data__dto(
        feedNativeCustomerId=feed_data.feedNativeCustomerId,
        nativeCustomerId=feed_data.feedElements[0].nativeCustomerId
    )

    response_data = client.create_container(request_data)

    assert response_data is not None
    assert response_data.id is not None


def test__get_containers(client):
    request_data = GetContainerWebApiDto(status='Active')

    response_data = client.get_containers(request_data)

    for container in response_data:
        assert container is not None


def test__edit_container(client, create_container):
    container_data = create_container().dict()
    for key in ["feedName", "nativeCustomerId", "feedNativeCustomerId", "erid", "status", "erirValidationError"]:
        container_data.pop(key, None)
    container_data['description'] += '__IS_EDITED__'
    request_data = EditAdvertisingContainerRequest(**container_data)

    response_data = client.edit_container(request_data)

    assert response_data is not None
    assert response_data.id is not None
    assert response_data.description == container_data['description']


def test__get_feed_elements(client):
    # Прописал вручную ids, так как сервис возвращает слишком много активных элементов
    request_data = GetFeedElementsWebApiDto(ids=FEED__ELEMENTS, status='Active')

    response_data = client.get_feed_elements(request_data)

    for feed_element in response_data:
        assert feed_element is not None


def test__edit_feed_element(client, create_feed_element, get__edit_feed_elements_data__dto):
    created_element = create_feed_element()
    request_data = get__edit_feed_elements_data__dto(feedElements=[
        {
            'id': created_element[0].id,
            'textData': [
                {
                    'id': created_element[0].textData[0].id,
                    'actionType': 'Edit',
                    'textData': 'Edited text data',
                },
            ],
        },
    ])

    response_data = client.edit_feed_element(request_data)

    for element in response_data:
        assert element is not None


def test__create_feed_elements_bulk(client, get__bulk_feed_elements_data__dto):
    request_data = get__bulk_feed_elements_data__dto()

    response_data = client.create_feed_elements_bulk(request_data)

    assert response_data is not None
    assert response_data.id is not None


# Используется заранее созданный фид с элементами и не пустыми полями feedElementId и feedId.
# После создания фида методом client.create_feed_elements_bulk(), запрос методом
# client.get_feed_elements_bulk_info() возвращает элементы с еще пустыми feedElementId и feedId.
# По этому выполнить редактирование client.edit_feed_elements_bulk() сразу нельзя.
# Так же нужно дождаться изменения статуса элементов с "ReadyToDownload" и появления загруженных данных в feedElementMedias
def test__edit_feed_elements_bulk(client, get__bulk_edit_feed_elements_data__dto):
    request_data = get__bulk_edit_feed_elements_data__dto()

    response_data = client.edit_feed_elements_bulk(request_data)

    assert response_data.id is not None


@pytest.mark.skip(reason="Этот тест временно отключен")
def test__request_absent_feed_element(client, faker):
    request_dto = GetFeedElementsWebApiDto(ids=['absent_feed_element_id'])

    response_dto = client.get_feed_elements(request_dto)

    assert len(response_dto) == 0


@pytest.mark.skip(reason="Этот тест временно отключен")
def test__request_all_feed_element(client, faker):
    request_dto = GetFeedElementsWebApiDto()

    response_dto = client.get_feed_elements(request_dto)

    assert len(response_dto) != 0
