import logging
import random
import string
from datetime import datetime, timedelta
import time
import pytest
from faker import Faker
from dotenv import load_dotenv
import os

from ord_mediascout_client import (
    CreateAdvertisingContainerRequest,
    CreateDelayedFeedElementsBulkRequest,
    CreateFeedElementsRequest,
    CreateFeedElement,
    CreativeForm,
    CreateCreativeRequest,
    CreateCreativeMediaDataItem,
    CreateCreativeTextDataItem,
    CreateClientRequest,
    CreateFinalContractRequest,
    CreateInitialContractRequest,
    CreateInvoiceRequest,
    CreateInvoicelessStatisticsRequest,
    CreateOuterContractRequest,
    CreatePlatformRequest,
    CampaignType,
    ContractType,
    ContractSubjectType,
    EditCreativeMediaDataItem,
    EditCreativeTextDataItem,
    EditDelayedFeedElementsBulkRequest,
    EditFeedElementsRequest,
    EditFeedElementWebApiDto,
    FileType,
    InvoicePartyRole,
    InvoiceInitialContractItem,
    InvoiceStatisticsByPlatformsItem,
    InvoicelessStatisticsByPlatforms,
    ORDMediascoutClient,
    ORDMediascoutConfig,
    PlatformType,
    TargetAudienceParamType,
    ClientRelationshipType,
    LegalForm,
)


logging.getLogger('faker').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)


load_dotenv()
faker = Faker()

# Setup Tests Data
CONTRACT__CLIENT_ID =  os.getenv('CLIENT_ID')
CONTRACT__INITIAL_CONTRACT__CLIENT_ID = os.getenv('INITIAL_CONTRACT_CLIENT_ID')
CONTRACT__CONTRACTOR_ID = os.getenv('CONTRACTOR_ID')
FINAL_CONTRACT_ID = os.getenv('FINAL_CONTRACT_ID')
INITIAL_CONTRACT_ID = os.getenv('INITIAL_CONTRACT_ID')
ER_ID = os.getenv('ER_ID')
CREATIVE_IDS = os.getenv('CREATIVE_IDS').split(',')
IMAGE_SRC_URL = os.getenv('IMAGE_SRC_URL')
FEED_ID = os.getenv('FEED_ID')
FEED__ELEMENTS = os.getenv('FEED_ELEMENTS').split(',')
FEED__MEDIA_IDS = os.getenv('FEED_MEDIA_IDS').split(',')


@pytest.fixture(scope='module')
def client():
    config = ORDMediascoutConfig()
    return ORDMediascoutClient(config)


@pytest.fixture(scope='session', autouse=True)
def faker_session_locale():
    return ['ru_RU']


@pytest.fixture(scope='session', autouse=True)
def faker_seed():
    return int(time.time())


# Client
@pytest.fixture(scope="module")
def get__client_data__dto():
    def _client_data(**kwargs):
        data = {
            'createMode': ClientRelationshipType.DirectClient,
            'legalForm': LegalForm.JuridicalPerson,
            'inn': '7720805643',
            'name': 'Тест клиент2',
            'mobilePhone': '+79161234567',
            'epayNumber': '12333',
            'regNumber': '54556',
            'oksmNumber': '44563',
        }
        data.update(kwargs)
        return CreateClientRequest(**data)

    return _client_data


# Contract
@pytest.fixture(scope="module")
def get__final_contract_data__dto():
    def _final_contract_data(**kwargs):
        data = {
            'number': f'{random_string()}-{random.randrange(111, 9999)}',
            'date': random_date(year='2024', month='05'),
            'amount': random.randrange(1000, 100000),
            'isAgentActingForPublisher': True,
            'type': ContractType.ServiceAgreement,
            'subjectType': ContractSubjectType.Distribution,
            # 'actionType': MediationActionType.Contracting,
            'parentMainContractId': '',
            'clientId': CONTRACT__CLIENT_ID,
        }
        data.update(kwargs)
        return CreateFinalContractRequest(**data)

    return _final_contract_data


@pytest.fixture(scope="module")
def get__initial_contract_data__dto():
    def _initial_contract_data(**kwargs):
        data = {
            'number': f'{random_string()}-{random.randrange(111, 9999)}',
            'date': random_date(year='2024', month='05'),
            'amount': random.randrange(1000, 100000),
            'isAgentActingForPublisher': True,
            'type': ContractType.ServiceAgreement,
            'subjectType': ContractSubjectType.Distribution,
            # 'actionType': MediationActionType.Contracting,
            'contractorId': CONTRACT__CONTRACTOR_ID,
            'clientId': CONTRACT__INITIAL_CONTRACT__CLIENT_ID,
            'finalContractId': FINAL_CONTRACT_ID,
        }
        data.update(kwargs)
        return CreateInitialContractRequest(**data)

    return _initial_contract_data


@pytest.fixture(scope="module")
def get__outer_contract_data__dto():
    def _outer_contract_data(**kwargs):
        data = {
            'number': f'{random_string()}-{random.randrange(111, 9999)}',
            'date': random_date(year='2024', month='05'),
            'amount': random.randrange(1000, 100000),
            'isAgentActingForPublisher': True,
            'type': ContractType.ServiceAgreement,
            'subjectType': ContractSubjectType.Distribution,
            # 'actionType': MediationActionType.Contracting,
            'contractorId': CONTRACT__CLIENT_ID,
            'isRegReport': True,
        }
        data.update(kwargs)
        return CreateOuterContractRequest(**data)

    return _outer_contract_data


# Invoice
@pytest.fixture(scope="module")
def get__invoice_randoms():
    def _get__invoice_randoms(**kwargs):
        start_date = random_date(year=kwargs.get('year') or '2024', month=kwargs.get('month') or '10')
        start_date_fact = random_date(start_date=start_date)
        end_date_plan = random_date(start_date=start_date_fact)
        end_date_fact = random_date(start_date=end_date_plan)
        end_date = random_date(start_date=end_date_fact)
        imps_plan = random.randrange(1000, 100000)

        return start_date, start_date_fact, end_date_plan, end_date_fact, end_date, imps_plan
    return _get__invoice_randoms


@pytest.fixture(scope="module")
def get__initial_contracts_data__dto():
    def _initial_contracts_data(**kwargs):
        data = {
            'initialContractId': INITIAL_CONTRACT_ID,
            'amount': 1000.00,
        }
        data.update(kwargs)
        return InvoiceInitialContractItem(**data)

    return _initial_contracts_data


@pytest.fixture(scope="module")
def get__statistics_by_platforms__dto(get__invoice_randoms):
    def _statistics_by_platforms(**kwargs):
        start_date, start_date_fact, end_date_plan, end_date_fact, end_date, imps_plan = get__invoice_randoms(
            year='2024', month='10'
        )
        data = {
                'initialContractId': INITIAL_CONTRACT_ID,
                'erid': ER_ID,
                'platformUrl': 'http://www.testplatform.ru',
                'platformName': 'Test Platform 1',
                'platformType': PlatformType.Site,
                'platformOwnedByAgency': False,
                'impsPlan': imps_plan,
                'impsFact': imps_plan,
                'startDatePlan': start_date,
                'startDateFact': start_date_fact,
                'endDatePlan': end_date_plan,
                'endDateFact': end_date_fact,
                'amount': random.randrange(100, 1000),
                'price': 0.5,
        }
        data.update(kwargs)
        return InvoiceStatisticsByPlatformsItem(**data)

    return _statistics_by_platforms


@pytest.fixture(scope="module")
def get__invoice_data__dto(get__invoice_randoms, get__initial_contracts_data__dto, get__statistics_by_platforms__dto):
    def _invoice_data(**kwargs):
        start_date, start_date_fact, end_date_plan, end_date_fact, end_date, imps_plan = get__invoice_randoms(
            year='2024', month='10'
        )
        data = {
            'number': 'INV-{}'.format(random.randrange(11111111, 99999999)),
            'date': start_date,
            'contractorRole': InvoicePartyRole.Rr,
            'clientRole': InvoicePartyRole.Ra,
            'amount': random.randrange(10000, 50000),
            'startDate': start_date,
            'endDate': end_date,
            'finalContractId': FINAL_CONTRACT_ID,
            'initialContractsData': [get__initial_contracts_data__dto(), ],
            'statisticsByPlatforms': [get__statistics_by_platforms__dto(), ]
        }
        data.update(kwargs)

        return CreateInvoiceRequest(**data)

    return _invoice_data


# Creative
@pytest.fixture(scope="module")
def get__creative_media_data__dto():
    def _creative_media_data(**kwargs):
        rnd = random.randrange(111, 9999)
        data = {
            'fileName': 'logo.svg',
            'fileType': FileType.Image,
            # fileContentBase64="string",
            'srcUrl': IMAGE_SRC_URL,
            'description': f'Тестовый баннер {rnd}',
            'isArchive': False,
        }
        data.update(kwargs)
        return CreateCreativeMediaDataItem(**data)
    return _creative_media_data


@pytest.fixture(scope="module")
def get__creative_text_data__dto():
    def _creative_text_data(**kwargs):
        rnd = random.randrange(111, 9999)
        data = {'textData': f'Creative {rnd} text data test'}
        data.update(kwargs)
        return CreateCreativeTextDataItem(**data)
    return _creative_text_data


@pytest.fixture(scope="module")
def get__creative_data__dto():
    def _creative_data(**kwargs):
        rnd = random.randrange(111, 9999)
        data = {
                'finalContractId': FINAL_CONTRACT_ID,
                'initialContractId': INITIAL_CONTRACT_ID,
                'creativeGroupName': f'_generated_creative_group_name_{random.randint(1000, 99999)}',
                'type': CampaignType.CPM,
                'form': CreativeForm.Banner,
                'advertiserUrls': ['https://clisite1.ru', 'https://clisite2.ru'],
                'description': f'Test mediadata creative {rnd}',
                'targetAudienceParams': [],
                'isSelfPromotion': False,
                'isNative': False,
                'isSocial': False,
                'mediaData': [],
                'textData': [],
        }
        data.update(kwargs)
        return CreateCreativeRequest(**data)

    return _creative_data


# Platform
@pytest.fixture(scope="module")
def get__platform_data__dto():
    def _platform_data(**kwargs):
        rnd = random.randrange(100000, 999999)
        data = {
            'name': f'Test Platform {rnd}',
            'type': PlatformType.Site,
            'url': f'http://www.testplatform{rnd}.ru/',
            'isOwner': True,
        }
        data.update(kwargs)
        return CreatePlatformRequest(**data)

    return _platform_data


# Feed
@pytest.fixture(scope="module")
def get__feed_element__dto(get__creative_text_data__dto):
    def _feed_element(**kwargs):
        data = {
            'nativeCustomerId': faker.uuid4(),
            'description': faker.text(30),
            'advertiserUrls': [faker.url()[:-1]],
            'textData': [get__creative_text_data__dto(), ],
        }
        data.update(kwargs)
        return CreateFeedElement(**data)

    return _feed_element

@pytest.fixture(scope="module")
def get__feed_elements_data__dto(get__feed_element__dto):
    def _feed_elements_data(**kwargs):
        data = {
            'feedName': 'test_feed',
            'feedNativeCustomerId': 'test_feed_id',
            'feedElements': [get__feed_element__dto()],
        }
        data.update(kwargs)
        return CreateFeedElementsRequest(**data)

    return _feed_elements_data


@pytest.fixture(scope="module")
def get__bulk_feed_elements_data__dto(get__creative_media_data__dto):
    def _bulk_feed_elements_data(**kwargs):
        rnd = random.randrange(100000, 999999)
        data = {
            'feedElements': [
                {
                    #"feedId": "string",
                    'feedName': f'bulk_test_feed {rnd}',
                    'feedNativeCustomerId': f'test_feed_id {rnd}',
                    'nativeCustomerId': faker.uuid4(),
                    'description': faker.text(30),
                    'advertiserUrls': [faker.url()[:-1]],
                    'mediaData': [get__creative_media_data__dto(), ],
                }
                for _ in range(3)
            ],
        }

        # Если в kwargs передан feedElements, то обновить поля в каждом элементе data['feedElements']
        if 'feedElements' in kwargs:
            for index, feed_element in enumerate(kwargs['feedElements']):
                if index < len(data['feedElements']):
                    # Обновить ключи для соответствующего элемента в data['feedElements']
                    for key, value in feed_element.items():
                        data['feedElements'][index][key] = value
            # Удалить 'feedElements' из kwargs после обработки
            kwargs.pop('feedElements')

        data.update(kwargs)

        return CreateDelayedFeedElementsBulkRequest(**data)

    return _bulk_feed_elements_data


@pytest.fixture(scope="module")
def get__edit_creative_media_data__dto():
    def _edit_creative_media_data(**kwargs):
        rnd = random.randrange(111, 9999)
        data = {
            'fileName': 'logo.svg',
            'fileType': FileType.Image,
            # fileContentBase64="string",
            'srcUrl': IMAGE_SRC_URL,
            'description': f'Тестовый баннер {rnd}',
            'isArchive': False,
        }
        data.update(kwargs)
        return EditCreativeMediaDataItem(**data)
    return _edit_creative_media_data


@pytest.fixture(scope="module")
def get__edit_creative_text_data__dto():
    def _edit_creative_text_data(**kwargs):
        rnd = random.randrange(111, 9999)
        data = {'textData': f'Creative {rnd} text data test'}
        data.update(kwargs)
        return EditCreativeTextDataItem(**data)
    return _edit_creative_text_data


@pytest.fixture(scope="module")
def get__bulk_edit_feed_elements_data__dto(get__edit_creative_media_data__dto):
    def _bulk_edit_feed_elements_data(**kwargs):
        rnd = random.randrange(100000, 999999)
        data = {
            'feedElements': [
                {
                    "id": feed_id,
                    "feedId": FEED_ID,
                    'feedName': f'bulk_test_feed Edit {rnd}',
                    'feedNativeCustomerId': f'feedNativeCustomerId__{rnd}',
                    'nativeCustomerId': customer_id,
                    'description': faker.text(30),
                    'advertiserUrls': [url],
                    'OverwriteExistingCreativeMedia': overwrite,
                    'mediaData': [get__edit_creative_media_data__dto(
                        id=media_id,
                        fileName=f'logo{rnd}.svg',
                        actionType='Edit',
                        description=f'Тестовый баннер {rnd}'
                    )],
                }
                for feed_id, customer_id, url, overwrite, media_id in [
                    (
                     FEED__ELEMENTS[0],
                     "60e2932f-85ae-44fe-885f-70086e2d957d",
                     "https://www.haley-salazar.com",
                     True,
                     FEED__MEDIA_IDS[0]
                     ),
                    (
                     FEED__ELEMENTS[1],
                     "79608f17-29ab-4ae6-950b-1dc2c249d56c",
                     "http://www.friedman.com",
                     True,
                     FEED__MEDIA_IDS[1]
                    ),
                    (
                     FEED__ELEMENTS[2],
                     "489c3bcb-f6fc-40ac-97a2-a7725a674f86",
                     "http://smith.com",
                     False,
                     FEED__MEDIA_IDS[2]
                    )
                ]
            ]
        }

        # Если в kwargs передан feedElements, то обновить поля в каждом элементе data['feedElements']
        if 'feedElements' in kwargs:
            for index, feed_element in enumerate(kwargs['feedElements']):
                if index < len(data['feedElements']):
                    # Обновить ключи для соответствующего элемента в data['feedElements']
                    for key, value in feed_element.items():
                        data['feedElements'][index][key] = value
            # Удалить 'feedElements' из kwargs после обработки
            kwargs.pop('feedElements')

        data.update(kwargs)

        return EditDelayedFeedElementsBulkRequest(**data)

    return _bulk_edit_feed_elements_data


@pytest.fixture(scope="module")
def get__edit_feed_element__dto(get__creative_text_data__dto):
    def _edit_feed_element(**kwargs):
        data = {
            'id': 'string',
            'description': faker.text(30),
            'advertiserUrls': [faker.url()[:-1]],
            'overwriteExistingCreativeMedia': False,
            'textData': [get__creative_text_data__dto(), ],
        }
        data.update(kwargs)
        return EditFeedElementWebApiDto(**data)

    return _edit_feed_element


@pytest.fixture(scope="module")
def get__edit_feed_elements_data__dto(get__edit_feed_element__dto):
    def _edit_feed_elements_data(**kwargs):
        # Если в kwargs передан feedElements, собираем его поля со значениями в feed_elements
        feed_elements = {}
        if 'feedElements' in kwargs:
            for key, value in kwargs['feedElements'][0].items():
                feed_elements[key] = value
            kwargs.pop('feedElements')
        data = {
            'feedName': 'edit_test_feed',
            'feedNativeCustomerId': 'test_feed_id',
            'feedElements': [get__edit_feed_element__dto(**feed_elements)],
        }

        data.update(kwargs)

        return EditFeedElementsRequest(**data)

    return _edit_feed_elements_data


@pytest.fixture(scope="module")
def get__container_data__dto():
    def _container_data(**kwargs):
        data = {
            'feedNativeCustomerId': 'string',
            'finalContractId': FINAL_CONTRACT_ID,
            'initialContractId': INITIAL_CONTRACT_ID,
            'name': f'Тестовый контейнер {random.randrange(10000, 999999)}',
            'nativeCustomerId': 'string',
            'type': CampaignType.CPM,
            'form': CreativeForm.Banner,
            'targetAudienceParams': [
                {
                    'type': TargetAudienceParamType.Geo,
                    'values': [
                        '75'
                    ]
                }
            ],
            'description': 'Описание тестового контейнера',
            'isNative': True,
            'isSocial': True
        }
        data.update(kwargs)
        return CreateAdvertisingContainerRequest(**data)

    return _container_data


# Statistics
@pytest.fixture(scope="module")
def get__invoiceless_statistics_by_platforms__dto():
    def _invoiceless_statistics_by_platforms(**kwargs):
        data = {
                'erid': 'Kra23f3QL',
                'platformUrl': 'http://www.testplatform.ru',
                'platformName': 'Test Platform 1',
                'platformType': 'Site',
                'platformOwnedByAgency': False,
                'type': 'CPM',
                'impsPlan': 10000,
                'impsFact': 100,
                'startDatePlan': '2023-06-01',
                'startDateFact': '2023-06-01',
                'endDatePlan': '2023-06-20',
                'endDateFact': '2023-06-20',
                'amount': 50000,
                'price': 5,
            }
        data.update(kwargs)
        return InvoicelessStatisticsByPlatforms(**data)
    return _invoiceless_statistics_by_platforms


@pytest.fixture(scope="module")
def get__statistics_data__dto(get__invoiceless_statistics_by_platforms__dto):
    def _statistics_data(**kwargs):
        data = {'statistics': [get__invoiceless_statistics_by_platforms__dto()]}
        data.update(kwargs)
        return CreateInvoicelessStatisticsRequest(**data)

    return _statistics_data


# Utils
def parse_relative_value(value, base, lower_limit=None, upper_limit=None):
    """
    Функция для обработки строковых значений с "+" и "-" и вычисления целевого значения на основе base.
    """
    if isinstance(value, str) and value.startswith(("+", "-", "+-")):
        if value.startswith("+-"):
            delta = int(value[2:])
            result = random.randint(base - delta, base + delta)
        elif value.startswith("+"):
            delta = int(value[1:])
            result = random.randint(base, base + delta)
        elif value.startswith("-"):
            delta = int(value[1:])
            result = random.randint(base - delta, base)
    else:
        # Если значение не является строкой с "+", "-" или "+-", то использовать указанное значение как есть.
        result = int(value)

    # Проверка, чтобы результат не выходил за границы
    if lower_limit is not None:
        result = max(lower_limit, result)
    if upper_limit is not None:
        result = min(upper_limit, result)

    return result


def random_date(year=None, month=None, start_date=None):
    """
    Генерация даты в формате '2024-10-23'
    Примеры использования:
    random_date(year='+3', month='05'))        # Рандомная дата от текущего до +3 лет, в мае
    random_date(year='+3', month='05'))        # Рандомная дата от текущего до +3 лет, в мае
    random_date(year='2024', month='-5'))      # Рандомная дата в 2024 году, месяцы -5 от текущего (например, текущий - октябрь, результат - май)
    random_date(year='+-5', month='+-2'))      # Рандомная дата +/- 5 лет и +/- 2 месяца от текущего
    random_date(year='+-5', month='+-2', start_date='2023-05-16'))  # Аналогично, но от указанной стартовой даты
    """
    # Установить базовую дату
    if start_date:
        base_date = datetime.strptime(start_date, '%Y-%m-%d')
    else:
        base_date = datetime.now()

    year = year or base_date.year
    month = month or base_date.month

    # Определить год и месяц на основе переданных значений или устанавить случайные значения
    year = parse_relative_value(year, base_date.year) if year is not None else random.randint(2000, datetime.now().year)
    month = parse_relative_value(month, base_date.month, 1, 12) if month is not None else random.randint(1, 12)

    # Если месяц за пределами 1-12, то скорректировать значения года и месяца
    if month < 1:
        year -= 1
        month = 12 + month
    elif month > 12:
        year += 1
        month = month - 12

    # Определить начальный день
    start_day = base_date.day if start_date else 1

    # Создать базовую дату и добавить случайное количество дней
    base_date = datetime(year=year, month=month, day=start_day)
    random_days_to_add = random.randint(1, 3)
    new_date = base_date + timedelta(days=random_days_to_add)

    return new_date.strftime('%Y-%m-%d')


def random_string(length=3):
    """
    Генератор рандомной строки
    """
    return ''.join(random.choices(string.ascii_uppercase, k=length))


def _serialize(obj, seen=None):
    """
    Рекурсивная функция для сериализации объекта в словарь.
    Обрабатывает объекты со словарями и списками, а также
    использует __dict__ для вложенных объектов.
    """
    from enum import Enum


    if seen is None:
        seen = set()

    # Проверка на Enum - получаем его значение
    if isinstance(obj, Enum):
        return obj.value

    # Проверка на тип списка
    if isinstance(obj, list):
        return [_serialize(item, seen) for item in obj]

    # Проверка на тип словаря
    elif isinstance(obj, dict):
        return {key: _serialize(value, seen) for key, value in obj.items()}

    # Проверка на объекты с __dict__, чтобы предотвратить бесконечную рекурсию
    elif hasattr(obj, "__dict__"):
        obj_id = id(obj)
        if obj_id in seen:
            return f"<RecursionError: {obj.__class__.__name__}>"

        seen.add(obj_id)  # Добавить объект в "просмотренные"

        obj_dict = {key: _serialize(value, seen) for key, value in obj.__dict__.items()}
        obj_dict["__class__"] = obj.__class__.__name__  # добавить имя класса
        return obj_dict

    else:
        return obj


def print_obj(obj):
    """
    Распечатать объект в удобочитаемом виде
    """
    from pprint import pprint

    serialized_data = _serialize(obj)
    pprint(serialized_data, width=80)
    print()
