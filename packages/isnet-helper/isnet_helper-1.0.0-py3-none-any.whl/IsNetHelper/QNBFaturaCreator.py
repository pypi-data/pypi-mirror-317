from time import sleep
from xml.etree import ElementTree
import requests
from zeep.client import Client
import datetime
from IsNetHelper.utils.utils import get_new_invoice_number
from IsNetHelper.models.Request import ArchiveInvoiceDetails, EArchiveInvoices, EArchiveInvoice, EArchiveInvoiceDetail, PagingRequest, Product, Receiver, ReceiverAddress, SearchArchiveInvoiceResultSet, SendArchiveInvoiceRequest, SendArchiveInvoiceRequestWithoutInvoiceNumber

class IsNetHelper:
    
    def __init__(self) -> None:
        self.session = requests.Session()
        self.INVOICE_WSDL_URL = self.get_invoice_wsdl_url(is_test=True)
        self.client = Client(self.INVOICE_WSDL_URL)
        self.address_client = Client(self.get_address_wsdl_url(is_test=True))
        
    def get_invoice_wsdl_url(self, is_test):
        if is_test:
            return "http://einvoiceservicetest.isnet.net.tr/InvoiceService/ServiceContract/InvoiceService.svc?singleWsdl"
        return "https://einvoiceservice.isnet.net.tr/InvoiceService/ServiceContract/InvoiceService.svc?singleWsdl"


    def get_address_wsdl_url(self, is_test):
        if is_test:
            return "http://einvoiceservicetest.isnet.net.tr/AddressBookService/ServiceContract/AddressBookService.svc?singleWsdl"
        return "http://einvoiceservice.isnet.net.tr/AddressBookService/ServiceContract/AddressBookService.svc?singleWsdl"


    def request(self, type: str, url: str, data: str, **kwargs):
        headers = kwargs.pop("headers", {})
        
        headers["Content-Type"] = "text/xml; charset=utf-8"
        return self.session.request(type, url, data=data, headers=headers, **kwargs)
    
    def search_archive_invoice(self, company_tax_code: str, is_cancelled: bool = False, paging_request: PagingRequest = PagingRequest(PageNumber=1, RecordsPerPage=1), result_set: SearchArchiveInvoiceResultSet = SearchArchiveInvoiceResultSet(
        IsAdditionalTaxIncluded=False,
        IsArchiveIncluded=False,
        IsAttachmentIncluded=False,
        IsExternalUrlIncluded=False,
        IsHtmlIncluded=False,
        IsInvoiceDetailIncluded=False,
        IsPDFIncluded=True,
        IsTextIncluded=False
    ), ExternalArchiveInvoiceCode: str = None):
        request = self.client.get_type("ns2:SearchArchiveInvoiceRequest")()  # WSDL'deki tam tipi alın
        request.CompanyTaxCode = company_tax_code
        request.IsCancelled = is_cancelled
        request.PagingRequest = paging_request.dict()
        request.ResultSet = result_set.dict()
        request.ExternalArchiveInvoiceCode = ExternalArchiveInvoiceCode
        return self.client.service.SearchArchiveInvoice(request=request)

    
    def get_cities(self):
        return self.address_client.service.GetCityList()
    
    def send_archive_invoice(self, request: SendArchiveInvoiceRequest):
        response = self.client.service.SendArchiveInvoice(request=request.dict())
        return response


    def get_last_invoice_number(self, company_tax_code: str):
        return self.search_archive_invoice(company_tax_code=company_tax_code, paging_request=PagingRequest(PageNumber=1, RecordsPerPage=1), result_set=SearchArchiveInvoiceResultSet()).ArchiveInvoices.ArchiveInvoice[0].ExternalArchiveInvoiceCode

    def send_archive_invoice_xml_without_invoice_number(self, request: SendArchiveInvoiceRequest):
        xml = ElementTree.tostring(request.to_xml(invoice_to_base64=True), encoding="utf-8")
        return self.client.service.SendArchiveInvoiceXmlWithoutInvoiceNumber(request=xml)


            