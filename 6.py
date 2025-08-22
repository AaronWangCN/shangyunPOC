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
功能：云管理员把该账号下所有按量付费的实例的云安全中心设置为防病毒版
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
     
        config.endpoint = 'tds.cn-shanghai.aliyuncs.com'
        return OpenApiClient(config)
    @staticmethod
    def create_api_info() -> open_api_models.Params:
        params = open_api_models.Params(
            action='UpdatePostPaidBindRel',
            version='2018-12-03',
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
        params = Sample.create_api_info()
        ApiFunction = 'c' # 参考填写说明，用于实现api的具体功能。
        Version = "6" # 替换为实际的Version, 如6
        print(\"开始：1、调用 UpdatePostPaidBindRel，对云安全中心的相关信息进行修改。")

        # query params api的参数在下方填入
        queries = {}
        queries['BindAction.1.Version'] = Version
        queries['BindAction.1.BindAll'] = 'true'

        # runtime options
        runtime = util_models.RuntimeOptions(
            connect_timeout=1000000,
            read_timeout=200000
        )
        try:
            request = open_api_models.OpenApiRequest(
                query=OpenApiUtilClient.query(queries),
                
            )
            version_map_dict = {'1':'免费版', '3':'企业版', '5':'高级版','6':'防病毒版','7':'旗舰版'}
            chinese_version = version_map_dict[str(Version)]
            response = client.call_api(params, request, runtime)
            response_body = response['body']
            if ApiFunction == 'c':
                if response_body['ResultCode'] == 0:
                    print(f'''<success>结束：调用 UpdatePostPaidBindRel，成功修改当前账号下所有按量付费的云产品的云安全中心（Sas）版本为 {chinese_version} </success>''')
                    print(\"结束：1、调用 UpdatePostPaidBindRel，对云安全中心的相关信息进行修改。")
                    return "Success"
                else:
                    print(f'''<success>结束：调用 UpdatePostPaidBindRel，未成功修改当前账号下所有按量付费的云产品的云安全中心（Sas）版本为{chinese_version}， 返回的响应体为{response_body}。</success>''')
                    print(\"结束：1、调用 UpdatePostPaidBindRel，对云安全中心的相关信息进行修改。")
                    return 'failed'    

            
        except Exception as error:
            if error.statusCode == 404:
                print(f'<success>:UpdatePostPaidBindRel 执行修改{queries}失败，请下一轮继续修改。</success>')
            else:
                traceback.print_exc()        
            return "failed"

if __name__ == '__main__':
    result = Sample.main(sys.argv[1:])
    print(result)
