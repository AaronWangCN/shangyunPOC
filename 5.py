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
功能：创建云企业网实例和转发路由器
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
        config.endpoint = f'cbn.aliyuncs.com'
        return OpenApiClient(config)

    @staticmethod
    def create_api_info_CreateCen() -> open_api_models.Params:
        params = open_api_models.Params(
            action='CreateCen',
            version='2017-09-12',
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
    def create_api_info_DescribeCens() -> open_api_models.Params:
        params = open_api_models.Params(
            action='DescribeCens',
            version='2017-09-12',
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
    def create_api_info_CreateTransitRouterVpcAttachment() -> open_api_models.Params:
        params = open_api_models.Params(
            action='CreateTransitRouterVpcAttachment',
            version='2017-09-12',
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
    def create_api_info_ListTransitRouterVpcAttachments() -> open_api_models.Params:
        params = open_api_models.Params(
            action='ListTransitRouterVpcAttachments',
            version='2017-09-12',
            protocol='HTTPS',
            method='POST',
            auth_type='AK',
            style='RPC',
            pathname=f'/',
            req_body_type='json',
            body_type='json'
        )
        return params

    @staticmethod
    def main(
            args: List[str],
    ) -> str:
        client = Sample.create_client()

        # 1、调用 CreateCen，创建一个云企业网实例。
        print("开始：1、调用 CreateCen，创建一个云企业网实例。")
        params = Sample.create_api_info_CreateCen()

        cen_name = "my_sample_cen"  
        cen_description = "This is a sample CEN created by SDK."  
        protection_level = "REDUCED"
        region_id = "cn-hangzhou"
        queries = {
            'Name': cen_name,
            'Description': cen_description,
            'ProtectionLevel': protection_level,
            'RegionId': region_id
        }
        runtime = util_models.RuntimeOptions(
            connect_timeout=1000000,
            read_timeout=200000
        )
        try:
            request = open_api_models.OpenApiRequest(
                query=OpenApiUtilClient.query(queries)
            )
            response = client.call_api(params, request, runtime)
            cen_id = response['body']['CenId']
            print(f"结束：1、调用 CreateCen，获取返回的 CenId: {cen_id}。")

            # 2、根据 CenId，使用 DescribeCens 查询云企业网的状态。
            print("开始：2、根据 CenId，使用 DescribeCens 查询云企业网的状态。")
            params = Sample.create_api_info_DescribeCens()
            queries = {
                'CenId': cen_id
            }
            runtime = util_models.RuntimeOptions(
                connect_timeout=1000000,
                read_timeout=200000
            )

            try:
                idx = 0
                while True:
                    request = open_api_models.OpenApiRequest(
                        query=OpenApiUtilClient.query(queries)
                    )
                    response = client.call_api(params, request, runtime)
                    status = response['body']['Cens']['Cen'][0]['Status']
                    if status == 'Active':
                        print(f"查询到CEN ID: {cen_id}, 名称: {cen_name}, 当前状态: {status}。")
                        break
                    else:
                        pass
                    idx += 1
                    if idx >= 15:
                        print(f'CEN:{cen_id} 创建超过15分钟，创建失败，退出任务。')
                        return "failed"
                    time.sleep(60)
            except Exception as error:
                if error.statusCode == 404:
                    print(f'<success>：已执行 CreateCen 成功，但是调用 DescribeCens 查询 {cen_id} 失败，请在下一轮继续查询 {cen_id}，无需重新创建。</success>')
                else:
                    traceback.print_exc()
                return "failed"
            # 针对查询类函数，需要打印代码执行成果
            print(f'<success>：调用 CreateCen，成功创建云企业网，CenId:{cen_id}。</success>')
            print("结束：2、根据 CenId，使用 DescribeCens 查询云企业网的状态。")
        except Exception as error:
            if error.statusCode == 404:
                print(f'<success>：CreateCen 创建云企业网实例失败，请在下一轮继续创建。</success>')
            else:
                traceback.print_exc()
            return "failed"

        # 3、调用 CreateTransitRouterVpcAttachment 自动创建企业版转发路由器实例，并将VPC连接至转发路由器。
        print("开始：3、调用 CreateTransitRouterVpcAttachment 自动创建企业版转发路由器实例，并将VPC连接至转发路由器。")
        params = Sample.create_api_info_CreateTransitRouterVpcAttachment()
        vpc_id = 'vpc-uf6sssssssssvmy9'
        region_id = 'cn-shanghai'
        v_switch_id = 'vsw-uf6sssssssssssrfcm'
        zone_id = 'cn-shanghai-f'
        auto_publish_route_enabled = 'true'
        charge_type = 'POSTPAY'
        dry_run = 'false'
        client_token = str(uuid.uuid4())
        queries = {
            'CenId': cen_id,
            'VpcId': vpc_id,
            'ZoneMappings': [
                {
                    'VSwitchId': v_switch_id,
                    'ZoneId': zone_id
                }
            ],
            'RegionId': region_id,
            'AutoPublishRouteEnabled': auto_publish_route_enabled,
            'ChargeType': charge_type,
            'DryRun': dry_run,
            'ClientToken': client_token
        }
        runtime = util_models.RuntimeOptions(
            connect_timeout=1000000,
            read_timeout=200000
        )
        try:
            request = open_api_models.OpenApiRequest(
                query=OpenApiUtilClient.query(queries)
            )
            response = client.call_api(params, request, runtime)
            transit_router_attachment_id = response['body']['TransitRouterAttachmentId']
            print(f"结束：3、调用 CreateTransitRouterVpcAttachment 自动创建企业版转发路由器实例，并将VPC连接至转发路由器。")

            # 4、调用 ListTransitRouterVpcAttachments 查询连接状态。
            print("开始：4、调用 ListTransitRouterVpcAttachments 查询连接状态。")
            params = Sample.create_api_info_ListTransitRouterVpcAttachments()
            queries = {
                'TransitRouterAttachmentId': transit_router_attachment_id
            }
            try:
                idx = 0
                while True:
                    request = open_api_models.OpenApiRequest(
                        query=OpenApiUtilClient.query(queries)
                    )
                    response = client.call_api(params, request, runtime)
                    TransitRouterAttachments = response['body']['TransitRouterAttachments']
                    if len(TransitRouterAttachments) > 0 and TransitRouterAttachments[0]['Status'] == 'Attached':
                        break
                    else:
                        pass
                    idx += 1
                    if idx >= 15:
                        print(f'<success>：将VPC连接至转发路由器超过15分钟，连接失败，退出任务。请检查输入参数是否有效。</success>')
                        return "failed"
                    time.sleep(60)
            except Exception as error:
                if error.statusCode == 404:
                    print(f'<success>：ListTransitRouterVpcAttachments 查询跨地域连接ID：{transit_router_attachment_id} 失败，请下一轮继续查询。</success>')
                else:
                    traceback.print_exc()
                return "failed"
            transit_router_id = TransitRouterAttachments[0]['TransitRouterId']
            print(f'<success>：在地域:{region_id}自动创建了企业版转发路由器实例:{transit_router_id}，并将该实例绑定至同一地域下的VPC:{vpc_id} 。</success>')
            print("结束：4、调用 ListTransitRouterVpcAttachments 查询连接状态。")
            return "Success"
        except Exception as error:
            if error.statusCode == 404:
                print(f'<success>：调用 CreateTransitRouterVpcAttachment 自动创建企业版转发路由器实例，并将VPC连接至转发路由器失败，请在下一轮调用。</success>')
            else:
                traceback.print_exc()
            return "failed"


if __name__ == '__main__':
    result = Sample.main(sys.argv[1:])
    print(result)