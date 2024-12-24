#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/py3_chanjet
=================================================
"""
from types import NoneType
from typing import Union

import py3_requests
import xmltodict
from addict import Dict
from bs4 import BeautifulSoup
from requests import Response

request_urls = Dict()
request_urls.get_data_set = "/estate/webService/ForcelandEstateService.asmx?op=GetDataSet"


class RequestUrl(py3_requests.RequestUrl):
    GETDATASET = "/estate/webService/ForcelandEstateService.asmx?op=GetDataSet"


class ResponseHandler(py3_requests.ResponseHandler):
    @staticmethod
    def success(response: Response = None):
        xml_doc = ResponseHandler.status_code_200_beautifulsoup(
            response=response,
            beautifulsoup_kwargs={"features": "xml"}
        )
        if isinstance(xml_doc, NoneType):
            return []
        results = Dict(
            xmltodict.parse(
                xml_doc.find("NewDataSet").encode(
                    "utf-8"))
        ).NewDataSet.Table
        if isinstance(results, list):
            return results
        if isinstance(results, dict) and len(results.keys()):
            return [results]


class Zkhb(object):
    def __init__(self, base_url: str = ""):
        self.base_url = base_url[:-1] if base_url.endswith("/") else base_url

    def get_data_set(
            self,
            sql: str = None,
            **kwargs
    ):
        """
        get dataset
        :param sql:
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("method", py3_requests.RequestMethod.POST)
        kwargs.setdefault("response_handler", ResponseHandler.success)
        kwargs.setdefault("url", request_urls.get_data_set)
        if not kwargs.get("url", "").startswith("http"):
            kwargs["url"] = self.base_url + kwargs["url"]
        kwargs.setdefault("headers", Dict())
        kwargs.headers.setdefault("Content-Type", "text/xml; charset=utf-8")
        kwargs.setdefault("data", Dict())
        data = xmltodict.unparse(
            {
                "soap:Envelope": {
                    "@xmlns:soap": "http://schemas.xmlsoap.org/soap/envelope/",
                    "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                    "@xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
                    "soap:Body": {
                        "GetDataSet": {
                            "@xmlns": "http://zkhb.com.cn/",
                            "sql": f"{sql}",
                        }
                    }
                }
            }
        )
        kwargs.data = data
        return py3_requests.request(**kwargs.to_dict())

    def query_actual_charge_bill_item_list(
            self,
            top_column_string: str = "",
            condition_string: str = "",
            order_by_string: str = "order by cfi.ChargeFeeItemID desc",
            **kwargs
    ):
        """
        按条件查询实际收费列表
        :param top_column_string:
        :param condition_string:
        :param order_by_string:
        :param kwargs:
        :return:
        """
        sql = f"select {top_column_string} {','.join([
            'cml.ChargeMListID',
            'cml.ChargeMListNo',
            'cml.ChargeTime',
            'cml.PayerName',
            'cml.ChargePersonName',
            'cml.ActualPayMoney',
            'cml.EstateID',
            'cml.ItemNames',
            'ed.Caption as EstateName',
            'cfi.ChargeFeeItemID',
            'cfi.ActualAmount',
            'cfi.SDate',
            'cfi.EDate',
            'cfi.RmId',
            'rd.RmNo',
            'cml.CreateTime',
            'cml.LastUpdateTime',
            'cbi.ItemName',
            'cbi.IsPayFull',
        ])} {''.join([
            ' from chargeMasterList as cml',
            ' left join EstateDetail as ed on cml.EstateID=ed.EstateID',
            ' left join ChargeFeeItem as cfi on cml.ChargeMListID=cfi.ChargeMListID',
            ' left join RoomDetail as rd on cfi.RmId=rd.RmId',
            ' left join ChargeBillItem as cbi on cfi.CBillItemID=cbi.CBillItemID',
        ])} where 1=1 {condition_string} {order_by_string};";

        kwargs = Dict(kwargs)
        kwargs.setdefault("sql", sql)
        return self.get_data_set(**kwargs)

    def query_actual_charge_bill_item_list_condition_string_formatter(
            self,
            estate_id: Union[str, int] = "",
            charge_type: str = "",
            room_no: str = "",
            end_date_begin: str = "",
            end_date_end: str = "",
    ):
        condition_string_list = []
        if int(estate_id) > 0:
            condition_string_list.append(f" and cml.EstateID='{estate_id}'")
        if isinstance(charge_type, str) and len(charge_type):
            condition_string_list.append(f" and cbi.ItemName='{charge_type}'")
        if isinstance(room_no, str) and len(room_no):
            condition_string_list.append(f" and rd.RmNo='{room_no}'")
        if isinstance(end_date_begin, str) and len(end_date_begin):
            condition_string_list.append(f" and cfi.EDate>='{end_date_begin}'")
        if isinstance(end_date_end, str) and len(end_date_end):
            condition_string_list.append(f" and cfi.EDate<='{end_date_end}'")
        return "".join(condition_string_list)
