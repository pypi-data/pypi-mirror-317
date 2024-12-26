from config.setting import logger, token_middleware
from fastapi import Request


def func_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"在函数 {func.__name__} 中捕获到异常: {e}")

    return wrapper


def func_requests(func):
    def wrapper(
        request: Request,
        data: dict = None,
    ):
        try:
            if not data:
                data = {}
            token = request.headers.get("Authorization")
            logger.info(request.headers)
            if token:
                res = token_middleware.jwt.decode_token(token)
                if not res:
                    return {"errorcode": "9999", "msg": "token无效"}
                data.update({"payload": res})
            else:
                return {"errorcode": "9999", "msg": "token无效"}
        except Exception as e:
            return {"errorcode": "9999", "msg": "token无效"}
        try:
            data.update(
                {
                    "request": request,
                }
            )
            logger.info(
                f""" 收到请求: {request.base_url}{request.url.path[1:]} 
                        
请求来源: {request.client.host}
请求地址: {request.base_url}{request.url.path[1:]}                        
请求参数: {data}

            """
            )
            return func(data)
        except Exception as e:
            print(f"在函数 {func.__name__} 中捕获到异常: {e}")
            return {"errorcode": "9999", "msg": "未知错误"}

    return wrapper
