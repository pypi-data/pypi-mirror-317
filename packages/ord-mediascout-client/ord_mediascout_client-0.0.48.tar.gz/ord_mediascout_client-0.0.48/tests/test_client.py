import pytest

from ord_mediascout_client import (
    CounterpartyStatus,
    GetClientRequest,
)


@pytest.fixture(scope="module")
def create_client(client, get__client_data__dto):
    def _create_client():
        request_data = get__client_data__dto()

        response_data = client.create_client(request_data)
        return response_data
    return _create_client


def test__create_client(client, get__client_data__dto):
    request_data = get__client_data__dto()

    response_data = client.create_client(request_data)

    assert response_data.id is not None
    assert request_data.name == response_data.name
    assert request_data.inn == response_data.inn
    # assert request_data.mobilePhone == response_data.mobilePhone
    # assert request_data.epayNumber == response_data.epayNumber
    # assert request_data.regNumber == response_data.regNumber
    # assert request_data.oksmNumber == response_data.oksmNumber
    # assert request_data.createMode == response_data.createMode
    assert request_data.legalForm == response_data.legalForm
    assert response_data.status == CounterpartyStatus.Active


def test__get_clients(client):
    request_data = GetClientRequest(status=CounterpartyStatus.Active)

    response_data = client.get_clients(request_data)

    assert len(response_data) > 0
    for participant in response_data:
        assert participant.id is not None
        assert participant.status == CounterpartyStatus.Active


def test__get_client__by_id(client, create_client):
    data = create_client()
    request_data = GetClientRequest(id=data.id)

    response_data = client.get_clients(request_data)

    assert len(response_data) == 1
    for participant in response_data:
        assert participant.id == data.id


def test__get_client__by_inn(client, get__client_data__dto):
    data = get__client_data__dto()
    request_data = GetClientRequest(inn=data.inn)

    response_data = client.get_clients(request_data)

    assert len(response_data) == 1
    for participant in response_data:
        assert participant.id is not None
        assert participant.inn == data.inn
