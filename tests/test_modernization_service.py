from application.modernization_service import ModernizationService


def test_ir_mode_contains_required_keys() -> None:
    source = """
START:
READ REC FROM CUSTOMER,ID ELSE STOP
IF REC<1> = '' THEN CRT 'MISSING'
WRITE REC ON CUSTOMER,ID
GOTO START
"""
    output = ModernizationService().transform(
        source_code=source,
        program_name="CUSTOMER_LOOP",
        target_language="python",
        output_mode="ir",
    )

    assert '"entities"' in output
    assert '"repositories"' in output
    assert '"confidence_score"' in output


def test_architecture_mode_contains_layers() -> None:
    output = ModernizationService().transform(
        source_code="CRT 'HELLO'",
        program_name="HELLO",
        target_language="python",
        output_mode="architecture",
    )

    assert '"domain"' in output
    assert '"application"' in output
    assert '"infrastructure"' in output
    assert '"interface"' in output
