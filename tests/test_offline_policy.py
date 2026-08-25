from pathlib import Path


def test_project_documents_offline_portfolio_policy():
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "offline" in readme.lower()
    assert "confidential" in readme.lower()
    assert "حفظ" in readme or "sanit" in readme.lower()
