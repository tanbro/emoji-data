# !/usr/bin/env python3
from __future__ import annotations

import json
import os.path
import sys
from argparse import ArgumentParser
from io import StringIO
from pathlib import Path, PurePath
from typing import TYPE_CHECKING, Any, Dict, Iterator, Union

from rich.console import Console
from rich.progress import Progress

if TYPE_CHECKING:
    from _typeshed import StrPath

__version__ = "1.0"
__description__ = "Parse emoji-list.html, full-emoji-modifiers.html, emoji-variants.html of Unicode® Emoji Charts v16.0, generate JSON files with data in it from HTML files"

DOWNLOAD_DIR = Path("download")
PAGE_DIR = DOWNLOAD_DIR.joinpath("pages")
CLDR_DIR = DOWNLOAD_DIR.joinpath("cldr-46.1.0-json-full")


def setup_args():
    _, file_tail = os.path.split(sys.argv[0])
    file_root, _ = os.path.splitext(file_tail)
    parser = ArgumentParser(
        f"{sys.executable} -m {__package__}" if file_root == "__main__" else __package__, description=__description__
    )
    parser.add_argument("--version", "-V", action="version", version=__version__)
    parser.add_argument("languages", nargs="*", type=str)
    return parser.parse_args()


def make(lang: str):
    emoji_list = list(iter_json_lines(PAGE_DIR.joinpath("emoji-list.jsonl")))
    full_emoji_modifiers = list(iter_json_lines(PAGE_DIR.joinpath("full-emoji-modifiers.jsonl")))
    emoji_variants = list(iter_json_lines(PAGE_DIR.joinpath("emoji-variants.jsonl")))

    annotations = {}
    if lang:
        with CLDR_DIR.joinpath("cldr-annotations-full", "annotations", lang, "annotations.json").open() as fp:
            data = json.load(fp)
            annotations_dict = data["annotations"]["annotations"]
            annotations.update(annotations_dict)
        with CLDR_DIR.joinpath("cldr-annotations-derived-full", "annotationsDerived", lang, "annotations.json").open() as fp:
            data = json.load(fp)
            annotations_dict = data["annotationsDerived"]["annotations"]
            annotations.update(annotations_dict)

    keywords_dict = {}
    with DOWNLOAD_DIR.joinpath(f"{lang}.jsonl").open("w") as f:
        for d0 in emoji_list:
            code = d0["code"]
            es = code_to_str(code)
            shortname = d0["shortname"]
            keywords = [s.strip() for s in d0["keywords"].split("|")]
            keywords_dict[shortname] = keywords
            dd = {
                "string": es,
                "code": code,
                "category": [d0["bighead"], d0["mediumhead"]],
                "shortname": d0["shortname"],
                "keywords": keywords,
            }
            if anno := annotations.get(es):
                dd.update({"shortname": anno["tts"], "keywords": anno["default"]})
            print(json.dumps(dd, ensure_ascii=False), file=f)

        for d0 in full_emoji_modifiers:
            code = d0["code"]
            es = code_to_str(code)
            shortname = d0["shortname"]
            basename = "".rsplit(":", 1)[0]
            keywords = keywords_dict.get(basename, [])
            dd = {
                "string": es,
                "code": code,
                "category": [d0["bighead"], d0["mediumhead"]],
                "shortname": shortname,
                "keywords": keywords,
            }
            if anno := annotations.get(es):
                dd.update({"shortname": anno["tts"], "keywords": anno["default"]})
            print(json.dumps(dd, ensure_ascii=False), file=f)

        for d0 in emoji_variants:
            code = d0["code"]
            es = code_to_str(code)
            shortname = d0["shortname"]
            basename = "".rsplit(":", 1)[0]
            keywords = keywords_dict.get(basename)
            dd = {
                "string": es,
                "code": code,
                "category": [],
                "shortname": shortname,
                "keywords": [],
            }
            if anno := annotations.get(es):
                dd.update({"shortname": anno["tts"], "keywords": anno["default"]})
            print(json.dumps(dd, ensure_ascii=False), file=f)


def code_to_str(s):
    parts = s.split()
    for i in range(len(parts)):
        part = parts[i]
        if part.startswith("U+"):
            parts[i] = part[2:]
    return "".join(chr(int(s, 16)) for s in parts)


def iter_json_lines(file: Union[StringIO, StrPath]) -> Iterator[Dict[str, Any]]:
    if isinstance(file, (str, bytes, PurePath)):
        with Path(file).open() as fp:
            for line in fp:
                yield json.loads(line)
    else:
        assert isinstance(file, StringIO)
        for line in file:
            yield json.loads(line)


def main():
    args = setup_args()
    console = Console()
    try:
        with console.status("Loading CLDR data..."):
            with CLDR_DIR.joinpath("cldr-core", "availableLocales.json").open() as fp:
                data = json.load(fp)
                available_locales = data["availableLocales"]["full"]
            with CLDR_DIR.joinpath("cldr-core", "coverageLevels.json").open() as fp:
                data = json.load(fp)
                coverage_levels = data["coverageLevels"]
            modern_locales = [m for m in available_locales if coverage_levels.get(m) == "modern"]
        if args.languages:
            for lang in args.languages:
                if lang not in modern_locales:
                    console.print(f"[red]Language {lang} is not available or not coverage well in CLDR[/red]")
                    sys.exit(3)
        else:
            args.languages = modern_locales

        with Progress(console=console) as progress:
            progress_task = progress.add_task("", total=len(args.languages))
            for lang in args.languages:
                progress.update(progress_task, advance=1, description=f"[bold cyan]{lang:<10}[/]")
                make(lang)
            progress.update(progress_task, description="[bold green]completed [/]")
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception:
        console.print_exception()
        sys.exit(-1)


if __name__ == "__main__":
    main()
