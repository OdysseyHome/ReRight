# ReRight.md 📝

Turning Markdown chaos into structured order.

**⚠️ STATUS: WORK IN PROGRESS / EDUCATIONAL**
This project is a self-learning Python CLI tool. It is currently in a pre-release state. DO NOT USE on production data!

ReRight.md is a high-performance CLI tool designed to refactor and normalize large Markdown note repositories (Obsidian, Joplin, Logseq). It treats your vault like a codebase, allowing for structural "migrations" and schema enforcement that maintain link integrity across thousands of files.

## Key Features

* **Re-Name:** Sanitize file and folder names (e.g., kebab-case conversion) while preserving internal [[wikilinks]].
* **Re-Format:** Apply Pydantic-style schemas to YAML frontmatter to ensure metadata consistency.
* **Re-Assure:** Every operation is a Dry-Run by default. Preview every file move and content edit before committing to disk.
* **Re-Engineered:** Built with Python and uv to handle batch operations at speeds that outperform GUI-based plugins.

## Example use case

*Before*

PATH: "My Obisidan Vault/Meeting_Notes/Meeting Notes (2023).md"
LINK: [[Meeting Notes (2023)]]

*After*

PATH: "documents/my-notes/2023-meeting-notes.md" (better for cross-platform compatibility)
LINK: [[2023-meeting-notes]] (Auto-updated so note vaults don't break)

## Quickstart

This project uses uv for lightning-fast dependency management and project isolation.

## 1. Installation

Clone the repo and sync the environment:

```powershell
git clone [https://github.com/OdysseyHome/reright-md](https://github.com/OdysseyHome/reright-md)
cd reright-md
uv sync --all-extras
```

## 2. Development & Testing

uv handles your virtual environment automatically. To run the quality suite:

```powershell
# Run tests
uv run pytest

# Format and Lint
uv run black .
uv run ruff check . 
```

## 3. Usage

The tool is accessible via the reright command. By default, it runs in Dry-Run mode.

```powershell
# Preview changes to a vault
uv run reright "C:\Path\To\Vault"

# Apply changes to disk (Live Mode)
uv run reright "C:\Path\To\Vault" --apply
```

## Why Python for Note Refactoring?

While Obsidian community plugins exist, they operate within the Electron/JavaScript overhead of the app. ReRight.md is built in Python because:

* **Data Integrity:** Better handling of complex regex and YAML parsing via robust libraries like ruamel.yaml.
* **Speed:** Standalone batch processing is significantly faster for vaults with 10,000+ notes.
* **Decoupling:** You shouldn't have to open your note-taking app just to fix your note-taking app's structure.

## License

This project is licensed under the MIT License — see the LICENSE file for details.