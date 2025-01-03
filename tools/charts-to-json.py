# !/usr/bin/env python3

import json
import os.path
import sys
from argparse import ArgumentParser
from pathlib import Path

from lxml import etree
from rich.console import Console

__version__ = "1.0"
__description__ = "Parse emoji-list.html, full-emoji-modifiers.html, emoji-variants.html of Unicode® Emoji Charts v16.0, generate JSON files with data in it from HTML files"

DOWNLOAD_DIR = Path("download")
PAGE_DIR = DOWNLOAD_DIR.joinpath("pages")


def proc_emoji_list(console: Console):
    num = 0
    status_prefix = "[bold blue]<emoji-list>[/]"
    with console.status(status_prefix) as status:
        with PAGE_DIR.joinpath("emoji-list.jsonl").open("w") as f:
            html = PAGE_DIR.joinpath("emoji-list.html").read_text()
            dom = etree.fromstring(html, etree.HTMLParser())

            for ele_bighead in dom.xpath("//th[@class='bighead']"):
                bighead = ele_bighead.xpath("./a[1]//text()")[0]
                mediumhead = ""
                for ele_next in ele_bighead.xpath("../following-sibling::tr"):
                    if ele_next.xpath("./th[@class='bighead'][1]"):
                        break
                    ele_mediumhead_ls = ele_next.xpath("./th[@class='mediumhead'][1]")
                    if ele_mediumhead_ls:
                        ele_mediumhead = ele_mediumhead_ls[0]
                        mediumhead = ele_mediumhead.xpath("./a[1]//text()")[0]

                    ele_code_ls = ele_next.xpath("./td[@class='code'][1]")
                    if not ele_code_ls:
                        continue
                    ele_code = ele_code_ls[0]

                    code = ele_code.xpath("./a[1]//text()")[0]  # eg: "U+1F600", "U+1F1EC U+1F1E9"
                    num = int(ele_next.xpath("./td[@class='rchars'][1]//text()")[0])
                    names = ele_next.xpath("./td[@class='name'][position()<3]//text()")
                    shortname = names[0]
                    keywords = "".join(names[1:])
                    img = ele_next.xpath(".//img[1]/@src")[0]

                    status.update(f"{status_prefix}\t[{num:,}]\t{bighead} / {mediumhead}")

                    data = {
                        "num": num,
                        "bighead": bighead,
                        "mediumhead": mediumhead,
                        "code": code,
                        "shortname": shortname,
                        "keywords": keywords,
                        "img": img,
                    }
                    print(json.dumps(data), file=f)
    if num:
        console.print(f"✔️ {status_prefix}\t{num:,}")
    else:
        console.print(f"❌{status_prefix}\t{num:,}")


def proc_full_emoji_modifiers(console: Console):
    num = 0
    status_prefix = "[bold blue]<full-emoji-modifiers>[/]"
    with console.status(status_prefix) as status:
        with PAGE_DIR.joinpath("full-emoji-modifiers.jsonl").open("w") as f:
            html = PAGE_DIR.joinpath("full-emoji-modifiers.html").read_text()
            dom = etree.fromstring(html, etree.HTMLParser())

            for ele_bighead in dom.xpath("//th[@class='bighead']"):
                bighead = ele_bighead.xpath("./a[1]//text()")[0]
                mediumhead = ""
                for ele_next in ele_bighead.xpath("../following-sibling::tr"):
                    if ele_next.xpath("./th[@class='bighead'][1]"):
                        break
                    ele_mediumhead_ls = ele_next.xpath("./th[@class='mediumhead'][1]")
                    if ele_mediumhead_ls:
                        ele_mediumhead = ele_mediumhead_ls[0]
                        mediumhead = ele_mediumhead.xpath("./a[1]//text()")[0]

                    if elements := ele_next.xpath("./td[@class='code'][1]"):
                        ele_code = elements[0]
                    else:
                        continue

                    code = ele_code.xpath("./a[1]//text()")[0]  # eg: "U+1F600", "U+1F1EC U+1F1E9"
                    num = int(ele_next.xpath("./td[@class='rchars'][1]//text()")[0])
                    shortname = ele_next.xpath("./td[@class='name'][1]//text()")[0]
                    img = ele_next.xpath(".//img[1]/@src")[0]

                    status.update(f"{status_prefix}\t[{num:,}]\t{bighead} / {mediumhead}")

                    data = {
                        "num": num,
                        "bighead": bighead,
                        "mediumhead": mediumhead,
                        "code": code,
                        "shortname": shortname,
                        "img": img,
                    }
                    print(json.dumps(data), file=f)
    if num:
        console.print(f"✔️ {status_prefix}\t{num:,}")
    else:
        console.print(f"❌{status_prefix}\t{num:,}")


def proc_emoji_variants(console: Console):
    num = 0
    status_prefix = "[bold blue]<emoji-variants>[/]"
    with console.status(status_prefix) as status:
        with PAGE_DIR.joinpath("emoji-variants.jsonl").open("w") as f:
            html = PAGE_DIR.joinpath("emoji-variants.html").read_text()
            dom = etree.fromstring(html, etree.HTMLParser())

            for ele in dom.xpath("//td[contains(@class, 'code')]"):
                num += 1
                code_0 = ele.xpath("./a[1]//text()")[0]

                status.update(f"{status_prefix}\t{num:,}\t{code_0}")

                code_1 = f"{code_0} FE0E"
                code_2 = f"{code_0} FE0F"

                img_0 = img_1 = None
                andr_0, andr_1 = ele.xpath("./following-sibling::td[contains(@class, 'andr')][position()<3]")
                if values := andr_0.xpath("./img[1]/@src"):
                    img_0 = values[0]
                if values := andr_1.xpath("./img[1]/@src"):
                    img_1 = values[0]
                date_ = ele.xpath("./following-sibling::td[3]//text()")[0]
                shortname = ele.xpath("./following-sibling::td[4]//text()")[0]

                data_1 = {"code": code_1, "date": date_, "shortname": shortname, "variation": "text", "img": img_0}
                print(json.dumps(data_1), file=f)
                data_2 = {"code": code_2, "date": date_, "shortname": shortname, "variation": "emoji", "img": img_1}
                print(json.dumps(data_2), file=f)
    if num:
        console.print(f"✔️ {status_prefix}\t{num:,}")
    else:
        console.print(f"❌{status_prefix}\t{num:,}")


PAGE_CHOICES = {"emoji-list", "full-emoji-modifiers", "emoji-variants"}


def setup_args():
    _, file_tail = os.path.split(sys.argv[0])
    file_root, _ = os.path.splitext(file_tail)
    parser = ArgumentParser(
        f"{sys.executable} -m {__package__}" if file_root == "__main__" else __package__, description=__description__
    )
    parser.add_argument("--version", "-V", action="version", version=__version__)
    parser.add_argument(
        "pages",
        nargs="*",
        type=str,
        choices=PAGE_CHOICES,
        help="Unicode® Emoji Charts v16.0 page to be parsed",
    )
    return parser.parse_args()


def main():
    args = setup_args()
    if not args.pages:
        args.pages = PAGE_CHOICES
    console = Console()
    try:
        if "emoji-list" in args.pages:
            proc_emoji_list(console)
        if "full-emoji-modifiers" in args.pages:
            proc_full_emoji_modifiers(console)
        if "emoji-variants" in args.pages:
            proc_emoji_variants(console)
    except KeyboardInterrupt:
        exit(1)
    except Exception:
        console.print_exception(show_locals=True)
        exit(2)


if __name__ == "__main__":
    main()
