import json
import logging
import requests
from typing import Type, TypeVar, Union
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)

baseApiUrl = "https://canvas.ssu.ac.kr/learningx/api/v1"

T = TypeVar('T')


@dataclass
class ApiResponse:
    ok: bool
    result: Union[None, T]
    status: int


def api(url: str, token: str, init: dict = {}, response_class: Type[T] = None) -> ApiResponse:
    headers = init.get('headers', {})
    headers['Authorization'] = f"Bearer {token}"
    init['headers'] = headers

    response = requests.request(init.get('method', 'GET'), f"{baseApiUrl}{url}", headers=headers,
                                data=init.get('body', None))

    if response.status_code == 200:
        result = json.loads(response.text)
        logging.info(result)
        if response_class:
            if isinstance(result, list):
                result = [response_class(**item) for item in result]
            else:
                result = response_class(**result)
        # logging.info(f"fetch: url={url}, token={token}, result={result}, setCookie={response.cookies}")
        return ApiResponse(True, result, response.status_code)
    else:
        # logging.error(f"response: {response.text}, status: {response.status_code}")
        return ApiResponse(False, None, response.status_code)
