

class DataVWebResInfo:

    @staticmethod
    def success(data={}, msg="成功"):
        return {"state": "success", "data": data, "msg": msg}

    @staticmethod
    def success_page(data, total):
        return {"state": "success", "data": data, "total": total, "msg": "成功"}

    @staticmethod
    def error(data, msg):
        return {"state": "error", "data": data, "msg": msg}

    @staticmethod
    def skip_to_rpa_service(request_url: str, request_params: dict):
        request_url = "rpa"+request_url
        return {"state": "success", "request_url": request_url, "request_params": request_params,
                "response_type": "skip"}

