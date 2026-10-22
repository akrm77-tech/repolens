from __future__ import annotations

import hashlib
import os
import re
from collections.abc import Iterable
from dataclasses import asdict, dataclass, field
from pathlib import Path

LANGUAGES = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".rs": "Rust",
    ".go": "Go",
    ".java": "Java",
    ".kt": "Kotlin",
    ".kts": "Kotlin",
    ".cs": "C#",
    ".cpp": "C++",
    ".cc": "C++",
    ".c": "C",
    ".h": "C/C++",
    ".hpp": "C++",
    ".rb": "Ruby",
    ".php": "PHP",
    ".swift": "Swift",
    ".scala": "Scala",
    ".sh": "Shell",
    ".sql": "SQL",
}
SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    "target",
    "__pycache__",
    ".idea",
    ".tox",
}
SKIP_NAMES = {
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "Cargo.lock",
    "poetry.lock",
}
LABELS = {
    "en": {
        "title": "Repository Lens",
        "summary": "Local repository intelligence",
        "files": "Files",
        "symbols": "Symbols",
        "imports": "Imports",
        "unknown": "Unknown",
    },
    "ar": {
        "title": "عدسة المستودع",
        "summary": "فهم محلي للمستودع",
        "files": "الملفات",
        "symbols": "الرموز",
        "imports": "الاستيرادات",
        "unknown": "غير معروف",
    },
    "es": {
        "title": "Lente del repositorio",
        "summary": "Inteligencia local del repositorio",
        "files": "Archivos",
        "symbols": "Símbolos",
        "imports": "Importaciones",
        "unknown": "Desconocido",
    },
    "fr": {
        "title": "Lentille du dépôt",
        "summary": "Intelligence locale du dépôt",
        "files": "Fichiers",
        "symbols": "Symboles",
        "imports": "Imports",
        "unknown": "Inconnu",
    },
    "zh": {
        "title": "仓库透镜",
        "summary": "本地代码仓库智能",
        "files": "文件",
        "symbols": "符号",
        "imports": "导入",
        "unknown": "未知",
    },
}


@dataclass
class Symbol:
    name: str
    kind: str
    line: int


@dataclass
class FileNode:
    path: str
    language: str
    sha256: str
    lines: int
    symbols: list[Symbol] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)


@dataclass
class RepositoryIndex:
    root: str
    generated_at: str
    files: list[FileNode]

    def to_dict(self) -> dict:
        return {
            "schema": "repolens/v1",
            "root": self.root,
            "generated_at": self.generated_at,
            "files": [{**asdict(f), "symbols": [asdict(s) for s in f.symbols]} for f in self.files],
        }

    def find(self, query: str) -> list[FileNode]:
        q = query.lower()
        return [
            f
            for f in self.files
            if q in f.path.lower() or any(q in s.name.lower() for s in f.symbols)
        ]


def _symbols(text: str, language: str) -> list[Symbol]:
    patterns = {
        "Python": [
            (r"^\s*(?:async\s+)?def\s+(\w+)", "function"),
            (r"^\s*class\s+(\w+)", "class"),
        ],
        "JavaScript": [
            (r"^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)", "function"),
            (r"^\s*class\s+(\w+)", "class"),
            (r"^\s*(?:export\s+)?const\s+(\w+)\s*=", "constant"),
        ],
        "TypeScript": [
            (r"^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)", "function"),
            (r"^\s*class\s+(\w+)", "class"),
            (r"^\s*(?:export\s+)?(?:const|interface|type)\s+(\w+)", "declaration"),
        ],
        "Go": [
            (r"^\s*func\s+(?:\([^)]*\)\s*)?(\w+)", "function"),
            (r"^\s*type\s+(\w+)", "type"),
        ],
        "Rust": [
            (r"^\s*(?:pub\s+)?(?:async\s+)?fn\s+(\w+)", "function"),
            (r"^\s*(?:pub\s+)?struct\s+(\w+)", "struct"),
            (r"^\s*(?:pub\s+)?enum\s+(\w+)", "enum"),
        ],
        "Java": [
            (r"^\s*(?:public\s+|private\s+|protected\s+)?class\s+(\w+)", "class"),
            (r"^\s*(?:public|private|protected).*\s(\w+)\s*\([^;]*\)\s*\{", "method"),
        ],
        "C#": [
            (r"^\s*(?:public\s+|private\s+|internal\s+)?class\s+(\w+)", "class"),
            (r"^\s*.*\s(\w+)\s*\([^;]*\)\s*\{", "method"),
        ],
    }
    out: list[Symbol] = []
    for i, line in enumerate(text.splitlines(), 1):
        for pat, kind in patterns.get(language, []):
            m = re.search(pat, line)
            if m:
                out.append(Symbol(m.group(1), kind, i))
                break
    return out


def _imports(text: str, language: str) -> list[str]:
    patterns = {
        "Python": [r"^\s*import\s+([\w.]+)", r"^\s*from\s+([\w.]+)\s+import"],
        "JavaScript": [r"from\s+['\"]([^'\"]+)", r"require\(['\"]([^'\"]+)['\"]\)"],
        "TypeScript": [r"from\s+['\"]([^'\"]+)", r"require\(['\"]([^'\"]+)['\"]\)"],
        "Go": [r'"([^"\n]+)"'],
        "Rust": [r"^\s*use\s+([\w:]+)"],
        "Java": [r"^\s*import\s+([\w.]+)"],
        "C#": [r"^\s*using\s+([\w.]+)"],
    }
    values: list[str] = []
    for line in text.splitlines():
        for pat in patterns.get(language, []):
            m = re.search(pat, line)
            if m and m.group(1) not in values:
                values.append(m.group(1))
    return values[:50]


def iter_source_files(root: Path) -> Iterable[Path]:
    for base, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
        for name in sorted(files):
            p = Path(base) / name
            if name in SKIP_NAMES or p.suffix.lower() not in LANGUAGES:
                continue
            yield p


def scan(root: str | Path) -> RepositoryIndex:
    import datetime

    base = Path(root).resolve()
    files: list[FileNode] = []
    for path in iter_source_files(base):
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        lang = LANGUAGES[path.suffix.lower()]
        rel = path.relative_to(base).as_posix()
        files.append(
            FileNode(
                rel,
                lang,
                hashlib.sha256(text.encode()).hexdigest(),
                len(text.splitlines()),
                _symbols(text, lang),
                _imports(text, lang),
            )
        )
    return RepositoryIndex(
        str(base), datetime.datetime.now(datetime.timezone.utc).isoformat(), files
    )


def render_markdown(index: RepositoryIndex, language: str = "en") -> str:
    labels = LABELS.get(language, LABELS["en"])
    by_lang: dict[str, int] = {}
    for f in index.files:
        by_lang[f.language] = by_lang.get(f.language, 0) + 1
    lines = [
        f"# {labels['title']}",
        "",
        labels["summary"],
        "",
        f"- {labels['files']}: {len(index.files)}",
        f"- {labels['symbols']}: {sum(len(f.symbols) for f in index.files)}",
        f"- {labels['imports']}: {sum(len(f.imports) for f in index.files)}",
        "",
        "## Languages",
        "",
    ]
    lines += [f"- **{k}**: {v}" for k, v in sorted(by_lang.items())]
    lines += ["", "## File map", ""]
    for f in index.files:
        lines.append(f"### `{f.path}`")
        lines.append(f"- {f.language} · {f.lines} lines · `{f.sha256[:12]}`")
        if f.symbols:
            lines.append(
                "- Symbols: " + ", ".join(f"`{s.name}` ({s.kind}:{s.line})" for s in f.symbols)
            )
        if f.imports:
            lines.append("- Imports: " + ", ".join(f"`{x}`" for x in f.imports))
    return "\n".join(lines) + "\n"


def diff(old: RepositoryIndex, new: RepositoryIndex) -> dict:
    a, b = {f.path: f for f in old.files}, {f.path: f for f in new.files}
    return {
        "added": sorted(set(b) - set(a)),
        "removed": sorted(set(a) - set(b)),
        "changed": sorted(p for p in set(a) & set(b) if a[p].sha256 != b[p].sha256),
    }
