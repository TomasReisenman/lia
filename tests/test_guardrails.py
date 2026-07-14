"""Test para verificar que los guardrails de términos prohibidos funcionan.

Uso:
    python tests/test_guardrails.py

Carga evalset.json, para cada caso verifica si el término prohibido
es detectado correctamente por la lógica en agent.py.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _term_blocked(text: str, forbidden_terms: list[str]) -> bool:
    """Replica la lógica de block_disallowed_content de agent.py."""
    lower = text.lower()
    return any(term in lower for term in forbidden_terms)


def load_evalset(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def test_evalset(evalset: list[dict], forbidden_terms: list[str]) -> tuple[int, int, list[str]]:
    passed = 0
    failed = 0
    errors: list[str] = []
    for case in evalset:
        case_id = case["id"]
        text = case["input"]
        expected = case["expected_blocked"]
        result = _term_blocked(text, forbidden_terms)
        if result == expected:
            passed += 1
        else:
            failed += 1
            status = "BLOQUEÓ (no debía)" if result else "NO BLOQUEÓ (debía)"
            errors.append(f"  [{case_id}] {status}: {text[:60]}")
    return passed, failed, errors


def main():
    config_path = HERE / "test_config.json"
    evalset_path = HERE / "evalset.json"

    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)

    print(f"[TEST] {config['test_name']}")
    print(f"  {config['description']}")
    print()

    import sys
    # agent.py vive en lia/, que está dentro del proyecto
    sys.path.insert(0, str(HERE.parent.parent))
    from lia.agent import FORBIDDEN_TERMS

    print(f"[TERMS] {len(FORBIDDEN_TERMS)} prohibidos: {', '.join(FORBIDDEN_TERMS)}")
    print()

    evalset = load_evalset(evalset_path)
    print(f"[EVALSET] {len(evalset)} casos desde {evalset_path.name}")
    print()

    passed, failed, errors = test_evalset(evalset, FORBIDDEN_TERMS)

    for err in errors:
        print(err)

    total = passed + failed
    print()
    print("=" * 40)
    print(f"  PASSED  {passed}/{total}")
    print(f"  FAILED  {failed}/{total}")
    print("=" * 40)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit(main())
