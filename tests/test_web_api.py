import json

from application.modernization_service import ModernizationService
from interface.web import _convert_payload


def test_convert_payload_success() -> None:
    status, response = _convert_payload(
        ModernizationService(),
        {
            "source_code": "START:\nIF A = 1 THEN CRT 'OK'\nGOTO START",
            "target_language": "python",
            "output_mode": "ir",
            "program_name": "TEST",
        },
    )

    assert status == 200
    assert "result" in response
    parsed = json.loads(response["result"])
    assert "repositories" in parsed
    assert "business_rules" in response
    assert "logic" in response


def test_convert_payload_requires_source() -> None:
    status, response = _convert_payload(ModernizationService(), {"source_code": ""})
    assert status == 400
    assert response["error"] == "source_code is required"
