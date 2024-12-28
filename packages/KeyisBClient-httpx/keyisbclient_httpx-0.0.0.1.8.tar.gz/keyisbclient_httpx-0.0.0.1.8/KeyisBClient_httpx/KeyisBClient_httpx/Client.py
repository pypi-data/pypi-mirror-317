





import typing
import httpx
from KeyisBLogging import logging
from KeyisBClient import Exceptions, Url
from KeyisBClient.models import Request, Response



class Client:
    def __init__(self):
        self.protocols = {
            'http': {'versions': ['1.1', '2'], 'last': '2', 'default': '1.1'},  # HTTP versions 1.1 and 2
            'https': {'versions': ['1.1', '2'], 'last': '2', 'default': '1.1'},  # HTTPS versions 1.1 and 2
            'ws': {'versions': ['1.0']},  # WebSocket (WS) - Версия 1.0 для обмена данными в реальном времени
            'wss': {'versions': ['1.0']}  # WebSocket Secure (WSS) - защищённая версия WebSocket
        }

        self.__httpAsyncClient = httpx.AsyncClient(verify=True, follow_redirects=True)
        self.__httpClient = httpx.Client(verify=True, follow_redirects=True)
        

    async def requestAsync(self, request: Request) -> Response:
        try:
            response = await self.__httpAsyncClient.request(
                method=request.method,
                url=request.url.getUrl(),
                content=request.content,
                data=request.data,
                files=request.files,
                json=request.json,
                params=request.params,
                headers=request.headers,
                cookies=request.cookies,
                auth=request.auth,
                follow_redirects=request.follow_redirects,
                timeout=request.timeout,
                extensions=request.extensions
            )
            try:
                json = response.json()
            except:
                json = None

            return Response(
                    status_code=response.status_code,
                    headers=response.headers,
                    content=response.content,
                    text=response.text,
                    json=json,
                    stream=response.aiter_bytes(),
                    request=request,
                    extensions=response.extensions,
                    history=None,
                    default_encoding=response.encoding or "utf-8",
                    url=Url(str(response.url))
                )
        except httpx.TimeoutException:
            logging.debug("HTTPS request timed out")
            raise Exceptions.ServerTimeoutError()
        except httpx.ConnectError:
            logging.debug("Failed to connect to server")
            raise Exceptions.ErrorConnection()
        except httpx.HTTPStatusError as e:
            logging.debug(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise Exceptions.InvalidServerResponseError(message=f"Некорректный ответ от сервера: {e.response.status_code}")
        except httpx.RequestError as e:
            logging.debug(f"HTTPS request failed: {e}")
            raise Exceptions.UnexpectedError(message=f"Неожиданная ошибка запроса HTTPS: {str(e)}")

    def requestSync(self, request: Request) -> Response:
        try:
            
            response = self.__httpClient.request(
                method=request.method,
                url=request.url.getUrl(),
                content=request.content,
                data=request.data,
                files=request.files,
                json=request.json,
                params=request.params,
                headers=request.headers,
                cookies=request.cookies,
                auth=request.auth,
                follow_redirects=request.follow_redirects,
                timeout=request.timeout,
                extensions=request.extensions
            )
            try:
                json = response.json()
            except:
                json = None

            return Response(
                    status_code=response.status_code,
                    headers=response.headers,
                    content=response.content,
                    text=response.text,
                    json=json,
                    stream=response.aiter_bytes(),
                    request=request,
                    extensions=response.extensions,
                    history=None,
                    default_encoding=response.encoding or "utf-8",
                    url=Url(str(response.url))
                )
        except httpx.TimeoutException:
            logging.debug("HTTPS request timed out")
            raise Exceptions.ServerTimeoutError()
        except httpx.ConnectError:
            logging.debug("Failed to connect to server")
            raise Exceptions.ErrorConnection()
        except httpx.HTTPStatusError as e:
            logging.debug(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise Exceptions.InvalidServerResponseError(message=f"Некорректный ответ от сервера: {e.response.status_code}")
        except httpx.RequestError as e:
            logging.debug(f"HTTPS request failed: {e}")
            raise Exceptions.UnexpectedError(message=f"Неожиданная ошибка запроса HTTPS: {str(e)}")
        
    async def streamAsync(self, request: Request) -> typing.AsyncIterator[Response]:
        async with self.__httpAsyncClient.stream(
                method=request.method,
                url=request.url.getUrl(),
                content=request.content,
                data=request.data,
                files=request.files,
                json=request.json,
                params=request.params,
                headers=request.headers,
                cookies=request.cookies,
                follow_redirects=request.follow_redirects,
                timeout=request.timeout,
                extensions=request.extensions
                ) as response:
                
                try:
                    json = response.json()
                except:
                    json = None

                    yield Response(
                    status_code=response.status_code,
                    headers=response.headers,
                    content=response.content,
                    text=response.text,
                    json=json,
                    stream=response.aiter_bytes(),
                    request=request,
                    extensions=response.extensions,
                    history=None,
                    default_encoding=response.encoding or "utf-8"
                )