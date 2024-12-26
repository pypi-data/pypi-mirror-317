import pytest

from .conftest import CREATIVE_IDS

from ord_mediascout_client import (
    GetCreativeGroupsRequest,
    CreativeGroupResponse,
    CreatedCreativeResponse,
    CreativeForm,
    CreativeStatus,
    DeleteRestoreCreativeWebApiDto,
    EditCreativeRequest,
    GetCreativesWebApiDto,
    GetCreativeStatusWebApiDto,
)


@pytest.fixture(scope="module")
def create_mediadata_creative(client, get__creative_data__dto, get__creative_media_data__dto):
    def _create_mediadata_creative():
        request_data = get__creative_data__dto(form=CreativeForm.Banner, mediaData=[get__creative_media_data__dto()])

        response_data = client.create_creative(request_data)

        return response_data
    return _create_mediadata_creative


@pytest.fixture(scope="module")
def create_textdata_creative(client, get__creative_data__dto, get__creative_text_data__dto):
    def _create_textdata_creative():
        request_data = get__creative_data__dto(form=CreativeForm.Text, textData=[get__creative_text_data__dto()])

        response_data = client.create_creative(request_data)

        return response_data
    return _create_textdata_creative


def test__create_mediadata_creative(client, get__creative_data__dto, get__creative_media_data__dto):
    request_data = get__creative_data__dto(mediaData=[get__creative_media_data__dto()])

    response_data = client.create_creative(request_data)

    assert response_data is not None
    assert response_data.id is not None
    assert isinstance(response_data, CreatedCreativeResponse)


def test__create_textdata_creative(client, get__creative_data__dto, get__creative_text_data__dto):
    request_data = get__creative_data__dto(form=CreativeForm.Text, textData=[get__creative_text_data__dto()])

    response_data = client.create_creative(request_data)

    assert response_data is not None
    assert response_data.id is not None
    assert isinstance(response_data, CreatedCreativeResponse)


def test__get_creative_status(client, create_mediadata_creative):
    created_mediadata_creative = create_mediadata_creative()
    request_data = GetCreativeStatusWebApiDto(creativeId=created_mediadata_creative.id)

    response_data = client.get_creative_status(request_data)

    assert response_data is not None
    assert response_data.erid == created_mediadata_creative.erid


def test__get_creatives(client):
    request_data = GetCreativesWebApiDto(status=CreativeStatus.Registering)

    response_data = client.get_creatives(request_data)

    assert len(response_data) > 0
    for creative in response_data:
        assert creative.id is not None
        assert creative.status == CreativeStatus.Registering


def test__get_one_creative(client):
    request_data = GetCreativesWebApiDto(ids=CREATIVE_IDS)

    response_data = client.get_creatives(request_data)

    assert len(response_data) == len(CREATIVE_IDS)
    for creative in response_data:
        assert creative.id is not None
        assert creative.id in CREATIVE_IDS


def test__edit_creative(client, create_mediadata_creative):
    created_mediadata_creative = create_mediadata_creative()
    advertiser_urls = ['https://clisite1-edit.ru', 'https://clisite2-edit.ru']
    request_data = EditCreativeRequest(
        id=created_mediadata_creative.id,
        creativeGroupId=created_mediadata_creative.creativeGroupId,
        advertiserUrls=advertiser_urls,
        overwriteExistingCreativeMedia=False,
    )
    filtered_data = request_data.dict(exclude_none=True)
    for field in request_data.__fields__:
        if field not in filtered_data:
            delattr(request_data, field)

    response_data = client.edit_creative(request_data)

    assert response_data is not None
    assert response_data.id == created_mediadata_creative.id
    assert sorted(response_data.advertiserUrls) == sorted(advertiser_urls)


def test__edit_creative_group(client, create_mediadata_creative):
    created_mediadata_creative = create_mediadata_creative()
    # Так как при создании креатива возвращаются не все данные,
    # нужно получить креатив для извлечения параметров для запроса на редактирование
    request_creative = GetCreativesWebApiDto(ids=[created_mediadata_creative.id])
    creative = client.get_creatives(request_creative)[0]
    description = "Edited description"
    request_creative_group = CreativeGroupResponse(
        creativeGroupId=creative.creativeGroupId,
        creativeGroupName=creative.creativeGroupName,
        finalContractId=creative.finalContractId,
        isSelfPromotion=creative.isSelfPromotion,
        type=creative.type,
        form=creative.form,
        isSocial=creative.isSocial,
        isNative=creative.isNative,
        description=description,
    )

    response_data = client.edit_creative_group(request_creative_group)

    assert response_data is not None
    assert response_data.creativeGroupId == creative.creativeGroupId
    assert response_data.description == description


def test__get_creative_groups(client, get__creative_data__dto):
    creative_data = get__creative_data__dto()
    request_data = GetCreativeGroupsRequest(
        finalContractId=creative_data.finalContractId,
        initialContractId=creative_data.initialContractId,
    )

    response_data = client.get_creative_groups(request_data)

    assert len(response_data) > 0
    for creative_group in response_data:
        assert creative_group.creativeGroupId is not None


def test__delete_and_restore_creative(client, create_mediadata_creative):
    created_mediadata_creative = create_mediadata_creative()
    request_data = DeleteRestoreCreativeWebApiDto(erid=created_mediadata_creative.erid)
    client.delete_creative(request_data)
    client.restore_creative(request_data)
    # пустой ответ от API МС, делать assert не с чем


def test__delete_creative(client, create_mediadata_creative):
    created_mediadata_creative = create_mediadata_creative()
    request_data = DeleteRestoreCreativeWebApiDto(erid=created_mediadata_creative.erid)
    client.delete_creative(request_data)
    # пустой ответ от API МС, делать assert не с чем
