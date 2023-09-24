import re
import httpx
import asyncio
from typing import Optional, Dict, Any

from rocketchat_API.APIExceptions.RocketExceptions import (
    RocketAuthenticationException,
    RocketConnectionException,
)

class RocketChatBase:
    API_path: str = "/api/v1/"

    def __init__(
        self,
        user: Optional[str] = None,
        password: Optional[str] = None,
        auth_token: Optional[str] = None,
        user_id: Optional[str] = None,
        server_url: str = "http://127.0.0.1:3000",
        ssl_verify: bool = True,
        proxies: Optional[Dict[str, str]] = None,
        timeout: int = 30,
        session: Optional[httpx.AsyncClient] = None,
        client_certs: Optional[str] = None,
    ) -> None:

        self.headers: Dict[str, str] = {}
        self.server_url: str = server_url
        self.proxies: Optional[Dict[str, str]] = proxies
        self.ssl_verify: bool = ssl_verify
        self.cert: Optional[str] = client_certs
        self.timeout: int = timeout
        self.req: httpx.AsyncClient = session or httpx.AsyncClient()

        # If user and password are provided, schedule the login coroutine
        if user and password:
            self.login_task: asyncio.Task = asyncio.create_task(self.login(user, password))
        elif auth_token and user_id:
            self.headers["X-Auth-Token"] = auth_token
            self.headers["X-User-Id"] = user_id
        else:
            self.login_task: Optional[asyncio.Task] = None

    @staticmethod
    def __reduce_kwargs(kwargs: Dict[str, Any]) -> Dict[str, Any]:
        if "kwargs" in kwargs:
            for arg in kwargs["kwargs"].keys():
                kwargs[arg] = kwargs["kwargs"][arg]
            del kwargs["kwargs"]
        return kwargs
    
    async def __aenter__(self) -> "RocketChatBase":
        self.req = httpx.AsyncClient(trust_env=self.ssl_verify, verify=self.ssl_verify, client_cert=self.cert, proxies=self.proxies)
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if exc_type is not None:
            print(f"Exception type: {exc_type}")
            print(f"Exception value: {exc_val}")
            print(f"Exception traceback: {exc_tb}")
        await self.req.aclose()

    async def call_api_delete(self, method: str) -> httpx.Response:
        url: str = self.server_url + self.API_path + method
        return await self.req.delete(
            url,
            headers=self.headers,
            #verify=self.ssl_verify,
            #cert=self.cert,
            #proxies=self.proxies,
            timeout=self.timeout,
        )

    async def call_api_get(self, method: str, api_path: Optional[str] = None, **kwargs: Any) -> httpx.Response:
        args: Dict[str, Any] = self.__reduce_kwargs(kwargs)
        if not api_path:
            api_path = self.API_path
        url: str = self.server_url + api_path + method
        params: str = "&".join(
            "&".join(i + "[]=" + j for j in args[i])
            if isinstance(args[i], list)
            else i + "=" + str(args[i])
            for i in args
        )
        return await self.req.get(
            "%s?%s" % (url, params),
            headers=self.headers,
            #verify=self.ssl_verify,
            #cert=self.cert,
            #proxies=self.proxies,
            timeout=self.timeout,
        )

    async def call_api_post(
        self,
        method: str,
        files: Optional[Dict[str, Any]] = None,
        use_json: Optional[bool] = None,
        **kwargs: Any
    ) -> httpx.Response:
        reduced_args: Dict[str, Any] = self.__reduce_kwargs(kwargs)
        if "password" in reduced_args and method != "users.create":
            reduced_args["pass"] = reduced_args["password"]
            del reduced_args["password"]
        if use_json is None:
            use_json = files is None
        if use_json:
            return await self.req.post(
                self.server_url + self.API_path + method,
                json=reduced_args,
                files=files,
                headers=self.headers,
                #trust_env=self.ssl_verify,
                #cert=self.cert,
                #proxies=self.proxies,
                timeout=self.timeout,
            )
        return await self.req.post(
            self.server_url + self.API_path + method,
            data=reduced_args,
            files=files,
            headers=self.headers,
            #verify=self.ssl_verify,
            #cert=self.cert,
            #proxies=self.proxies,
            timeout=self.timeout,
        )

    async def call_api_put(
        self,
        method: str,
        files: Optional[Dict[str, Any]] = None,
        use_json: Optional[bool] = None,
        **kwargs: Any
    ) -> httpx.Response:
        reduced_args: Dict[str, Any] = self.__reduce_kwargs(kwargs)
        if use_json is None:
            use_json = files is None
        if use_json:
            return await self.req.put(
                self.server_url + self.API_path + method,
                json=reduced_args,
                files=files,
                headers=self.headers,
                #verify=self.ssl_verify,
                #cert=self.cert,
                #proxies=self.proxies,
                timeout=self.timeout,
            )
        return await self.req.put(
            self.server_url + self.API_path + method,
            data=reduced_args,
            files=files,
            headers=self.headers,
            #verify=self.ssl_verify,
            #cert=self.cert,
            #proxies=self.proxies,
            timeout=self.timeout,
        )

    async def login(self, user: str, password: str) -> httpx.Response:
        request_data: Dict[str, str] = {"password": password}
        if re.match(
            r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
            user,
        ):
            request_data["user"] = user
        else:
            request_data["username"] = user
        login_request: httpx.Response = await self.req.post(
            self.server_url + self.API_path + "login",
            data=request_data,
           # verify=self.ssl_verify,
           # proxies=self.proxies,
           # cert=self.cert,
            timeout=self.timeout,
        )
        if login_request.status_code == 401:
            raise RocketAuthenticationException()

        if (
            login_request.status_code == 200
            and login_request.json().get("status") == "success"
        ):
            self.headers["X-Auth-Token"] = (
                login_request.json().get("data").get("authToken")
            )
            self.headers["X-User-Id"] = login_request.json().get("data").get("userId")
            return login_request

        raise RocketConnectionException()

    async def logout(self, **kwargs: Any) -> httpx.Response:
        return await self.call_api_post("logout", kwargs=kwargs)

    async def info(self, **kwargs: Any) -> httpx.Response:
        return await self.call_api_get("info", api_path="/api/", kwargs=kwargs)