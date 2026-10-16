"""Refresh the experiment table in README.md from root-level experiment folders."""
from pathlib import Path
import re
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
START = "<!-- EXPERIMENTS:START -->"
END = "<!-- EXPERIMENTS:END -->"


def sort_key(path: Path) -> tuple[int, str]:
    match = re.search(r"\d+", path.name)
    return (int(match.group()) if match else 10**9, path.name.casefold())


def experiment_table() -> str:
    folders = [
        path for path in ROOT.iterdir()
        if path.is_dir() and path.name.casefold().startswith("experiment")
    ]
    folders.sort(key=sort_key)

    if not folders:
        return "_No experiment folders have been added yet._"

    lines = [
        "| Experiment | Source file | Folder |",
        "|---|---|---|",
    ]
    for folder in folders:
        folder_url = quote(folder.name, safe="")
        folder_link = f"./{folder_url}/"
        index_file = folder / "index.html"
        source_link = f"[Open `index.html`](./{folder_url}/index.html)" if index_file.is_file() else "_Open folder to view files_"
        lines.append(f"| **{folder.name}** | {source_link} | [Browse ↗]({folder_link}) |")
    return "\n".join(lines)


def main() -> None:
    content = README.read_text(encoding="utf-8")
    if content.count(START) != 1 or content.count(END) != 1:
        raise SystemExit("README markers are missing or duplicated; experiment index was not changed.")

    before, after_start = content.split(START, 1)
    _, after_end = after_start.split(END, 1)
    updated = f"{before}{START}\n{experiment_table()}\n{END}{after_end}"

    if updated != content:
        README.write_text(updated, encoding="utf-8")
        print("Experiment index refreshed.")
    else:
        print("Experiment index is already up to date.")


if __name__ == "__main__":
    main()
