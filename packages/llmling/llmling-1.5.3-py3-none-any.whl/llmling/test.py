# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "reposcape"
# ]
# ///

from __future__ import annotations

import importlib

import reposcape


def get_repo_overview(module: str) -> str:
    """Get a structured overview over a codebase.

    Args:
        module: Module name

    Returns:
        Extracted content as string

    Raises:
        ValueError: If the URL is invalid or content extraction fails
    """
    mod_obj = importlib.import_module(module)
    return reposcape.get_repo_overview(mod_obj)


if __name__ == "__main__":
    content = get_repo_overview("llmling")
    print(content)
