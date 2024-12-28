"""
ezsec_requests

a library of adapters to automatically format http requests to send to
the ezsec API service.
"""
__version__ = "0.1.1"

import requests

base_dir = "api.ezsec-api.com"

def request_filing_cik(year,qtr,cik,type,auth):
    return requests.get(f'https://{base_dir}/filing/api/retrieve/type?year={year}&qtr={qtr}&cik={cik}&filing_type={type}',headers={"accept": "application/json", "Authorization": auth}, verify=False)

def request_filing_ticker(year,qtr,ticker,type,auth):
    return requests.get(f'https://{base_dir}/filing/api/ticker/retrieve/type?year={year}&qtr={qtr}&ticker={ticker}&filing_type={type}',headers={"accept": "application/json", "Authorization": auth}, verify=False)
    
def request_filing_company(year,qtr,name,type,auth):
    return requests.get(f'https://{base_dir}/filing/api/company_name/retrieve/type?year={year}&qtr={qtr}&name={name}&filing_type={type}',headers={"accept": "application/json", "Authorization": auth}, verify=False)

def request_processed(year,qtr,cik,type,auth):
    return requests.get(f'https://{base_dir}/filing/api/retrieve/processed/type?year={year}&qtr={qtr}&cik={cik}&filing_type={type}',headers={"accept": "application/json", "Authorization": auth}, verify=False)
    