import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def version():
    return os.environ.get("VERSION", "dev")


def log(event, **fields):
    record = {"event": event, "version": version(), **fields}
    print(json.dumps(record, ensure_ascii=False), flush=True)


def response_for(path):
    if path == "/health":
        return 200, {"status": "ok", "version": version()}
    return 404, {"status": "not_found", "version": version()}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?", 1)[0]
        status, payload = response_for(path)
        body = json.dumps(payload).encode()
        log("request", method=self.command, path=path, status=status)
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        return


def main():
    port = int(os.environ.get("PORT", "8080"))
    log("startup", port=port)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
