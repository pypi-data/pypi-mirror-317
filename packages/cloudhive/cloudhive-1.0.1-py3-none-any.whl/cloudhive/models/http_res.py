
class HttpRes:
    def __init__(self, attrs: dict):
        self._status_code: int = attrs.get("status_code", 200)
        self._api_version: str | None = attrs.get("api_version", None)
        self._content_type: str | None = attrs.get("content_type", "application/json")
        self._docker_experimental: bool  = attrs.get("docker_experimental", False)
        self._ostype: str | None = attrs.get("ostype", None)
        self._server: str | None = attrs.get("server", None)
        self._date: str | None = attrs.get("date", None)
        self._content_length: int = attrs.get("content_length", 0)
        self._body: dict | list = attrs.get("body", {})


    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def api_version(self):
        return self._api_version

    @property
    def content_type(self):
        return self._content_type

    @property
    def docker_experimental(self):
        return self._docker_experimental

    @property
    def ostype(self):
        return self._ostype

    @property
    def server(self):
        return self._server

    @property
    def date(self):
        return self._date

    @property
    def body(self):
        return self._body

    @property
    def content_length(self):
        return self._content_length

    @classmethod
    def format(cls, data):
        _tmp = {}
        for key, value in data.items():
            key = key.replace("-", "_").lower()
            if isinstance(value, dict):
                pass
            elif isinstance(value, list):
                pass
            elif value.isdigit():
                value = int(value)
            elif value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            _tmp[key] = value

        return cls(attrs=_tmp)
