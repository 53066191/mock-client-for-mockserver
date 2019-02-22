# mock-client-for-mockserver
mockserver 的mockclient python版



https://github.com/internap/python-mockserver-friendly-client 在此基础上增加request依赖

普通mock:
      client = MockServerClient("192.168.1.193", "5003")
      client.stub(
        request(method="GET", path="/aaa"),
        response(code=200, body="i'm a teapot", headers={"hi": "haa"}),
        times(60)
    )
    
 
 request依赖:
 
     client = MockServerClient("192.168.1.193", "5003")
     
     '''返回处理函数'''
     def get_response(request):
        '''
            自行解析request
        '''
        return {"code": 0, "msg": "sucess"}

    '''需要Mock的函数 ''' 
     def  need_request(id):
            return request_for_callback(clientId(id),
                         request(method="GET", path="/that/thing"),
                         times(1))

     client.mock_callback(need_request, get_response)

