from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from .core import diff, render_markdown, scan

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="repolens", description="Local-first repository intelligence")
    p.add_argument("command", choices=["scan", "query", "diff"], help="operation")
    p.add_argument("path", nargs="?", default=".")
    p.add_argument("--out", type=Path)
    p.add_argument("--lang", default="en", choices=["en", "ar", "es", "fr", "zh"])
    p.add_argument("--format", choices=["json", "markdown"], default="markdown")
    p.add_argument("--query")
    p.add_argument("--against", type=Path, help="previous RepoLens JSON snapshot")
    return p

def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        current = scan(args.path)
        if args.command == "scan":
            payload = current.to_dict() if args.format == "json" else render_markdown(current, args.lang)
        elif args.command == "query":
            if not args.query: raise ValueError("query requires --query")
            payload = json.dumps([{"path": f.path, "language": f.language, "symbols": [s.name for s in f.symbols]} for f in current.find(args.query)], ensure_ascii=False, indent=2)
        else:
            if not args.against: raise ValueError("diff requires --against SNAPSHOT.json")
            old_data = json.loads(args.against.read_text(encoding="utf-8"))
            from .core import FileNode, RepositoryIndex, Symbol
            old = RepositoryIndex(old_data["root"], old_data.get("generated_at", ""), [FileNode(f["path"], f["language"], f["sha256"], f["lines"], [Symbol(**s) for s in f.get("symbols", [])], f.get("imports", [])) for f in old_data["files"]])
            payload = json.dumps(diff(old, current), ensure_ascii=False, indent=2)
        if isinstance(payload, dict): payload = json.dumps(payload, ensure_ascii=False, indent=2)
        if args.out: args.out.write_text(payload, encoding="utf-8")
        else: print(payload, end="" if payload.endswith("\n") else "\n")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"repolens: error: {exc}", file=sys.stderr); return 2

if __name__ == "__main__": raise SystemExit(main())
