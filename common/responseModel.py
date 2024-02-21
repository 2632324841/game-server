def response(code:int = 200, message:str = 'ok', data = None, success:bool = True):
    return {'code':code, 'message':message, 'data':data, 'success':success}