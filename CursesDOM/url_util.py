from urllib.parse import urlparse, ParseResult
import os

class URLHandler:

    def handle_file(self, result: ParseResult):
        pass

    def handle_http(self, result: ParseResult):
        pass
    
    def handle_https(self, result: ParseResult):
        pass

    def handle_ws(self, result: ParseResult):
        pass

    def handle_wss(self, result: ParseResult):
        pass

    def handle_null(self, result: ParseResult):
        pass


def get_resource_from_url(url, handler: URLHandler):
    result = urlparse(url)
    if result.scheme == "file":
        return handler.handle_file(result)
    elif result.scheme == "http":
        return handler.handle_http(result)
    elif result.scheme == "":
        return handler.handle_null(result)


class FileSchemeHandler(URLHandler):
    def handle_file(self, result: ParseResult):
        with open(os.path.join(os.getcwd(), result.path), "r") as fp:
            return fp.read()
    