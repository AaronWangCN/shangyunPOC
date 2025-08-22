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
功能：创建两台ecs实例
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
        config.endpoint = f'ecs.cn-hangzhou.aliyuncs.com'
        return OpenApiClient(config)

    @staticmethod
    def create_api_info_DescribeAvailableResource() -> open_api_models.Params:
        params = open_api_models.Params(
            action='DescribeAvailableResource',
            version='2014-05-26',
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
    def create_api_info_DescribeImages() -> open_api_models.Params:
        params = open_api_models.Params(
            action='DescribeImages',
            version='2014-05-26',
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
    def create_api_info_RunInstances() -> open_api_models.Params:
        params = open_api_models.Params(
            action='RunInstances',
            version='2014-05-26',
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
    def create_api_info_DescribeInstances() -> open_api_models.Params:
        params = open_api_models.Params(
            action='DescribeInstances',
            version='2014-05-26',
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
    def main(args: List[str]) -> None:
        print("开始：1、调用 DescribeAvailableResource 查询可用的ECS实例规格。")
        try:
            RegionId = "cn-hangzhou"
            ZoneId = "cn-hangzhou-b"
            SystemDiskCategory = "cloud_efficiency"
            Cores = 2
            Memory = 2
            client = Sample.create_client()
            params = Sample.create_api_info_DescribeAvailableResource()
            queries = {
                'RegionId': RegionId,
                'DestinationResource': 'InstanceType',
                'ZoneId': ZoneId,
                'SystemDiskCategory': SystemDiskCategory,
                'Cores': Cores,
                'Memory': Memory
            }
            runtime = util_models.RuntimeOptions(
                connect_timeout=1000000,
                read_timeout=200000
            )
            request = open_api_models.OpenApiRequest(
                query=OpenApiUtilClient.query(queries)
            )
            response = client.call_api(params, request, runtime)
            AvailableZone = response['body'].get('AvailableZones', {}).get('AvailableZone', [])
            if not AvailableZone:
                print(f"<success>：查询失败，没有可用的实例规格。请检查输入参数是否有效。</success>")
                return "Failed"
            AvailableResource = AvailableZone[0].get('AvailableResources', {}).get('AvailableResource', [])
            if not AvailableResource:
                print(f"<success>：查询失败，没有可用的实例规格。请检查输入参数是否有效。</success>")
                return "Failed"
            SupportedResource = AvailableResource[0].get('SupportedResources', {}).get('SupportedResource', [])
            available_resource = [item for item in SupportedResource if item.get('Status') == 'Available']
            if not available_resource:
                print(f"<success>：查询失败，没有可用的实例规格。请检查输入参数是否有效。</success>")
                return "Failed"
            import random
            random_instance_type = random.choice(available_resource)
            instance_type_value = random_instance_type['Value']
            if not SupportedResource:
                print(f"<success>：查询失败，没有可用的实例规格。请检查输入参数是否有效。</success>")
                return "Failed"
            print(
                f"<success>：查询可用的ECS实例规格成功。在可用区：{ZoneId} 随机选择一个可用的实例规格：{instance_type_value}，其对应的系统盘类型为:{SystemDiskCategory}。</success>")
            print("结束：1、调用 DescribeAvailableResource 查询可用的ECS实例规格。")
        except Exception as error:
            if error.statusCode == 404:
                print(f'<success>：DescribeAvailableResource 查询 {queries} 失败，请下一轮继续查询。</success>')
            else:
                traceback.print_exc()
            return "failed"

        print("开始：2、调用 DescribeImages 查询指定ECS实例规格的镜像列表。")
        try:
            InstanceType = instance_type_value
            params = Sample.create_api_info_DescribeImages()
            queries = {
                'RegionId': RegionId,
                'InstanceType': InstanceType
            }
            runtime = util_models.RuntimeOptions(
                connect_timeout=1000000,
                read_timeout=200000
            )
            request = open_api_models.OpenApiRequest(
                query=OpenApiUtilClient.query(queries)
            )
            response = client.call_api(params, request, runtime)
            images = response['body'].get('Images', {}).get('Image', [])
            Available_images = [image for image in images if image.get('Status') == 'Available']
            if not Available_images:
                print(
                    f"<success>：查询失败，在区域：{RegionId}没有实例规格：{InstanceType}可用的镜像。请检查输入参数是否有效。</success>")
                return "Failed"
            import random
            random_image = random.choice(Available_images)
            image_id = random_image.get('ImageId')
            print(
                f"<success>：查询ECS镜像成功。在区域：{RegionId} 选择实例规格：{InstanceType} 可用的一个镜像：{image_id} 。</success>")
            print("结束：2、调用 DescribeImages 查询指定ECS实例规格的镜像列表。")
        except Exception as error:
            if error.statusCode == 404:
                print(f'<success>：DescribeImages 查询 {queries} 失败，请下一轮继续查询。</success>')
            else:
                traceback.print_exc()
            return "failed"

        print("开始：3、调用 RunInstances，根据查询到的镜像和实例规格创建ECS实例。")
        try:
            params = Sample.create_api_info_RunInstances()
            ImageId = image_id
            InstanceType = instance_type_value
            SecurityGroupId = "sg-bxxxxxxxs"
            VSwitchId = "vsw-bp17xxxx0n"
            InternetMaxBandwidthIn = "5"
            InternetMaxBandwidthOut = "10"
            Password = "Paxxxxxxxxxxxxxx23!"
            Amount = 2
            HostName = "web-server"
            SystemDiskSize = 40
            queries = {
                'RegionId': RegionId,
                'ImageId': ImageId,
                'InstanceType': InstanceType,
                'SecurityGroupId': SecurityGroupId,
                'VSwitchId': VSwitchId,
                'SystemDisk.Category': SystemDiskCategory,
                'InternetMaxBandwidthIn': InternetMaxBandwidthIn,
                'InternetMaxBandwidthOut': InternetMaxBandwidthOut,
                'Password': Password,
                'Amount': Amount,
                'HostName': HostName,
                'SystemDisk.Size': SystemDiskSize
            }
            runtime = util_models.RuntimeOptions(
                connect_timeout=1000000,
                read_timeout=200000
            )
            request = open_api_models.OpenApiRequest(
                query=OpenApiUtilClient.query(queries)
            )
            response = client.call_api(params, request, runtime)
            instance_ids: list = response['body']['InstanceIdSets']['InstanceIdSet']
            print(f'创建的实例ID: {instance_ids}')
            print("结束：3、调用 RunInstances，根据查询到的镜像和实例规格创建ECS实例。")
            print("开始：4、调用 DescribeInstances 查询实例的状态。")
            params = Sample.create_api_info_DescribeInstances()
            queries = {
                'RegionId': RegionId,
                'InstanceIds': str(instance_ids),
                'Status': 'Running'
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
                    instances: list = response['body']['Instances']['Instance']
                    if len(instances) != len(instance_ids):
                        pass
                    elif all(item['Status'] == 'Running' for item in instances):
                        print(f'实例 {instance_ids} 已创建成功并正常运行')
                        for instance in instances:
                            public_ip = instance['PublicIpAddress']['IpAddress']
                            private_ips = instance.get('VpcAttributes', {}).get('PrivateIpAddress', {}).get('IpAddress', [])
                            if public_ip:
                                print(f"<success>：实例ID: {instance['InstanceId']}创建成功，并且已分配公网IP: {public_ip}，私网IP: {private_ips}。</success>")
                            else:
                                print(f"<success>：实例ID: {instance['InstanceId']}创建成功，但未分配公网IP，私网IP: {private_ips}。</success>")
                        break
                    idx += 1
                    if idx >= 15:
                        print(f'<success>：实例 {instance_ids} 创建超过15分钟，创建失败，退出任务。请检查输入参数是否有效。</success>')
                        return "failed"
                    time.sleep(60)
            except Exception as error:
                if error.statusCode == 404:
                    print(f'<success>：DescribeInstances 查询 {queries} 失败，请下一轮继续查询。</success>')
                else:
                    traceback.print_exc()
                return "failed"

            print("结束：4、调用 DescribeInstances 查询实例的状态。")
            return "Success"
        except Exception as error:
            if error.statusCode == 404:
                print(f'<success>：RunInstances 创建 {queries} 失败，请下一轮继续创建。</success>')
            else:
                traceback.print_exc()
            return "failed"


if __name__ == '__main__':
    result = Sample.main(sys.argv[1:])
    print(result)
