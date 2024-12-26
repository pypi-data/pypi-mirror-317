import pytest

from ord_mediascout_client import (
    ContractStatus,
    DeleteContractWebApiDto,
    DeleteContractKind,
    EditFinalContractWebApiDto,
    EditInitialContractWebApiDto,
    EditOuterContractWebApiDto,
    GetFinalContractsRequest,
    GetInitialContractRequest,
    GetOuterContractsRequest,
)


# Final Contract
@pytest.fixture(scope="module")
def create_final_contract(client, get__final_contract_data__dto):
    def _create_final_contract():
        request_data = get__final_contract_data__dto()

        response_data = client.create_final_contract(request_data)
        return response_data
    return _create_final_contract


def test__create_final_contract(client, get__final_contract_data__dto):
    request_data = get__final_contract_data__dto()

    response_data = client.create_final_contract(request_data)

    assert response_data.id is not None
    assert request_data.number == response_data.number
    assert request_data.date == response_data.date
    assert request_data.amount == response_data.amount
    assert request_data.type == response_data.type
    assert request_data.subjectType == response_data.subjectType
    assert request_data.clientId == response_data.clientId
    assert response_data.status == ContractStatus.Created or ContractStatus.Active


def test__get_final_contracts(client):
    request_data = GetFinalContractsRequest(status=ContractStatus.Active)

    response_data = client.get_final_contracts(request_data)

    for final_contract in response_data:
        assert final_contract.id is not None
        assert final_contract.status == ContractStatus.Active


def test__edit_final_contract(client, create_final_contract):
    data = create_final_contract().dict()
    contract_id = data["id"]
    data["number"] += "_edit_"
    data["amount"] += 1
    for key in ["id", "cid", "status", "contractorId", "contractorInn", "contractorName", "erirValidationError"]:
        data.pop(key, None)
    request_data = EditFinalContractWebApiDto(**data)

    response_data = client.edit_final_contract(contract_id, request_data)

    assert response_data.number == request_data.number
    assert response_data.amount == request_data.amount


# curl -X 'DELETE' 'https://demo.mediascout.ru/webapi/v3/contracts/FinalContract/CTiwhIpoQ_F0OEPpKj8vWKGg' -H 'accept: */*'
def test__delete_final_contract(client, create_final_contract):
    created_final_contract = create_final_contract()
    request_data = DeleteContractWebApiDto(
        contractId=created_final_contract.id,
        contractKind=DeleteContractKind.FinalContract
    )
    client.delete_contract(created_final_contract.id, request_data)


# Initial Contract
@pytest.fixture(scope="module")
def create_initial_contract(client, get__initial_contract_data__dto):
    def _create_initial_contract():
        request_data = get__initial_contract_data__dto()

        response_data = client.create_initial_contract(request_data)
        return response_data
    return _create_initial_contract


def test__create_initial_contract(client, get__initial_contract_data__dto):
    request_data = get__initial_contract_data__dto()

    response_data = client.create_initial_contract(request_data)

    assert response_data.id is not None
    assert request_data.number == response_data.number
    assert request_data.date == response_data.date
    assert request_data.amount == response_data.amount
    # assert request_data.isAgentActingForPublisher == response_data.isAgentActingForPublisher
    assert request_data.type == response_data.type
    assert request_data.subjectType == response_data.subjectType
    # assert request_data.actionType == response_data.actionType
    assert request_data.parentMainContractId == response_data.parentMainContractId
    assert request_data.contractorId == response_data.contractorId
    assert request_data.clientId == response_data.clientId
    assert request_data.finalContractId == response_data.finalContractId
    assert response_data.status == ContractStatus.Created or ContractStatus.Active


def test__get_initial_contracts(client):
    request_data = GetInitialContractRequest(status=ContractStatus.Active)

    response_data = client.get_initial_contracts(request_data)

    assert len(response_data) > 0
    for initial_contract in response_data:
        assert initial_contract.id is not None
        assert initial_contract.status == ContractStatus.Active


def test__edit_initial_contract(client, create_initial_contract):
    data = create_initial_contract().dict()
    contract_id = data["id"]
    data["number"] += "_edit_"
    data["amount"] += 1
    for key in [
        "id", "cid", "status", "contractorInn", "contractorName", "clientInn", "clientName", "erirValidationError"
    ]:
        data.pop(key, None)
    request_data = EditInitialContractWebApiDto(**data)

    response_data = client.edit_initial_contract(contract_id, request_data)

    assert response_data.number == request_data.number
    assert response_data.amount == request_data.amount


def test__delete_initial_contract(client, create_initial_contract):
    created_initial_contract = create_initial_contract()
    request_data = DeleteContractWebApiDto(
        contractId=created_initial_contract.id,
        finalContractId=created_initial_contract.finalContractId,
        contractKind=DeleteContractKind.InitialContract
    )
    client.delete_contract(created_initial_contract.id, request_data)


# Outer Contract
@pytest.fixture(scope="module")
def create_outer_contract(client, get__outer_contract_data__dto):
    def _create_outer_contract():
        request_data = get__outer_contract_data__dto()

        response_data = client.create_outer_contract(request_data)
        return response_data
    return _create_outer_contract


def test__create_outer_contract(client, create_outer_contract):
    request_data = create_outer_contract()

    response_data = client.create_outer_contract(request_data)

    assert response_data.id is not None
    assert request_data.number == response_data.number
    assert request_data.date == response_data.date
    assert request_data.amount == response_data.amount
    # assert request_data.isAgentActingForPublisher == response_data.isAgentActingForPublisher
    assert request_data.type == response_data.type
    assert request_data.subjectType == response_data.subjectType
    # assert request_data.actionType == response_data.actionType
    # assert request_data.parentMainContractId == response_data.parentMainContractId
    assert request_data.contractorId == response_data.contractorId
    assert response_data.status == ContractStatus.Created or ContractStatus.Active


def test__get_outer_contracts(client):
    request_data = GetOuterContractsRequest(status=ContractStatus.Active)

    response_data = client.get_outer_contracts(request_data)

    assert len(response_data) > 0
    for outer_contract in response_data:
        assert outer_contract.id is not None
        assert outer_contract.status == ContractStatus.Active


def test__edit_outer_contract(client, create_outer_contract):
    data = create_outer_contract().dict()
    contract_id = data["id"]
    data["number"] += "_edit_"
    data["amount"] += 1
    for key in ["id", "cid", "status", "erirValidationError"]:
        data.pop(key, None)
    request_data = EditOuterContractWebApiDto(**data)

    response_data = client.edit_outer_contract(contract_id, request_data)

    assert response_data.number == request_data.number
    assert response_data.amount == request_data.amount


def test__delete_outer_contract(client, create_outer_contract):
    created_outer_contract = create_outer_contract()
    request_data = DeleteContractWebApiDto(
        contractId=created_outer_contract.id,
        contractKind=DeleteContractKind.OuterContract
    )
    client.delete_contract(created_outer_contract.id, request_data)
