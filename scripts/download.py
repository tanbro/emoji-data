# !usr/bin/env python

import asyncio
from pathlib import Path
from urllib.parse import unquote

import httpx
from rich.console import Console
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

URLS = (
    "https://www.unicode.org/Public/UCD/latest/ucd/emoji/emoji-data.txt",
    "https://www.unicode.org/Public/UCD/latest/ucd/emoji/emoji-variation-sequences.txt",
    "https://www.unicode.org/Public/emoji/latest/emoji-sequences.txt",
    "https://www.unicode.org/Public/emoji/latest/emoji-zwj-sequences.txt",
    "https://www.unicode.org/Public/emoji/latest/emoji-test.txt",
)

OUTPUT_DIR = Path(__file__).parent.parent / "src" / "emoji_data" / "data"


def get_filename_from_response(response: httpx.Response, url: str) -> str:
    """从 HTTP 响应头或 URL 中提取文件名"""
    # 尝试从 Content-Disposition 头获取文件名
    content_disposition = response.headers.get("content-disposition", "")
    if content_disposition:
        for part in content_disposition.split(";"):
            part = part.strip()
            if part.startswith("filename="):
                filename = part.split("=", 1)[1].strip("\"'")
                return unquote(filename)

    # 如果没有 Content-Disposition，从 URL 中提取
    return unquote(url.rsplit("/", 1)[-1])


async def download(
    client: httpx.AsyncClient,
    url: str,
    progress: Progress,
    task_id: TaskID,
) -> None:
    """下载单个文件"""
    try:
        async with client.stream("GET", url, follow_redirects=True) as response:
            response.raise_for_status()

            filename = get_filename_from_response(response, url)
            output_path = OUTPUT_DIR / filename
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

            total = int(response.headers.get("content-length", 0))
            progress.update(task_id, total=total, filename=filename)

            with output_path.open("wb") as f:
                async for chunk in response.aiter_bytes():
                    f.write(chunk)
                    progress.update(task_id, advance=len(chunk))

    except httpx.HTTPStatusError as e:
        progress.console.print(f"[red]下载失败 {url}: {e}[/red]")
    except Exception as e:
        progress.console.print(f"[red]错误 {url}: {e}[/red]")


async def main():
    """并发下载所有文件"""
    console = Console()

    progress = Progress(
        TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
        BarColumn(bar_width=None),
        "[progress.percentage]{task.percentage:>3.0f}%",
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        console=console,
    )

    timeout = httpx.Timeout(60.0, connect=10.0)
    limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)

    async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
        with progress:
            tasks = [progress.add_task(url, filename=url) for url in URLS]
            await asyncio.gather(*[download(client, url, progress, task_id) for url, task_id in zip(URLS, tasks)])


if __name__ == "__main__":
    asyncio.run(main())
