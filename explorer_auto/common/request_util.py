import requests
from explorer_auto.common.yaml_util import read_yaml_by_key

class RequestMain:
    session = requests.session()

    def request_main(method, url, params=None, data=None, json=None, headers=None, default_assert=True,**kwargs):
        """

        :param method: 请求方式
        :param url: 请求地址
        :param params: 字典或bytes，作为参数增加到url中
        :param data: data类型传参，字典、字节序列或文件对象，作为Request的内容
        :param json: json传参，作为Request的内容
        :param headers: 请求头，字典
        :param kwargs: 若还有其他的参数，使用可变参数字典形式进行传递
        :return:
        """
        re_data = None
        # 对异常进行捕获
        try:
            """
            封装request请求，将请求方法、请求地址，请求参数、请求头等信息入参。
            """
            url = read_yaml_by_key("base_url") + url
            print("url:",url)
            re_data = RequestMain.session.request(method, url, params=params, data=data, json=json, headers=headers, **kwargs)
            print(re_data.status_code)
            print("response:",re_data.json())
            
            if default_assert:
                if re_data.status_code != 200:
                    raise  Exception("返回码不正确")
                if re_data.json()['code'] != 0:
                    raise  Exception("返回码不正确")
                if re_data.json()['message'] != "Success":
                    raise  Exception("返回码不正确")
            else:
                if re_data.status_code == 200:
                    raise  Exception("返回码不正确")    
            
        # 异常处理 报错显示具体信息
        except Exception as e:
            # 打印异常
            print("请求失败：{0}".format(e)) 
        # 返回响应结果
        return re_data