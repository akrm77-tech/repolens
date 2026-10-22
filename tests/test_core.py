from pathlib import Path
from repolens.core import diff, render_markdown, scan

def make_repo(tmp_path: Path):
    (tmp_path / "app.py").write_text("import os\n\nclass Greeter:\n    def hello(self):\n        return 'hi'\n", encoding="utf-8")
    (tmp_path / "web.ts").write_text("import x from './x'\nexport function render() {}\n", encoding="utf-8")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "bad.py").write_text("def no(): pass", encoding="utf-8")

def test_scan_extracts_symbols_and_ignores_dependencies(tmp_path):
    make_repo(tmp_path)
    index = scan(tmp_path)
    assert [f.path for f in index.files] == ["app.py", "web.ts"]
    assert [s.name for s in index.files[0].symbols] == ["Greeter", "hello"]
    assert index.files[1].imports == ["./x"]

def test_markdown_is_localized(tmp_path):
    make_repo(tmp_path)
    assert "الملفات" in render_markdown(scan(tmp_path), "ar")

def test_diff_detects_changes(tmp_path):
    make_repo(tmp_path)
    before = scan(tmp_path)
    (tmp_path / "new.go").write_text("package main\nfunc Main() {}", encoding="utf-8")
    (tmp_path / "app.py").write_text("def changed(): pass", encoding="utf-8")
    result = diff(before, scan(tmp_path))
    assert result["added"] == ["new.go"]
    assert result["changed"] == ["app.py"]
