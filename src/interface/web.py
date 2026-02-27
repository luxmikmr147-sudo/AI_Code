from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from application.modernization_service import ModernizationService

TEMPLATE_PATH = Path(__file__).parent / "templates" / "index.html"


def _convert_payload(service: ModernizationService, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    source_code = payload.get("source_code", "")
    target_language = payload.get("target_language", "python")
    output_mode = payload.get("output_mode", "ir")
    program_name = payload.get("program_name", "WEB_INPUT")

    if not isinstance(source_code, str) or not source_code.strip():
        return HTTPStatus.BAD_REQUEST, {"error": "source_code is required"}

    try:
        transformed = service.transform_with_details(
            source_code=source_code,
            program_name=str(program_name),
            target_language=str(target_language),
            output_mode=str(output_mode),
        )
    except ValueError as exc:
        return HTTPStatus.BAD_REQUEST, {"error": str(exc)}

    return HTTPStatus.OK, {
        "result": transformed["output"],
        "business_rules": transformed["business_rules"],
        "logic": transformed["logic"],
        "assumptions": transformed["assumptions"],
        "confidence_score": transformed["confidence_score"],
    }


class WebHandler(BaseHTTPRequestHandler):
    service = ModernizationService()

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path != "/":
            self.send_error(HTTPStatus.NOT_FOUND, "Not Found")
            return

        html = TEMPLATE_PATH.read_text(encoding="utf-8").encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(html)

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/convert":
            self.send_error(HTTPStatus.NOT_FOUND, "Not Found")
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length) if content_length > 0 else b"{}"
        try:
            payload = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "invalid JSON payload"})
            return

        status, response = _convert_payload(self.service, payload)
        self._send_json(status, response)


def run_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    httpd = ThreadingHTTPServer((host, port), WebHandler)
    print(f"Web UI running on http://{host}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
