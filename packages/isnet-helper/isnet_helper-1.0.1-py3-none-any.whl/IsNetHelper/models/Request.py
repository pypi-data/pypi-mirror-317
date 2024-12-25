import base64
from typing import List, Optional
from xml.etree import ElementTree as ET
import pydantic
from pydantic import BaseModel

class CustomBaseModel(pydantic.BaseModel):
    
    def to_xml(self) -> str:
        raise NotImplementedError


class RequestHeader(CustomBaseModel):
    value: str


class PagingRequest(CustomBaseModel):
    PageNumber: int = 1
    RecordsPerPage: int = 25
    
    def to_xml(self) -> str:
        
        root = ET.Element("ein:PagingRequest")
        for field, value in self.dict().items():
            ET.SubElement(root, f"ein:{field}").text = str(value)
        return root
        
    
    


class SearchArchiveInvoiceResultSet(CustomBaseModel):
    IsAdditionalTaxIncluded: bool = False
    IsArchiveIncluded: bool = False
    IsAttachmentIncluded: bool = False
    IsExternalUrlIncluded: bool = False
    IsHtmlIncluded: bool = False
    IsInvoiceDetailIncluded: bool = False
    IsPDFIncluded: bool = False
    IsXMLIncluded: bool = False
    
    def to_xml(self) -> str:
        root = ET.Element("ein:SearchArchiveInvoiceResultSet")
        for field, value in self.dict().items():
            ET.SubElement(root, f"ein:{field}").text = str(value)
        return root

class SearchArchiveInvoiceRequestData(CustomBaseModel):
    CompanyTaxCode: str
    IsCancelled: bool = False
    PagingRequest: PagingRequest
    ResultSet: SearchArchiveInvoiceResultSet
    
    
    def to_xml(self) -> ET.Element:
        root = ET.Element("tem:request")
        ET.SubElement(root, "ein:CompanyTaxCode").text = self.CompanyTaxCode
        ET.SubElement(root, "ein:IsCancelled").text = str(self.IsCancelled).lower()
        root.append(self.PagingRequest.to_xml())
        root.append(self.ResultSet.to_xml())
        return root
    

class SearchArchiveInvoiceRequest(CustomBaseModel):
    headers: List[RequestHeader] = []
    request: SearchArchiveInvoiceRequestData
    
    def to_xml(self) -> str:
        root = ET.Element("soapenv:Envelope", attrib={"xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/", "xmlns:tem": "http://tempuri.org/", "xmlns:ein": "http://schemas.datacontract.org/2004/07/EInvoice.Service.Model", "xmlns:ein1": "http://schemas.datacontract.org/2004/07/EInvoice.Service.Model.DataTypes.Enums"})
        
        headers = ET.SubElement(root, "soapenv:Header")
        for header in self.headers:
            headers.append(header.to_xml())
        
        body = ET.SubElement(root, "soapenv:Body")
        
        ET.SubElement(body, "tem:SearchArchiveInvoice").append(self.request.to_xml())
        
        
        return root
    

class Product(BaseModel):
    __xml_name__ = "Product"
    ExternalProductCode: str
    MeasureUnit: str
    ProductCode: str
    ProductName: str
    ReceiverProductCode: str
    UnitPrice: float

class EArchiveInvoiceDetail(BaseModel):
    __xml_name__ = "InvoiceDetail"
    CurrencyCode: str
    DiscountAmount: float
    DiscountRate: float
    LineExtensionAmount: float
    Note: str
    Product: Product
    Quantity: float
    SpecialBasisAmount: float
    SpecialBasisPercent: float
    SpecialBasisTaxAmount: float
    StockDescription: str
    VATAmount: float
    VATRate: float
    TaxExemptionReasonCode: str

class ArchiveInvoiceDetails(BaseModel):
    __xml_name__ = "ArchiveInvoiceDetail"
    ArchiveInvoiceDetail: List['EArchiveInvoiceDetail']

class EArchiveInvoices(BaseModel):
    __xml_name__ = "ArchiveInvoices"
    ArchiveInvoice: List['EArchiveInvoice']

class ReceiverAddress(BaseModel):
    __xml_name__ = "Address"
    CityCode: str
    EMail: str

class Receiver(BaseModel):
    __xml_name__ = "Receiver"
    Address: ReceiverAddress
    ReceiverName: str
    ReceiverTaxCode: str
    RecipientType: str
    SendingType: str

class EArchiveInvoice(BaseModel):
    __xml_name__ = "ArchiveInvoice"
    CurrencyCode: str
    ExternalArchiveInvoiceCode: Optional[str]
    InvoiceCreationDate: str
    InvoiceDate: str
    InvoiceDetails: ArchiveInvoiceDetails
    InvoiceType: str
    Notes: List[str]
    Receiver: Receiver
    TaxExemptionReason: str
    TotalDiscountAmount: float
    TotalLineExtensionAmount: float
    TotalPayableAmount: float
    TotalTaxInclusiveAmount: float
    TotalVATAmount: float
    CrossRate: float

class SendArchiveInvoiceRequest(BaseModel):
    __xml_name__ = "request"
    ArchiveInvoices: EArchiveInvoices
    CompanyTaxCode: str
    
    def to_xml(self, invoice_to_base64: bool = False):
        envelope = ET.Element("soapenv:Envelope", {
        "xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
        "xmlns:tem": "http://tempuri.org/",
        "xmlns:ein": "http://schemas.datacontract.org/2004/07/EInvoice.Service.Model",
        "xmlns:arr": "http://schemas.microsoft.com/2003/10/Serialization/Arrays",
    })
        body = ET.SubElement(envelope, "soapenv:Body")
        send_archive_invoice = ET.SubElement(body, "tem:SendArchiveInvoice")
        request = ET.SubElement(send_archive_invoice, "tem:request")

        # ArchiveInvoices
        archive_invoices = ET.SubElement(request, "ein:ArchiveInvoices")
        for invoice in self.ArchiveInvoices.ArchiveInvoice:
            
            invoice_element = ET.Element("ein:ArchiveInvoice")
            for key, value in invoice.dict().items():
                if isinstance(value, list):
                    if key == "Notes":
                        notes = ET.SubElement(invoice_element, "ein:Notes")
                        for note in value:
                            ET.SubElement(notes, "ein:string").text = note
                elif isinstance(value, dict):
                    sub_element = ET.SubElement(invoice_element, f"ein:{key}")
                    for sub_key, sub_value in value.items():
                        ET.SubElement(sub_element, f"ein:{sub_key}").text = str(sub_value)
                else:
                    ET.SubElement(invoice_element, f"ein:{key}").text = str(value)
            
            
            archive_invoices.append(invoice_element)
        # CompanyTaxCode
        ET.SubElement(request, "ein:CompanyTaxCode").text = self.CompanyTaxCode

        return envelope

class EArchiveInvoiceWithoutInvoiceNumber(BaseModel):
    __xml_name__ = "ArchiveInvoice"
    ArchiveInvoiceContent: bytes
    SendMailAutomatically: bool
    
class SendArchiveInvoiceRequestWithoutInvoiceNumber(BaseModel):
    __xml_name__ = "request"
    ArchiveInvoices: EArchiveInvoices
    CompanyVendorNumber: str
    SendMailAutomatically: bool
    
    def to_xml(self):
        envelope = ET.Element("soapenv:Envelope", {
        "xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
        "xmlns:tem": "http://tempuri.org/",
        "xmlns:ein": "http://schemas.datacontract.org/2004/07/EInvoice.Service.Model",
        "xmlns:arr": "http://schemas.microsoft.com/2003/10/Serialization/Arrays",
    })
        body = ET.SubElement(envelope, "soapenv:Body")
        send_archive_invoice = ET.SubElement(body, "tem:SendArchiveInvoice")
        request = ET.SubElement(send_archive_invoice, "tem:request")

        # ArchiveInvoices
        archive_invoices = ET.Element("ein:ArchiveInvoices")
        for invoice in self.ArchiveInvoices.ArchiveInvoice:
            invoice_element = ET.Element("ein:ArchiveInvoice")
            for key, value in invoice.dict().items():
                if isinstance(value, list):
                    if key == "Notes":
                        notes = ET.SubElement(invoice_element, "ein:Notes")
                        for note in value:
                            ET.SubElement(notes, "ein:string").text = note
                elif isinstance(value, dict):
                    sub_element = ET.SubElement(invoice_element, f"ein:{key}")
                    for sub_key, sub_value in value.items():
                        ET.SubElement(sub_element, f"ein:{sub_key}").text = str(sub_value)
                else:
                    ET.SubElement(invoice_element, f"ein:{key}").text = str(value)
            
            earchive_invoice = ET.SubElement(archive_invoices, "ein:ArchiveInvoice")
            ET.SubElement(earchive_invoice, "ein:ArchiveInvoiceContent").text = base64.b64encode(ET.tostring(invoice_element))
            ET.SubElement(earchive_invoice, "ein:SendMailAutomatically").text = str(self.SendMailAutomatically).lower()
            
        # CompanyTaxCode
        ET.SubElement(body, "ein:CompanyVendorNumber").text = self.CompanyVendorNumber
        return ET.tostring(envelope, encoding="utf-8", method="xml")



EArchiveInvoices.update_forward_refs()