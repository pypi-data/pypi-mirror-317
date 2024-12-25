


import datetime


def edm_action_date(datetime: datetime.datetime) -> str:
    return datetime.strftime("%Y-%m-%dT%H:%M:%S")


def get_new_invoice_number(invoice_number_prefix: str, last_invoice_number: str) -> str:
    
    MAX_INVOICE_NUMBER_COUNT = 7
    invoice_number = str(int(last_invoice_number[7:]) + 1)
    invoice_number_str = "0" * (MAX_INVOICE_NUMBER_COUNT - len(invoice_number)) + invoice_number
        
    
    return f"{invoice_number_prefix}{datetime.datetime.now().strftime('%Y')}{invoice_number_str}"
