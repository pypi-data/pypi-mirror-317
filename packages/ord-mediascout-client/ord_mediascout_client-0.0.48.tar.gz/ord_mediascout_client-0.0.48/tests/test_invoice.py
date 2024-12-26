import pytest
import random
import copy

from ord_mediascout_client import (
    ClearInvoiceDataWebApiDto,
    EditInvoiceDataWebApiDto,
    EditInvoiceStatisticsWebApiDto,
    EntityIdResponse,
    GetInvoicesWebApiDto,
    InvoiceStatus,
    PartialClearInvoiceWebApiDto,
    PartialClearInvoiceStatisticsItem,
    PartialClearInvoiceStatisticsRequest,
    PartialClearInvoiceInitialContractsRequest,
)


# НЕ работает в режиме "get or create", только "create" с новым номером, потому number генерится
@pytest.fixture(scope="module")
def create_invoice(client, get__invoice_data__dto):
    def _create_invoice():
        request_data = get__invoice_data__dto()

        response_data = client.create_invoice(request_data)
        return response_data
    return _create_invoice


def test__create_invoice(client, get__invoice_data__dto):
    request_data = get__invoice_data__dto()

    response_data = client.create_invoice(request_data)

    assert response_data is not None
    assert response_data.id is not None


def test__get_invoices(client):
    request_data = GetInvoicesWebApiDto(status=InvoiceStatus.Active)

    response_data = client.get_invoices(request_data)

    assert len(response_data) > 0
    for invoice in response_data:
        assert invoice.id is not None
        assert invoice.status == InvoiceStatus.Active


def test__get_one_invoice(client, create_invoice):
    created_invoice = create_invoice()
    request_data = GetInvoicesWebApiDto(ids=[created_invoice.id])

    response_data = client.get_invoices(request_data)[0]

    assert response_data is not None
    assert response_data.id is not None


def test__get_invoice_summary(client, create_invoice):
    created_invoice = create_invoice()
    request_data = EntityIdResponse(id=created_invoice.id)

    response_data = client.get_invoice_summary(request_data)

    assert response_data is not None
    assert response_data.id is not None
    assert isinstance(response_data.id, str)


def test__edit_invoice(client, create_invoice, get__invoice_data__dto):
    # Получить и подготовить данные акта для редактирования
    created_invoice = create_invoice()
    _created_invoice_data = get__invoice_data__dto()
    invoice_data = copy.deepcopy(_created_invoice_data)
    # Отредактировать данные
    invoice_data.number += '_edit_'
    del(invoice_data.initialContractsData)
    del(invoice_data.statisticsByPlatforms)

    request_data = EditInvoiceDataWebApiDto(**invoice_data.dict())

    response_data = client.edit_invoice(created_invoice.id, request_data)

    assert response_data is not None
    assert isinstance(response_data.id, str)


def test__overwrite_invoice(client, create_invoice, get__invoice_data__dto):
    created_invoice = create_invoice()
    _created_invoice_data = get__invoice_data__dto()
    invoice_data = copy.deepcopy(_created_invoice_data)
    # Отредактировать данные
    invoice_data.initialContractsData[0].amount += random.randrange(10, 100)
    invoice_data.statisticsByPlatforms[0].amount += random.randrange(10, 100)

    request_data = EditInvoiceStatisticsWebApiDto(
        initialContractsData=invoice_data.initialContractsData,
        statisticsByPlatforms=invoice_data.statisticsByPlatforms,
    )

    client.overwrite_invoice(created_invoice.id, request_data)
    # Пустой ответ от API МС, делать assert не с чем


def test__confirm_invoice(client, create_invoice):
    created_invoice = create_invoice()
    request_data = EntityIdResponse(id=created_invoice.id)

    client.clear_invoice(request_data)
    # Пустой ответ от API МС, делать assert не с чем


def test__clear_invoice(client, create_invoice):
    created_invoice = create_invoice()
    request_data = ClearInvoiceDataWebApiDto(id=created_invoice.id)

    client.clear_invoice(request_data)
    # Пустой ответ от API МС, делать assert не с чем


def test__partial_clear_invoice(client, create_invoice, get__invoice_data__dto):
    created_invoice = create_invoice()
    _created_invoice_data = get__invoice_data__dto()
    statistics_data = _created_invoice_data.statisticsByPlatforms[0].dict()
    # Удалить лишние поля из статистики
    for key in ["amount", "impsFact", "impsPlan", "platformName", "platformOwnedByAgency", "platformType", "price"]:
        statistics_data.pop(key, None)
    request_data = PartialClearInvoiceWebApiDto(
        initialContracts=[initital_contract.initialContractId for initital_contract in _created_invoice_data.initialContractsData],
        statisticsByPlatforms=[PartialClearInvoiceStatisticsItem(**statistics_data)],
    )

    client.partial_clear_invoice(created_invoice.id, request_data)
    # пустой ответ от API МС, делать assert не с чем


def test__delete_invoice_initial_contracts(client, create_invoice, get__invoice_data__dto):
    created_invoice = create_invoice()
    _created_invoice_data = get__invoice_data__dto()

    request_data = PartialClearInvoiceInitialContractsRequest(
        initialContracts=[
            initital_contract.initialContractId for initital_contract in _created_invoice_data.initialContractsData
        ]
    )

    client.delete_invoice_initial_contracts(created_invoice.id, request_data)
    # пустой ответ от API МС, делать assert не с чем


def test__delete_invoice_statistics(client, create_invoice, get__invoice_data__dto):
    created_invoice = create_invoice()
    _created_invoice_data = get__invoice_data__dto()
    statistics_data = _created_invoice_data.statisticsByPlatforms[0].dict()
    for key in ["amount", "impsFact", "impsPlan", "platformName", "platformOwnedByAgency", "platformType", "price"]:
        statistics_data.pop(key, None)
    request_data = PartialClearInvoiceStatisticsRequest(
        statistics=[PartialClearInvoiceStatisticsItem(**statistics_data)]
    )
    client.delete_invoice_statistics(created_invoice.id, request_data)
    # пустой ответ от API МС, делать assert не с чем


def test__delete_invoice(client, create_invoice):
    created_invoice = create_invoice()
    request_data = EntityIdResponse(id=created_invoice.id)
    client.delete_invoice(request_data)
    # пустой ответ от API МС, делать assert не с чем

