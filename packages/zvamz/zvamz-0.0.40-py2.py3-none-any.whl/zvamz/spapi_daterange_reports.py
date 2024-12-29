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

def refunds_daterange(marketplace_action, access_token, start_date, end_date):
    """
    This will pull Refund Reports per region in a specific date range.

    Parameter:
    - marketplace_action: the specific marketplace command to pull the data
    - access_token: matching access token of the marketplace
    - start_date: start date in ISO format, this is inclusive
    - end_date: end date in ISO format, this is exclusive

    return:
    - data frame of Refund Report
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
        records.extend(response.json()['payload']['FinancialEvents']['RefundEventList'])

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
            records.extend(response.json()['payload']['FinancialEvents']['RefundEventList'])

            try:
                NextToken = response.json()['payload']['NextToken']
            except:
                NextToken = None
            
        print('End of List')

    except Exception as e:
        print(response.json()['errors'][0]['message'])
        print(response.json()['errors'][0]['details'])

    # Data Frame
    refunds = []
    for record in records:
        data = {
            'amazon_order_id': record.get('AmazonOrderId', np.nan),
            'seller_order_id': record.get('SellerOrderId', np.nan),
            'marketplace_link': record.get('MarketplaceName', np.nan),
            'refund_date': record.get('PostedDate', np.nan),
            'sku': record.get('ShipmentItemAdjustmentList', [{}])[0].get('SellerSKU', np.nan),
            'order_adjustment_item_id': record.get('ShipmentItemAdjustmentList', [{}])[0].get('OrderAdjustmentItemId', np.nan),
            'quantity': record.get('ShipmentItemAdjustmentList', [{}])[0].get('QuantityShipped', np.nan),
            'currency': record.get('ShipmentItemAdjustmentList', [{}])[0].get('ItemChargeAdjustmentList', [{}])[0].get('ChargeAmount',{}).get('CurrencyCode',np.nan),
        }

        chargeAdjustment = record.get('ShipmentItemAdjustmentList', [{}])[0].get('ItemChargeAdjustmentList', [])
        for charge in chargeAdjustment:
            data['charge_' + charge.get('ChargeType')] = charge.get('ChargeAmount', {}).get('CurrencyAmount', np.nan)

        feeAdjustment = record.get('ShipmentItemAdjustmentList', [{}])[0].get('ItemFeeAdjustmentList', [])
        for fee in feeAdjustment:
            data['fee_' + fee.get('FeeType')] = fee.get('FeeAmount', {}).get('CurrencyAmount', np.nan)

        taxWithheld = record.get('ShipmentItemAdjustmentList', [{}])[0].get('ItemTaxWithheldList', [{}])[0].get('TaxesWithheld',[])
        for tax in taxWithheld:
            data['tax_' + tax.get('ChargeType')] = tax.get('ChargeAmount', {}).get('CurrencyAmount', np.nan)

        refunds.append(data)

    refundsDf = pd.DataFrame(refunds)
    refundsDf = refundsDf.rename(columns=lambda x:x.replace('-','_').lower())

    req_columns = [
        'amazon_order_id',
        'seller_order_id',
        'marketplace_link',
        'refund_date',
        'sku',
        'order_adjustment_item_id',
        'quantity',
        'currency',
        'charge_tax',
        'charge_principal',
        'fee_commission',
        'fee_fixedclosingfee',
        'fee_giftwrapchargeback',
        'fee_refundcommission',
        'fee_shippingchargeback',
        'fee_variableclosingfee',
        'fee_digitalservicesfee',
        'tax_marketplacefacilitatortax_principal',
        'charge_restockingfee',
        'charge_shippingtax',
        'charge_shippingcharge',
        'fee_salestaxcollectionfee',
        'charge_returnshipping',
        'tax_marketplacefacilitatortax_shipping',
        'charge_exportcharge',
        'charge_giftwrap',
        'charge_giftwraptax',
        'tax_marketplacefacilitatorvat_principal',
        'fee_renewedprogramfee',
        'tax_marketplacefacilitatorvat_shipping'
    ]

    for col in req_columns:
        if col not in refundsDf.columns:
            refundsDf[col] = np.nan

    refundsDf = refundsDf[req_columns]

    schema = {
        'amazon_order_id': str,
        'seller_order_id': str,
        'marketplace_link': str,
        'refund_date': 'datetime64[ns, UTC]',
        'sku': str,
        'order_adjustment_item_id': str,
        'quantity': float,
        'currency': str,
        'charge_tax': float,
        'charge_principal': float,
        'fee_commission': float,
        'fee_fixedclosingfee': float,
        'fee_giftwrapchargeback': float,
        'fee_refundcommission': float,
        'fee_shippingchargeback': float,
        'fee_variableclosingfee': float,
        'fee_digitalservicesfee': float,
        'tax_marketplacefacilitatortax_principal': float,
        'charge_restockingfee': float,
        'charge_shippingtax': float,
        'charge_shippingcharge': float,
        'fee_salestaxcollectionfee': float,
        'charge_returnshipping': float,
        'tax_marketplacefacilitatortax_shipping': float,
        'charge_exportcharge': float,
        'charge_giftwrap': float,
        'charge_giftwraptax': float,
        'tax_marketplacefacilitatorvat_principal': float,
        'fee_renewedprogramfee': float,
        'tax_marketplacefacilitatorvat_shipping': float
    }

    refundsDf = refundsDf.astype(schema)

    return refundsDf

