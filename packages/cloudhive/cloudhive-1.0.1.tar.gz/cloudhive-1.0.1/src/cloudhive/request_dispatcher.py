import json
import socket


class BaseHttpReq(object):
    def __init__(self, host: None | str = None, socket_file: None | str = None, *args, **kwargs):
        if "logger" in kwargs:
            self.logger = kwargs['logger']

        self._line_end = "\r\n"
        self.host = host or "localhost"
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.connection_file = socket_file or "/var/run/docker.sock"
        self.__connect()

    def _send_request(self, request: bytes):
        try:
            self.socket.sendall(request)
        except Exception:
            raise Exception("Error while sending the request")

    def _receive_data(self, buffer_size: None | int =None):
        if not buffer_size:
            buffer_size = 4096

        data = b""
        while True:
            part = self.socket.recv(buffer_size)
            data += part
            if len(part) < buffer_size:
                break
        return data

    def __connect(self):
        self.socket.connect(self.connection_file)

    @staticmethod
    def _endpoint_generator(url: str, params: dict) -> str:
        _st = f"{url}?"
        _st += "&".join(f"{key}={str(value)}" for key, value in params.items())
        return _st

    def _common_ops(self,
                    method,
                    url,
                    content_type=None,
                    payload=None,
                    query_param=None):

        if query_param:
            url = self._endpoint_generator(url=url, params=query_param)

        _request = self._dispatch(method,
                                  url=url,
                                  content_type=content_type,
                                  payload=payload)
        self._send_request(_request.encode("utf-8"))
        return self._request_formatter(self._receive_data().decode("utf-8"))

    def _dispatch(self, method, url, content_type, payload=None):
        if not content_type:
            content_type = "application/json"

        _request_line = f"{method.upper()} {url} HTTP/1.1{self._line_end}"
        _headers = (
            f"Host: {self.host}{self._line_end}"
            f"Content-Type: {content_type}{self._line_end}"
        )
        if method.upper() == "POST":
            if url.find("create") != -1:
                _headers += f"Content-length: {len(json.dumps(payload))}{self._line_end}"
            if url.find("start") != -1:
                _headers += f"Content-length: 0{self._line_end}"

        _headers += self._line_end

        _body = json.dumps(payload) if payload else ""

        return _request_line + _headers + _body

    @staticmethod
    def _request_formatter(data):
        _response_status = dict()

        if "\r\n\r\n" in data:
            for idx, data in enumerate(data.split("\r\n\r\n")):
                if idx == 0:
                    for header in data.split("\r\n"):
                        if ":" in header.strip():
                            if "Date" in header:
                                _response_status['Date'] = header[6:]
                            else:
                                k, v = header.split(":")
                                _response_status[k] = v.strip()
                        else:
                            _response_status['Status-Code'] = header.strip().split("HTTP/1.1 ")[1][:3]

                elif idx == 1:
                    if "\r\n" in data:
                        data = data.split("\r\n")[1]
                    try:
                        _response_status['body'] = json.loads(data)
                    except Exception:
                        _response_status['body'] = {}

        return _response_status


class HttpReq(BaseHttpReq):

    def _get(self, url, payload=None, content_type=None, query_param=None):
        __method = "GET"
        response = self._common_ops(
            method=__method,
            url=url,
            content_type=content_type,
            payload=payload,
            query_param=query_param
        )
        return response

    def _post(self, url, payload=None, content_type=None, query_param=None):
        __method = "POST"
        response = self._common_ops(
            method=__method,
            url=url,
            content_type=content_type,
            payload=payload,
            query_param=query_param
        )
        return response

    def _delete(self, url, payload=None, content_type=None, query_param=None):
        __method = "DELETE"
        response = self._common_ops(
            method=__method,
            url=url,
            content_type=content_type,
            payload=payload,
            query_param=query_param
        )
        return response
