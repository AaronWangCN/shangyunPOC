# -*- coding: utf-8 -*-
import os
import sys
import time
import traceback
from typing import List
from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_credentials.client import Client as CredentialClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient

'''
功能：创建一个带有公网IP的SLB实例和安全组
'''


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> OpenApiClient:
        credential = CredentialClient()
        config = open_api_models.Config(
            credential=credential
        )
        config.endpoint = 'slb.aliyuncs.com'
        return OpenApiClient(config)

    @staticmethod
    def create_api_info_CreateLoadBalancer() -> open_api_models.Params:
        params = open_api_models.Params(
            action='CreateLoadBalancer',
            version='2014-05-15',
            protocol='HTTPS',
            method='POST',
            auth_type='AK',
            style='RPC',
            pathname='/',
            req_body_type='json',
            body_type='json'
        )
        return params

    @staticmethod
    def create_api_info_DescribeLoadBalancers() -> open_api_models.Params:
        params = open_api_models.Params(
            action='DescribeLoadBalancers',
            version='2014-05-15',
            protocol='HTTPS',
            method='POST',
            auth_type='AK',
            style='RPC',
            pathname='/',
            req_body_type='json',
            body_type='json'
        )
        return params

    @staticmethod
    def main(
            args: List[str],
    ) -> None:
        client = Sample.create_client()

        # 1、调用 CreateLoadBalancer，获取返回的SLB LoadBalancerId。
        print("开始：1、调用 CreateLoadBalancer，获取返回的SLB LoadBalancerId。")
        params = Sample.create_api_info_CreateLoadBalancer()
        RegionId = 'cn-hangzhou'
        AddressType = 'internet'
        VpcId = 'vpc-bp1xxxxxxxxxui'
        VSwitchId = 'vsw-bpxxxxxxxxxnlz'
        InternetChargeType = 'paybytraffic'
        MasterZoneId = 'cn-hangzhou-b'
        PayType = 'PayOnDemand'
        AddressIPVersion = 'ipv4'
        DeleteProtection = 'off'
        ModificationProtectionStatus = 'ConsoleProtection'
        queries = {
            'RegionId': RegionId,
            'AddressType': AddressType,
            'VpcId': VpcId,
            'VSwitchId': VSwitchId,
            'InternetChargeType': InternetChargeType,
            'MasterZoneId': MasterZoneId,
            'PayType': PayType,
            'AddressIPVersion': AddressIPVersion,
            'DeleteProtection': DeleteProtection,
            'ModificationProtectionStatus': ModificationProtectionStatus
        }
        runtime = util_models.RuntimeOptions(
            connect_timeout=1000000,  # 连接超时时间，单位毫秒
            read_timeout=200000  # 读取超时时间，单位毫秒
        )
        try:
            request = open_api_models.OpenApiRequest(
                query=OpenApiUtilClient.query(queries)
            )
            response = client.call_api(params, request, runtime)
            loadbalancer_id = response['body']['LoadBalancerId']
            print(f'<success>：SLB实例ID:{loadbalancer_id} 创建成功。</success>')
            print("结束：1、调用 CreateLoadBalancer，获取返回的SLB LoadBalancerId。")

            # 2、根据 LoadBalancerId，使用 DescribeLoadBalancers 查询SLB实例的状态
            print("开始：2、根据 LoadBalancerId，使用 DescribeLoadBalancers 查询SLB实例的状态")
            params = Sample.create_api_info_DescribeLoadBalancers()
            queries = {
                'RegionId': RegionId,
                'LoadBalancerId': loadbalancer_id
            }
            runtime = util_models.RuntimeOptions(
                connect_timeout=1000000,  # 连接超时时间，单位毫秒
                read_timeout=200000  # 读取超时时间，单位毫秒
            )

            try:
                idx = 0
                while True:
                    request = open_api_models.OpenApiRequest(
                        query=OpenApiUtilClient.query(queries)
                    )
                    response = client.call_api(params, request, runtime)
                    found = False
                    for LoadBalancer in response['body']['LoadBalancers']['LoadBalancer']:
                        loadbalancer_status = LoadBalancer['LoadBalancerStatus']
                        loadbalancer_Address = LoadBalancer['Address']
                        loadbalancer_PayType = LoadBalancer['PayType']
                        loadbalancer_AddressType = LoadBalancer['AddressType']
                        loadbalancer_AddressIPVersion = LoadBalancer['AddressIPVersion']
                        loadbalancer_Bandwidth = LoadBalancer['Bandwidth']
                        loadbalancer_InternetChargeTypeAlias = LoadBalancer['InternetChargeTypeAlias']
                        loadbalancer_LoadBalancerSpec = LoadBalancer['LoadBalancerSpec']
                        if loadbalancer_id == LoadBalancer['LoadBalancerId'] and loadbalancer_status == 'active':
                            # 打印代码执行成果
                            print(f'<success>：调用 CreateLoadBalancer，获取返回的SLB LoadBalancerId:{loadbalancer_id} ，查询SLB实例的详情：实例状态：{loadbalancer_status}，实例的网络类型：{loadbalancer_AddressType}，实例IP地址：{loadbalancer_Address}，实例付费模式：{loadbalancer_PayType}，实例IP 版本：{loadbalancer_AddressIPVersion}，实例监听的带宽峰值：{loadbalancer_Bandwidth}，实例公网计费方式：{loadbalancer_InternetChargeTypeAlias}，实例规格：{loadbalancer_LoadBalancerSpec} 。</success>')
                            found = True

                    if found == True:
                       break
                    else:
                        time.sleep(60)
                    idx += 1
                    if idx >= 15:
                        print(f'<success>：调用 CreateLoadBalancer，loadbalancer:{loadbalancer_id} 创建超过15分钟，创建失败，退出任务。</success>')
                        return "failed"
            except Exception as error:
                if error.statusCode == 404:
                    print(f'<success>：DescribeLoadBalancers 查询 {queries} 查询失败，请下一轮继续查询。</success>')
                else:
                    traceback.print_exc()
                return "failed"
            # 针对查询类函数，需要打印代码执行成果
            print("结束：2、根据 LoadBalancerId，使用 DescribeLoadBalancers 查询SLB实例的状态")

            return "Success"
        except Exception as error:
            # 错误 message
            if error.statusCode == 404:
                print(f'<success>：CreateLoadBalancer 创建 {queries} 失败，请下一轮继续创建。</success>')
            else:
                traceback.print_exc()
            return "failed"


if __name__ == '__main__':
    result = Sample.main(sys.argv[1:])
    print(result)