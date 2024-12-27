import pytest
from pandas import DataFrame

from business_central_kon.services import (
    CustomerService,
    CustomerLedgerEntryService,
    VendorService,
    VendorLedgerEntryService,
    ItemService,
    ItemLedgerEntryService,
    GeneralLedgerService,
    GeneralLedgerEntriesService,
    SalesInvoiceService,
    SalesInvoiceLinesService,
    ILEOriginEntriesService,
    SalesOrderService,
    SalesOrderLinesService,
    LocationService,
    BomHeaderService,
    BomLinesService,
    ResponsibilityMatrixService,
    SalesPersonService,
    ProductGroupService,
    ExportOrderService,
    SampleOrderService,
    TransferOrderService,
    TransferOrderLinesService
)
from business_central_kon.session import BusinessCentralSession

# List of services to test
SERVICES = [
    CustomerService,
    CustomerLedgerEntryService,
    VendorService,
    VendorLedgerEntryService,
    ItemService,
    ItemLedgerEntryService,
    GeneralLedgerService,
    GeneralLedgerEntriesService,
    SalesInvoiceService,
    SalesInvoiceLinesService,
    ILEOriginEntriesService,
    SalesOrderService,
    SalesOrderLinesService,
    LocationService,
    BomHeaderService,
    BomLinesService,
    ResponsibilityMatrixService,
    SalesPersonService,
    ProductGroupService,
    ExportOrderService,
    SampleOrderService,
    TransferOrderService,
    TransferOrderLinesService
]


@pytest.fixture
def api_session():
    """
    Fixture to create a real session with the Business Central API.
    Ensure valid credentials and base URL are provided.
    """
    # Replace these with your actual credentials and API base URL
    username = ""
    password = ""
    base_url = ""
    return BusinessCentralSession(username=username, password=password, base_url=base_url)


@pytest.mark.parametrize("service_class", SERVICES)
def test_get_top_ten_for_service(api_session, service_class):
    """
    Test the get_top_ten method for each service and ensure a non-empty DataFrame is returned.
    :param api_session: BusinessCentralSession instance.
    :param service_class: The service class to test.
    """
    # Instantiate the service
    service = service_class(api_session)

    # Fetch top 10 records
    df = service.get_top_ten(as_dataframe=True)

    # Assertions
    assert isinstance(df, DataFrame), f"{service.SERVICE_NAME}: Result is not a DataFrame"
    assert not df.empty or len(df) <= 10, (
        f"{service.SERVICE_NAME}: DataFrame is either empty or has more than 10 items"
    )
