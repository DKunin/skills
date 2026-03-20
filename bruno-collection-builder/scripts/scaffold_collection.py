#!/usr/bin/env python3

import argparse
import json
import re
import sys
from pathlib import Path


DEFAULT_BASE_URL = "https://api.example.com"


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value.strip()).strip("-").lower()
    return slug or "item"


def sanitize_display_name(value: str, fallback: str) -> str:
    cleaned = " ".join(value.split())
    return cleaned or fallback


def yaml_string(value: str) -> str:
    return json.dumps(value)


def parse_env(raw: str) -> tuple[str, str]:
    name, separator, base_url = raw.partition("=")
    name = sanitize_display_name(name, "")
    if not name:
        raise ValueError(f"Invalid environment value: {raw!r}")
    return name, (base_url.strip() if separator else "") or DEFAULT_BASE_URL


def ensure_target_directory(path: Path) -> None:
    if path.exists():
        if not path.is_dir():
            raise ValueError(f"Target path exists and is not a directory: {path}")
        if any(path.iterdir()):
            raise ValueError(f"Target directory is not empty: {path}")
        return
    path.mkdir(parents=True, exist_ok=False)


def write_file(path: Path, content: str, created: list[Path]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    created.append(path)


def render_yaml_root(name: str) -> str:
    return (
        'opencollection: "1.0.0"\n'
        "info:\n"
        f"  name: {yaml_string(name)}\n"
        "\n"
        "extensions:\n"
        "  bruno:\n"
        "    ignore:\n"
        "      - node_modules\n"
        "      - .git\n"
    )


def render_bru_root_json(name: str) -> str:
    payload = {
        "version": "1",
        "name": name,
        "type": "collection",
        "ignore": ["node_modules", ".git"],
    }
    return json.dumps(payload, indent=2) + "\n"


def render_bru_collection(name: str) -> str:
    return f"docs {{\n  # {name}\n}}\n"


def render_yaml_folder(name: str, seq: int) -> str:
    return (
        "info:\n"
        f"  name: {yaml_string(name)}\n"
        f"  seq: {seq}\n"
    )


def render_bru_folder(name: str, seq: int) -> str:
    return f"meta {{\n  name: {name}\n  seq: {seq}\n}}\n"


def render_yaml_env(name: str, base_url: str) -> str:
    return (
        f"name: {yaml_string(name)}\n"
        "variables:\n"
        "  - name: baseUrl\n"
        f"    value: {yaml_string(base_url)}\n"
    )


def render_bru_env(base_url: str) -> str:
    return f"vars {{\n  baseUrl: {base_url}\n}}\n"


def create_folders(root: Path, collection_format: str, folder_specs: list[str], created: list[Path]) -> None:
    seq_by_parent: dict[Path, int] = {}
    for raw in folder_specs:
        parts = [sanitize_display_name(part, "") for part in raw.split("/") if sanitize_display_name(part, "")]
        if not parts:
            raise ValueError(f"Invalid folder value: {raw!r}")

        current_dir = root
        for part in parts:
            current_dir = current_dir / slugify(part)
            current_dir.mkdir(parents=True, exist_ok=True)

            folder_filename = "folder.yml" if collection_format == "yaml" else "folder.bru"
            folder_file = current_dir / folder_filename
            if folder_file.exists():
                continue

            parent_dir = current_dir.parent
            next_seq = seq_by_parent.get(parent_dir, 0) + 1
            seq_by_parent[parent_dir] = next_seq

            if collection_format == "yaml":
                content = render_yaml_folder(part, next_seq)
            else:
                content = render_bru_folder(part, next_seq)
            write_file(folder_file, content, created)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a minimal Bruno collection scaffold in YAML or legacy Bru format."
    )
    parser.add_argument("--name", required=True, help="Collection display name.")
    parser.add_argument("--path", required=True, help="Output directory for the collection.")
    parser.add_argument(
        "--format",
        choices=("yaml", "bru"),
        default="yaml",
        help="Collection format to create. Defaults to yaml.",
    )
    parser.add_argument(
        "--env",
        action="append",
        default=[],
        help="Environment stub to create. Use NAME or NAME=BASE_URL.",
    )
    parser.add_argument(
        "--folder",
        action="append",
        default=[],
        help="Top-level or nested folder path to create, for example 'Users' or 'Admin/Users'.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    collection_name = sanitize_display_name(args.name, "Collection")
    target_dir = Path(args.path).expanduser().resolve()
    created: list[Path] = []

    try:
        ensure_target_directory(target_dir)

        if args.format == "yaml":
            write_file(target_dir / "opencollection.yml", render_yaml_root(collection_name), created)
        else:
            write_file(target_dir / "bruno.json", render_bru_root_json(collection_name), created)
            write_file(target_dir / "collection.bru", render_bru_collection(collection_name), created)

        if args.env:
            env_dir = target_dir / "environments"
            env_dir.mkdir(parents=True, exist_ok=True)
            for raw_env in args.env:
                env_name, base_url = parse_env(raw_env)
                env_filename = slugify(env_name) + (".yml" if args.format == "yaml" else ".bru")
                env_path = env_dir / env_filename
                if args.format == "yaml":
                    content = render_yaml_env(env_name, base_url)
                else:
                    content = render_bru_env(base_url)
                write_file(env_path, content, created)

        if args.folder:
            create_folders(target_dir, args.format, args.folder, created)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Created Bruno {args.format} collection at {target_dir}")
    for path in created:
        print(f"- {path.relative_to(target_dir)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
