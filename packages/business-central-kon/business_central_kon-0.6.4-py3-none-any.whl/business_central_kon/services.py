import pandas as pd

from .session import BusinessCentralSession


class BaseService:
    """
    Base class for interacting with Business Central API endpoints.
    Each subclass should define the SERVICE_NAME for the respective API endpoint.
    """

    SERVICE_NAME = ""

    def __init__(self, session: BusinessCentralSession) -> None:
        """
        Initialize the service with a session.
        :param session: An instance of BusinessCentralSession.
        """

        if not self.SERVICE_NAME:
            raise ValueError("SERVICE_NAME must be defined in the subclass.")
        self.session = session

    def get_data(self, filters: str = "", columns: dict = None, as_dataframe: bool = False) -> list | pd.DataFrame:
        """
        Fetch data from the API endpoint with optional filters and column selection.
        :param filters: OData filter string for query conditions.
        :param columns: Dict of column names to select.
        :param as_dataframe: Return results as a pandas DataFrame if True, otherwise as a list.
        :return: List or DataFrame of fetched data.
        """

        return self.session.fetch_data(
            service_name=self.SERVICE_NAME,
            filters=filters, columns=columns,
            as_dataframe=as_dataframe
        )

    def get_top_ten(self, as_dataframe: bool = False) -> list | pd.DataFrame:
        """
        Fetch the top 10 records from the API endpoint without any filters or column selection.
        :param as_dataframe: Return results as a pandas DataFrame if True, otherwise as a list.
        :return: List or DataFrame of the top 10 records.
        """
        # Construct the URL with $top=10
        url = self.session._build_query_url(service_name=self.SERVICE_NAME)
        url = f"{url}?$top=10"

        # Fetch data directly
        data = self.session._fetch_paginated_data(url)

        if as_dataframe:
            return self.session._convert_to_dataframe(data)

        return data


class CustomerService(BaseService):
    SERVICE_NAME = "ksppl_customers"


class CustomerLedgerEntryService(BaseService):
    SERVICE_NAME = "ksppl_customer_ledger_entries"


class VendorService(BaseService):
    SERVICE_NAME = "ksppl_vendors"


class VendorLedgerEntryService(BaseService):
    SERVICE_NAME = "ksppl_vendor_ledger_entries"


class ItemService(BaseService):
    SERVICE_NAME = "ksppl_items"


class ItemLedgerEntryService(BaseService):
    SERVICE_NAME = "ksppl_item_ledger_entries"


class GeneralLedgerService(BaseService):
    SERVICE_NAME = "ksppl_general_ledgers"


class GeneralLedgerEntriesService(BaseService):
    SERVICE_NAME = "ksppl_general_ledger_entries"


class SalesInvoiceService(BaseService):
    SERVICE_NAME = "ksppl_sales_invoices"


class SalesInvoiceLinesService(BaseService):
    SERVICE_NAME = "ksppl_sales_invoice_lines"


class ILEOriginEntriesService(BaseService):
    SERVICE_NAME = "ksppl_ile_origin_detail"


class SalesOrderService(BaseService):
    SERVICE_NAME = "ksppl_sales_orders"


class SalesOrderLinesService(BaseService):
    SERVICE_NAME = "ksppl_sales_order_lines"


class LocationService(BaseService):
    SERVICE_NAME = "ksppl_locations"


class BomHeaderService(BaseService):
    SERVICE_NAME = "ksppl_boms"


class BomLinesService(BaseService):
    SERVICE_NAME = "ksppl_bom_lines"


class ResponsibilityMatrixService(BaseService):
    SERVICE_NAME = "ksppl_responsibility_matrix"


class SalesPersonService(BaseService):
    SERVICE_NAME = "ksppl_sales_people"


class ProductGroupService(BaseService):
    SERVICE_NAME = "ksppl_product_groups"


class SampleOrderService(BaseService):
    SERVICE_NAME = "ksppl_sample_orders"


class ExportOrderService(BaseService):
    SERVICE_NAME = "ksppl_export_orders"


class TransferOrderService(BaseService):
    SERVICE_NAME = "ksppl_transfer_orders"


class TransferOrderLinesService(BaseService):
    SERVICE_NAME = "ksppl_transfer_order_lines"