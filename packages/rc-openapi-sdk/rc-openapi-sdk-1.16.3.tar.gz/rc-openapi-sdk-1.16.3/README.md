# RC-OpenAPI-SDK

融创开放API平台接口调用SDK

## 安装&使用
安装:
```shell
pip install rc-openapi-sdk
```
使用案例:
```python
from rc_openapi_sdk import OpenAPI

if __name__ == '__main__':
    rc_api = OpenAPI(ssl_verify=False)
    # data = rc_api.investment_promotion_regional("650000", "mcxfhy38160")
    data = rc_api.investment_promotion_ranking("440000", "mccy778")
    print(data)
```