"""Prompt loading utilities."""
from pathlib import Path

_PROMPT_DIR = Path(__file__).parent


def load_prompt(name: str) -> str:
    """Load a prompt file by name (without .md extension)."""
    file_path = _PROMPT_DIR / f"{name}.md"
    if not file_path.exists():
        return ""
    return file_path.read_text(encoding="utf-8")


def render_prompt(name: str, variables: dict[str, str]) -> str:
    """Load and render a prompt template with variable substitution."""
    template = load_prompt(name)
    for key, value in variables.items():
        template = template.replace("{{" + key + "}}", str(value))
    return template


def list_prompts() -> list[str]:
    """List all available prompt names."""
    return [f.stem for f in _PROMPT_DIR.glob("*.md") if f.name != "__init__.py"]
