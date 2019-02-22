# encoding: utf-8
"""
@author: liuyun
@time: 2019/1/10/010 11:13
@desc:
"""


from MockServerClient import MockServerClient, request, response, times, request_for_callback, clientId

if __name__ == '__main__':
    client = MockServerClient("192.168.1.193", "5003")

    print("回调测试,返回结果依赖 request")
    def request_handle(request):
        '''
            自行解析request
        '''
        return {"code": 0, "msg": "sucess"}

    def request_test(id):
        return request_for_callback(clientId(id),
                         request(method="GET", path="/that/thing"),
                         times(1))

    client.mock_callback(request_test, request_handle)
    print("普通mock, 不依赖request")
    client.stub(
        request(method="GET", path="/aaa"),
        response(code=200, body="i'm a teapot", headers={"hi": "haa"}),
        times(60)
    )






