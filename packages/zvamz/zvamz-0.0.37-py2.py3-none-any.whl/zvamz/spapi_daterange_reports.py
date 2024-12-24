import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
import time
from .ratelimit import RateLimiter
from .fcmap import fc_to_country
from .marketplaces import marketplaces
import gzip
import shutil
import os
import urllib.parse

def shipmentEvents_daterange(marketplace_action, access_token, start_date, end_date):
    """
    This will pull Shipment Event Reports per region in a specific date range.

    Parameter:
    - marketplace_action: the specific marketplace command to pull the data
    - access_token: matching access token of the marketplace
    - start_date: start date in ISO format, this is inclusive
    - end_date: end date in ISO format, this is exclusive

    return:
    - data frame of Shipment Event Report
    """
    # Pull API Data
    rate_limiter = RateLimiter(tokens_per_second=0.5, capacity=30)
    records = []
    regionUrl, marketplace_id = marketplace_action()
    NextToken = None

    headers = {
            'x-amz-access-token': access_token
        }

    request_params  = {
        'PostedAfter': start_date,
        'PostedBefore': end_date
    }

    try:
        url = regionUrl + f'/finances/v0/financialEvents' + '?' + urllib.parse.urlencode(request_params)
        response = requests.get(url, headers=headers)
        records.extend(response.json()['payload']['FinancialEvents']['ShipmentEventList'])

        try:
            NextToken = response.json()['payload']['NextToken']
        except:
            NextToken = None

        while NextToken:
            request_params_next  = {
                'NextToken': NextToken
            }
            url = regionUrl + f'/finances/v0/financialEvents' + '?' + urllib.parse.urlencode(request_params_next)
            response = rate_limiter.send_request(requests.get, url, headers=headers)
            records.extend(response.json()['payload']['FinancialEvents']['ShipmentEventList'])

            try:
                NextToken = response.json()['payload']['NextToken']
            except:
                NextToken = None
            
        print('End of List')

    except Exception as e:
        print(response.json()['errors'][0]['message'])
        print(response.json()['errors'][0]['details'])

    # set Data Frame
    taxDf = []
    for record in records:
        data ={
            'amazon_order_id': record.get('AmazonOrderId', np.nan),
            'posted_date': record.get('PostedDate', np.nan),
            'marketplace': record.get('MarketplaceName', np.nan),
            'sku': record.get('ShipmentItemList', [{}])[0].get('SellerSKU', np.nan),
            'qty': record.get('ShipmentItemList', [{}])[0].get('QuantityShipped', np.nan),
            'currency': record.get('ShipmentItemList', [{}])[0].get('ItemChargeList', [{}])[0].get('ChargeAmount',{}).get('CurrencyCode', np.nan),
        }

        charges = record.get('ShipmentItemList', [{}])[0].get('ItemChargeList', [])
        for charge in charges:
            data[charge.get('ChargeType')] = charge.get('ChargeAmount', {}).get('CurrencyAmount', np.nan)

        fees = record.get('ShipmentItemList', [{}])[0].get('ItemFeeList', [])
        for fee in fees:
            data[fee.get('FeeType')] = fee.get('FeeAmount', {}).get('CurrencyAmount', np.nan)

        withhelds = record.get('ShipmentItemList', [{}])[0].get('ItemTaxWithheldList', [{}])[0].get('TaxesWithheld',[])
        for withheld in withhelds:
            data[withheld.get('ChargeType')] = withheld.get('ChargeAmount', {}).get('CurrencyAmount', np.nan)

        taxDf.append(data)

    taxDf = pd.DataFrame(taxDf)

    taxDf['posted_date'] = pd.to_datetime(taxDf['posted_date'])

    req_columns = [
        'amazon_order_id',
        'posted_date',
        'marketplace',
        'sku',
        'qty',
        'currency',
        'Principal',
        'Tax',
        'GiftWrap',
        'GiftWrapTax',
        'ShippingCharge',
        'ShippingTax',
        'FBAPerUnitFulfillmentFee',
        'Commission',
        'FixedClosingFee',
        'GiftwrapChargeback',
        'SalesTaxCollectionFee',
        'ShippingChargeback',
        'VariableClosingFee',
        'DigitalServicesFee',
        'FBAPerOrderFulfillmentFee',
        'FBAWeightBasedFee',
        'MarketplaceFacilitatorTax-Principal',
        'MarketplaceFacilitatorTax-Shipping',
        'MarketplaceFacilitatorVAT-Principal',
        'LowValueGoodsTax-Shipping',
        'LowValueGoodsTax-Principal',
        'MarketplaceFacilitatorVAT-Shipping',
        'MarketplaceFacilitatorTax-Other',
        'RenewedProgramFee'
    ]

    for col in req_columns:
        if col not in taxDf.columns:
            taxDf[col] = np.nan

    taxDf = taxDf[req_columns]

    schema = {
        'amazon_order_id': str,
        'posted_date': 'datetime64[ns, UTC]',
        'marketplace': str,
        'sku': str,
        'qty': float,
        'currency': str,
        'Principal': float,
        'Tax': float,
        'GiftWrap': float,
        'GiftWrapTax': float,
        'ShippingCharge': float,
        'ShippingTax': float,
        'FBAPerUnitFulfillmentFee': float,
        'Commission': float,
        'FixedClosingFee': float,
        'GiftwrapChargeback': float,
        'SalesTaxCollectionFee': float,
        'ShippingChargeback': float,
        'VariableClosingFee': float,
        'DigitalServicesFee': float,
        'FBAPerOrderFulfillmentFee': float,
        'FBAWeightBasedFee': float,
        'MarketplaceFacilitatorTax-Principal': float,
        'MarketplaceFacilitatorTax-Shipping': float,
        'MarketplaceFacilitatorVAT-Principal': float,
        'LowValueGoodsTax-Shipping': float,
        'LowValueGoodsTax-Principal': float,
        'MarketplaceFacilitatorVAT-Shipping': float,
        'MarketplaceFacilitatorTax-Other': float,
        'RenewedProgramFee': float
    }

    taxDf = taxDf.astype(schema)

    return taxDf

