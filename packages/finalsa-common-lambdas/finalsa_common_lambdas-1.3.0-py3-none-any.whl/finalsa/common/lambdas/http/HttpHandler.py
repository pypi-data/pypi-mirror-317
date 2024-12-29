from finalsa.traceability.functions import (
    HTTP_HEADER_CORRELATION_ID,
    HTTP_HEADER_TRACE_ID,
)
from finalsa.traceability import (
    set_context,
)
from finalsa.common.lambdas.http.HttpResponse import HttpResponse
from finalsa.common.lambdas.http.HttpQueryParams import HttpQueryParams
from finalsa.common.lambdas.http.HttpHeaders import HttpHeaders
from typing import Callable, Optional, Union, Dict, Any, List, Tuple
from pydantic import BaseModel
from orjson import loads, dumps
from logging import Logger, getLogger
from re import match


class HttpHandler():

    @classmethod
    def test(cls) -> 'HttpHandler':
        return cls("test", getLogger("test"))

    def __init__(self, app_name: str, logger: Logger) -> None:
        self.handlers = {}
        self.logger = logger
        self.app_name = app_name
        self.regex_expressions = {}

    @staticmethod
    def match_key(regex_dict: Dict[str, Any], path: str) -> Optional[Tuple[str, Any]]:
        for key, value in regex_dict.items():
            match_result = match(key, path)
            if match_result and match_result.group(0) == path:
                return value, match_result.groups()
        return None, None

    @staticmethod
    def get_fixed_path(splited_path: List[str]) -> str:
        result = "/"
        for part in splited_path:
            result += f"{part}/"
        return result

    @staticmethod
    def get_regex_path(splited_path: List[str], args: List[str]) -> str:
        regex = "/"
        for part in splited_path:
            if part in args:
                regex += f"(?P<{part}>[^/]+)/"
                continue
            regex += f"{part}/"
        return regex

    def validate_handler(self, path: str, method: str) -> Dict:
        fixed_path = path if path.startswith("/") else f"/{path}"
        splited_path = fixed_path.split("/")
        splited_path = list(filter(lambda x: x != "", splited_path))
        if len(splited_path) < 1:
            raise ValueError("Path must have at least 1 parts")
        if len(splited_path) > 5:
            raise ValueError("Path must have at most 5 parts")
        keys = []
        fixed_args = []
        for part in splited_path:
            if not part.startswith("{") or not part.endswith("}"):
                keys.append(part)
                continue
            arg_name = part[1:-1]
            keys.append(arg_name)
            fixed_args.append(arg_name)

        real_path = self.get_fixed_path(keys)
        if real_path in self.handlers and method in self.handlers[real_path]:
            raise ValueError("Path already has a handler")
        regex_exp = self.get_regex_path(keys, fixed_args)
        return {
            "path": real_path,
            "fixed_args": fixed_args,
            "regex": regex_exp
        }

    def handler(
            self,
            path: str,
            method: Optional[str] = "POST",
            headers: Optional[Dict[str, str]] = {}
    ) -> Callable:
        params = self.validate_handler(path, method)
        methods = [method]
        if method == "POST":
            methods.append("OPTIONS")

        def decorator(handler: Callable) -> Callable:
            def wrapper(*args, **kwargs) -> Optional[Union[Dict, str]]:
                self.logger.info("Processing http event", extra={
                    "path": path,
                    "method": method
                })
                try:
                    result = handler(*args, **kwargs)
                    self.logger.info("Processed http event")
                    return result
                except Exception as e:
                    self.logger.error("Error processing http event", extra={
                        "error": e,
                    })
                    self.logger.exception(e)
                    return {
                        "message": "Internal Server Error"
                    }, 500
            real_path = params["path"]
            regex_path = params["regex"]
            for method in methods:
                self.handlers[method][real_path] = {
                    "handler": wrapper,
                    "function_args": handler.__annotations__,
                    "headers": headers or {},
                    **params
                }
                self.regex_expressions[method][regex_path] = real_path
            return wrapper
        return decorator

    def default(self, headers: Optional[Dict[str, str]] = {}) -> Callable:
        return self.post("default", headers)

    def post(self, path: str, headers: Optional[Dict[str, str]] = {}) -> Callable:
        if "POST" not in self.handlers:
            self.handlers["POST"] = {}
            self.regex_expressions["POST"] = {}
        if "OPTIONS" not in self.handlers:
            self.handlers["OPTIONS"] = {}
            self.regex_expressions["OPTIONS"] = {}
        return self.handler(path, "POST", headers)

    def get(self, path: str, headers: Optional[Dict[str, str]] = {}) -> Callable:
        if "GET" not in self.handlers:
            self.handlers["GET"] = {}
            self.regex_expressions["GET"] = {}
        return self.handler(path, "GET", headers)

    def put(self, path: str, headers: Optional[Dict[str, str]] = {}) -> Callable:
        if "PUT" not in self.handlers:
            self.handlers["PUT"] = {}
            self.regex_expressions["PUT"] = {}
        return self.handler(path, "PUT", headers)

    def delete(self, path: str, headers: Optional[Dict[str, str]] = {}) -> Callable:
        if "DELETE" not in self.handlers:
            self.handlers["DELETE"] = {}
            self.regex_expressions["DELETE"] = {}
        return self.handler(path, "DELETE", headers)

    def patch(self, path: str, headers: Optional[Dict[str, str]] = {}) -> Callable:

        if "PATCH" not in self.handlers:
            self.handlers["PATCH"] = {}
            self.regex_expressions["PATCH"] = {}
        return self.handler(path, "PATCH", headers)

    def options(self, path: str, headers: Optional[Dict[str, str]] = {}) -> Callable:
        if "OPTIONS" not in self.handlers:
            self.handlers["OPTIONS"] = {}
            self.regex_expressions["OPTIONS"] = {}
        return self.handler(path, "OPTIONS", headers)

    @staticmethod
    def parse_body(headers: Dict, body: str) -> Any:
        if body == "" or body is None:
            return {}
        content_type = headers.get("Content-Type", "")
        if "application/json" in content_type:
            return loads(body)
        if 'text/plain' in content_type:
            return body
        try:
            return loads(body)
        except:
            return body

    @staticmethod
    def parse_response(http_response: HttpResponse, default_headers: Dict = {}) -> Dict:
        body = http_response.body
        headers = http_response.headers or {}
        if isinstance(body, str):
            body = body
            headers["Content-Type"] = "text/plain"
        if isinstance(body, dict):
            body = dumps(body).decode("utf-8")
            headers["Content-Type"] = "application/json"
        if isinstance(body, BaseModel):
            body = body.model_dump_json()
            headers["Content-Type"] = "application/json"
        for key, value in default_headers.items():
            headers[key] = value
        return {
            "statusCode": http_response.status_code,
            "headers": headers,
            "body": body
        }

    @staticmethod
    def get_correct_response(response: Any) -> HttpResponse:
        if isinstance(response, HttpResponse):
            return response
        http_response = HttpResponse(status_code=200, body=response)
        if response is None:
            http_response.body = {
                "message": "Not Found"
            }
            http_response.status_code = 404
        if isinstance(response, tuple):
            body_response, status_code = response
            http_response.body = body_response
            http_response.status_code = status_code
        return http_response

    @staticmethod
    def get_filled_args(
        function_args: Dict[str, Any],
        parsed_args_from_path: List[str],
        args_from_path: Dict[str, str],
        query_params: Dict[str, str],
        headers: Dict[str, str],
        body: Optional[Union[Dict, str]]
    ) -> Dict:
        filled_args = {}
        for arg, value in zip(args_from_path, parsed_args_from_path):
            if arg in function_args:
                filled_args[arg] = value
        if query_params is None:
            query_params = {}
        for arg, value in query_params.items():
            if arg in function_args:
                filled_args[arg] = value
        for key in function_args:
            if key in filled_args:
                continue
            value = function_args[key]
            if value == HttpHeaders:
                filled_args[key] = HttpHeaders(headers)
            elif value == HttpQueryParams:
                filled_args[key] = HttpQueryParams(query_params)
            elif issubclass(value, BaseModel):
                filled_args[key] = value(**body)
            elif key == "body":
                filled_args[key] = body
        return filled_args

    def set_context(self, context: Any, headers: Dict) -> None:
        span_id = None
        if context is not None and hasattr(context, "aws_request_id"):
            span_id = context.aws_request_id
        set_context(
            headers.get(HTTP_HEADER_CORRELATION_ID, None),
            trace_id=headers.get(HTTP_HEADER_TRACE_ID, None),
            span_id=span_id,
            service_name=self.app_name
        )

    def process(self, event: Dict, context: Any) -> Dict:
        method = event['httpMethod']
        path = event['path']
        headers = event.get('headers')
        if not headers:
            headers = {}
        self.set_context(context, headers)
        self.logger.info("Processing http event", extra={
            "httpMethod": method,
            "path": path,
        })

        real_path = path if path.startswith("/") else f"/{path}"
        real_path = real_path if real_path.endswith("/") else f"{real_path}/"
        if self.regex_expressions.get(method) is None:
            self.logger.info("Path not found", extra={
                "httpMethod": method,
                "path": path,
            })
            return self.parse_response(HttpResponse.not_found())
        match_result, args = self.match_key(
            self.regex_expressions[method], real_path)
        if match_result is None:
            self.logger.info("Path not found", extra={
                "httpMethod": method,
                "path": path,
            })
            return self.parse_response(HttpResponse.not_found())
        handler = self.handlers[method][match_result]
        body = event.get('body', "")
        parsed_body = self.parse_body(headers, body)
        handler = self.handlers[method][match_result]
        try:
            filled_args = self.get_filled_args(
                handler["function_args"],
                args,
                handler["fixed_args"],
                event.get("queryStringParameters", {}),
                headers,
                parsed_body
            )
        except Exception as e:
            self.logger.error("Error processing http event", extra={
                "error": e,
            })
            self.logger.exception(e)
            return self.parse_response(HttpResponse.bad_request())
        method_handler = handler["handler"]
        response = method_handler(**filled_args)
        correct_response = self.get_correct_response(response)
        return self.parse_response(correct_response, handler["headers"])

    def merge(self, other: 'HttpHandler') -> None:
        for method, handlers in other.handlers.items():
            if method not in self.handlers:
                self.handlers[method] = {}
            for path, handler in handlers.items():
                if path not in self.handlers[method]:
                    self.handlers[method][path] = handler
                else:
                    raise ValueError("Path already has a handler")
        for method, regex in other.regex_expressions.items():
            if method not in self.regex_expressions:
                self.regex_expressions[method] = {}
            for regex_path, path in regex.items():
                self.regex_expressions[method][regex_path] = path
                if path not in self.handlers[method]:
                    raise ValueError("Path already has a handler")

    def set_app_name(self, app_name: str) -> None:
        self.app_name = app_name
