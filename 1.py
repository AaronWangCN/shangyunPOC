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
功能：为ECS实例分配公网IP
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
        config.endpoint = 'ecs.cn-hangzhou.aliyuncs.com'
        return OpenApiClient(config)

    @staticmethod
    def create_api_info_ModifyInstanceAttribute() -> open_api_models.Params:
        params = open_api_models.Params(
            action='ModifyInstanceAttribute',
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
    def create_api_info_RebootInstance() -> open_api_models.Params:
        params = open_api_models.Params(
            action='RebootInstance',
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
    def create_api_info_DescribeInstanceStatus() -> open_api_models.Params:
        params = open_api_models.Params(
            action='DescribeInstanceStatus',
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
    def create_api_info_ModifyInstanceNetworkSpec() -> open_api_models.Params:
        params = open_api_models.Params(
            action='ModifyInstanceNetworkSpec',
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
    def create_api_info_AllocatePublicIpAddress() -> open_api_models.Params:
        params = open_api_models.Params(
            action='AllocatePublicIpAddress',
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
    def create_api_info_DescribeInstanceAttribute() -> open_api_models.Params:
        params = open_api_models.Params(
            action='DescribeInstanceAttribute',
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
    def main(
            args: List[str],
    ) -> None:
        client = Sample.create_client()

        # 1、调用 ModifyInstanceAttribute，修改实例属性信息。
        print("开始：1、调用 ModifyInstanceAttribute，修改实例属性信息。")
        params = Sample.create_api_info_ModifyInstanceAttribute()

        InstanceId = 'i-bp1xxxxxxxxxxxxx0v'  # 替换为实际的实例ID
        HostName = 'exxxxxxxsh'  # 替换为实际的主机名，长度为 2-15 个字符，允许使用大小写字母、数字或短划线（-）。不能以短划线（-）开头或结尾，不能连续使用短划线（-），也不能仅使用数字。
        Password = 'Aaxxxxxxxxx!@'  # 替换为实际的密码，支持长度为 8~30 个字符，必须同时包含大小写英文字母、数字和特殊符号中的三类字符。特殊符号可以是：()`~!@#$%^&*-_+=|{}[]:;'<>,.?/ 。
        SecurityGroupIds = 'sg-bpxxxxxxxxxxs1'  # 替换为实际的安全组ID
        Description = ''  # 替换为实际的描述，不得为空字符串
        EnableJumboFrame = 'false'  # 替换为实际的是否启用 Jumbo Frame
        modify_queries = {
            'InstanceId': InstanceId,
            'HostName': HostName,
            'Password': Password,
            'SecurityGroupIds': SecurityGroupIds,
            'Description': Description,
            'EnableJumboFrame': EnableJumboFrame
        }
        runtime = util_models.RuntimeOptions(
            connect_timeout=1000000,  # 连接超时时间，单位毫秒
            read_timeout=200000  # 读取超时时间，单位毫秒
        )
        try:
            request = open_api_models.OpenApiRequest(
                query=OpenApiUtilClient.query(modify_queries)
            )
            response = client.call_api(params, request, runtime)
            print("结束：1、调用 ModifyInstanceAttribute，修改实例属性信息。")

            # 2、为使ModifyInstanceAttribute修改内容生效，调用 RebootInstance，重启实例。
            print("开始：2、为使ModifyInstanceAttribute修改内容生效，调用 RebootInstance，重启实例。")
            params = Sample.create_api_info_RebootInstance()
            reboot_queries = {
                'InstanceId': InstanceId
            }
            request = open_api_models.OpenApiRequest(
                query=OpenApiUtilClient.query(reboot_queries)
            )
            response = client.call_api(params, request, runtime)
            print("结束：2、为使ModifyInstanceAttribute修改内容生效，调用 RebootInstance，重启实例。")

            # 3、根据 InstanceId，使用 DescribeInstanceStatus 查询实例的状态
            print("开始：3、根据 InstanceId，使用 DescribeInstanceStatus 查询实例的状态。")
            RegionId = 'cn-hangzhou'  # 替换为实际的区域ID，例如"cn-hangzhou"
            params = Sample.create_api_info_DescribeInstanceStatus()
            describe_queries = {
                'RegionId': RegionId,
                'InstanceId': InstanceId
            }
            runtime = util_models.RuntimeOptions(
                connect_timeout=1000000,
                read_timeout=200000
            )

            try:
                idx = 0
                while True:
                    request = open_api_models.OpenApiRequest(
                        query=OpenApiUtilClient.query(describe_queries)
                    )
                    response = client.call_api(params, request, runtime)
                    instance_status = response['body']['InstanceStatuses']['InstanceStatus'][0]['Status']
                    if instance_status == 'Running':
                        print(f'instance:{InstanceId} is running')
                        break
                    elif instance_status in ['Stopped', 'Starting', 'Stopping']:
                        pass
                    else:
                        print(f'instance:{InstanceId} is in an unexpected status: {instance_status}')
                        return "failed"
                    idx += 1
                    if idx >= 15:
                        print(f'<success>：instance:{InstanceId} 重启超过15分钟，重启失败，退出任务。请检查输入参数是否有效。</success>')
                        return "failed"
                    time.sleep(60)
            except Exception as error:
                if error.statusCode == 404:
                    print(f'<success>：DescribeInstanceStatus 查询 {describe_queries} 失败，请下一轮继续查询。</success>')
                else:
                    traceback.print_exc()
                return "failed"
            print(
                f'<success>：调用 ModifyInstanceAttribute，修改实例属性信息。修改内容如下：{modify_queries}。并且重启指定实例，当前实例的状态：{instance_status} 。</success>')
            print("结束：3、根据 InstanceId，使用 DescribeInstanceStatus 查询实例的状态。")

            # 4、调用 ModifyInstanceNetworkSpec，设置公网带宽
            print("开始：4、调用 ModifyInstanceNetworkSpec，设置公网带宽")
            InternetMaxBandwidthOut = 5  # 替换为实际的公网出带宽最大值，单位：Mbit/s（取值范围0-100，必须大于0才能分配公网IP）
            InternetMaxBandwidthIn = 5  # 替换为实际的公网入带宽最大值，单位：Mbit/s（取值范围0-100，必须大于0才能分配公网IP）
            params = Sample.create_api_info_ModifyInstanceNetworkSpec()
            queries = {
                'InstanceId': InstanceId,
                'InternetMaxBandwidthOut': InternetMaxBandwidthOut,
                'InternetMaxBandwidthIn': InternetMaxBandwidthIn
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
                print(f"实例 {InstanceId} 公网带宽设置成功")
            except Exception as error:
                if error.statusCode == 404:
                    print(f'<success>：ModifyInstanceNetworkSpec 设置公网带宽 {queries} 失败，请下一轮继续设置。</success>')
                else:
                    traceback.print_exc()
                return "failed"
            print("结束：4、调用 ModifyInstanceNetworkSpec，设置公网带宽")

            # 5、调用 AllocatePublicIpAddress，分配公网IP地址。
            print("开始：5、调用 AllocatePublicIpAddress，分配公网IP地址。")
            params = Sample.create_api_info_AllocatePublicIpAddress()
            queries = {
                'InstanceId': InstanceId
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
                print("结束：5、调用 AllocatePublicIpAddress，分配公网IP地址。")

                # 6、根据 InstanceId，使用 DescribeInstanceAttribute 查询实例的公网IP地址信息
                print("开始：6、根据 InstanceId，使用 DescribeInstanceAttribute 查询实例的公网IP地址信息")
                params = Sample.create_api_info_DescribeInstanceAttribute()
                queries = {
                    'InstanceId': InstanceId
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
                        public_ip_address = response['body']['PublicIpAddress']['IpAddress']
                        if public_ip_address:
                            print(f'instance:{InstanceId} has public IP address: {public_ip_address}')
                            break
                        else:
                            print(f'instance:{InstanceId} does not have public IP address yet')

                        idx += 1
                        if idx >= 15:
                            print(f'<success>：调用 AllocatePublicIpAddress 为实例:{InstanceId} 分配公网IP失败。超过15分钟仍然未完成，退出任务。请检查输入参数是否有效。</success>')
                            return "failed"
                        time.sleep(60)
                except Exception as error:
                    if error.statusCode == 404:
                        print(
                            f'<success>：DescribeInstanceAttribute 查询公网IP {queries} 失败，请下一轮继续查询。</success>')
                    else:
                        traceback.print_exc()
                    return "failed"
                # 针对查询类函数，需要打印代码执行成果
                print(f'<success>：调用 AllocatePublicIpAddress，为实例: {InstanceId} 分配公网IP地址。所分配的公网IP地址: {public_ip_address} 。公网出带宽最大值: {InternetMaxBandwidthOut}Mb，公网入带宽最大值: {InternetMaxBandwidthIn}Mb。</success>')
                print("结束：6、根据 InstanceId，使用 DescribeInstanceAttribute 查询实例的公网IP地址信息")
                return "Success"
            except Exception as error:
                if error.statusCode == 404:
                    print(f'<success>：AllocatePublicIpAddress 分配公网IP {queries} 失败，请下一轮继续分配。</success>')
                else:
                    traceback.print_exc()
                return "failed"
        except Exception as error:
            if error.statusCode == 404:
                print(f'<success>：ModifyInstanceAttribute 修改 {modify_queries} 失败，请下一轮继续修改。</success>')
            else:
                traceback.print_exc()
            return "failed"


if __name__ == '__main__':
    result = Sample.main(sys.argv[1:])
    print(result)