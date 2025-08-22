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
功能：将ECS实例添加到SLB后端服务器组并启动监听
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
    def create_api_info_AddBackendServers() -> open_api_models.Params:
        params = open_api_models.Params(
            action='AddBackendServers',
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
    def create_api_info_DescribeLoadBalancerAttribute() -> open_api_models.Params:
        params = open_api_models.Params(
            action='DescribeLoadBalancerAttribute',
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
    def create_api_info_CreateLoadBalancerTCPListener() -> open_api_models.Params:
        params = open_api_models.Params(
            action='CreateLoadBalancerTCPListener',
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
    def create_api_info_DescribeLoadBalancerTCPListenerAttribute() -> open_api_models.Params:
        params = open_api_models.Params(
            action='DescribeLoadBalancerTCPListenerAttribute',
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

        # 1、调用 AddBackendServers，获取返回的SLB LoadBalancerId。
        print("开始：1、调用 AddBackendServers，获取返回的SLB LoadBalancerId。")
        params = Sample.create_api_info_AddBackendServers()
        RegionId = 'cn-hangzhou'
        LoadBalancerId = 'lb-bxxxxxxxxb9'
        BackendServers = '[{"ServerId":"i-bp1bxxxxxxxxpafi","ServerIp":"190.0.0.8","Port":22,"Type":"ecs","Weight":100}]'

        queries = {
            'RegionId': RegionId,
            'LoadBalancerId': LoadBalancerId,
            'BackendServers': BackendServers
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
            loadbalancer_id = queries['LoadBalancerId']
            print("结束：1、调用 AddBackendServers，获取返回的SLB LoadBalancerId。")

            # 2、根据 LoadBalancerId，使用 DescribeLoadBalancerAttribute 查询负载均衡SLB实例的详细信息
            print("开始：2、根据 LoadBalancerId，使用 DescribeLoadBalancerAttribute 查询负载均衡SLB实例的详细信息")
            params = Sample.create_api_info_DescribeLoadBalancerAttribute()
            queries = {
                'LoadBalancerId': loadbalancer_id
            }
            runtime = util_models.RuntimeOptions(
                connect_timeout=1000000,  # 连接超时时间，单位毫秒
                read_timeout=200000  # 读取超时时间，单位毫秒
            )

            try:
                idx = 0
                import json
                BackendServers = json.loads(BackendServers)
                while True:
                    flag_create_api_info_DescribeLoadBalancerAttribute = False
                    request = open_api_models.OpenApiRequest(
                        query=OpenApiUtilClient.query(queries)
                    )
                    response = client.call_api(params, request, runtime)
                    print(f'BackendServers:{BackendServers}')
                    backend_servers = response['body']['BackendServers']['BackendServer']
                    print(f'backend_servers:{backend_servers}')
                    for BackendServers_instance in BackendServers:
                        BackendServers_instance_id = BackendServers_instance['ServerId']
                        BackendServers_instance_Type = BackendServers_instance['Type']
                        server_status = [server['Weight'] for server in backend_servers if server['ServerId'] == BackendServers_instance_id]
                        print(f'server_status:{server_status}')
                        if server_status[0] == 100: # 后端服务器的权重100
                            flag_create_api_info_DescribeLoadBalancerAttribute = True
                            break
                    if flag_create_api_info_DescribeLoadBalancerAttribute == True:
                        break

                    idx += 1
                    if idx >= 15:
                        print(f'<success>：loadbalancer:{loadbalancer_id} 添加后端服务器超过15分钟，创建失败，退出任务。</success>')
                        return "failed"
            except Exception as error:
                if error.statusCode == 404:
                    print(f'<success>：DescribeLoadBalancerAttribute 查询 {queries} 查询失败，请下一轮继续查询。</success>')
                else:
                    traceback.print_exc()
                return "failed"
            # 针对查询类函数，需要打印代码执行成果
            print(
                f'<success>：调用 AddBackendServers，获取返回的 LoadBalancerId:{loadbalancer_id} ，根据 LoadBalancerId，使用 DescribeLoadBalancerAttribute 查询负载均衡SLB实例的后端服务器信息：{BackendServers} 。</success>')
            print("结束：2、根据 LoadBalancerId，使用 DescribeLoadBalancerAttribute 查询负载均衡SLB实例的详细信息")

        except Exception as error:
            # 错误 message
            if error.statusCode == 404:
                print(f'<success>：AddBackendServers 添加 {queries} 失败，请下一轮继续添加。</success>')
            else:
                traceback.print_exc()
            return "failed"

        # 3、调用 CreateLoadBalancerTCPListener，获取返回的 LoadBalancerId 和 ListenerPort。
        print("开始：3、调用 CreateLoadBalancerTCPListener，获取返回的 LoadBalancerId 和 ListenerPort。")
        params = Sample.create_api_info_CreateLoadBalancerTCPListener()
        RegionId = 'cn-hangzhou'
        LoadBalancerId = 'lb-bp1xxxxxxxb9'
        ListenerPort = '22'
        queries = {
            'RegionId': RegionId,
            'LoadBalancerId': LoadBalancerId,
            'ListenerPort': ListenerPort,
            'BackendServerPort': '22',
            'Bandwidth': '-1',
            'HealthCheckSwitch': 'on',
            'HealthCheckDomain': '$_ip',
            'HealthCheckType': 'tcp',
            'HealthCheckConnectPort': '22'
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
            print("结束：3、调用 CreateLoadBalancerTCPListener，获取返回的 LoadBalancerId 和 ListenerPort。")

            # 4、根据 LoadBalancerId 和 ListenerPort，使用 DescribeLoadBalancerTCPListenerAttribute 查询实例的状态
            print("开始：4、根据 LoadBalancerId 和 ListenerPort，使用 DescribeLoadBalancerTCPListenerAttribute 查询实例的状态")
            params = Sample.create_api_info_DescribeLoadBalancerTCPListenerAttribute()
            queries = {
                'RegionId': RegionId,
                'LoadBalancerId': LoadBalancerId,
                'ListenerPort': ListenerPort
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
                    status = response['body']['Status'] # CreateLoadBalancerTCPListener 新建的监听的状态为 stopped。创建完成后，调用 StartLoadBalancerListener 接口启动监听来转发流量。
                    if status == 'stopped':
                        print(f'LoadBalancerId:{LoadBalancerId} , listener:{ListenerPort} is Stopped')
                        break
                    else:
                        print(f'LoadBalancerId:{LoadBalancerId} , listener:{ListenerPort} is {status}')
                        time.sleep(60)
                    idx += 1
                    if idx >= 15:
                        print(f'<success>：调用 CreateLoadBalancerTCPListener，LoadBalancerId:{LoadBalancerId} , listener:{ListenerPort} 创建超过15分钟，创建失败，退出任务。</success>')
                        return "failed"
            except Exception as error:
                if error.statusCode == 404:
                    print(f'<success>：DescribeLoadBalancerTCPListenerAttribute 查询 {queries} 查询失败，请下一轮继续查询。</success>')
                else:
                    traceback.print_exc()
                return "failed"
            # 针对查询类函数，需要打印代码执行成果
            print(
                f'<success>：调用 CreateLoadBalancerTCPListener，获取返回的 LoadBalancerId:{LoadBalancerId} , listener:{ListenerPort}，根据 LoadBalancerId 和 ListenerPort，使用 DescribeLoadBalancerTCPListenerAttribute 查询实例的状态：{status} 。</success>')
            print("结束：4、根据 LoadBalancerId 和 ListenerPort，使用 DescribeLoadBalancerTCPListenerAttribute 查询实例的状态")

            return "Success"
        except Exception as error:
            if error.statusCode == 404:
                print(f'<success>：CreateLoadBalancerTCPListener 创建 {queries} 失败，请下一轮继续创建。</success>')
            else:
                traceback.print_exc()
            return "failed"


if __name__ == '__main__':
    result = Sample.main(sys.argv[1:])
    print(result)