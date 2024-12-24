from pathlib import Path
import sys

def write_to_file(content: str, output_file: Path) -> None:
    """Write content to specified file."""
    try:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(content)
        print(f"Output written to: {output_file}")
    except Exception as e:
        print(f"Error writing to file: {e}", file=sys.stderr)
        sys.exit(1)

def write_output(response: str, output: Path | None = None) -> None:
    if output:
        write_to_file(response, output)
    else:
        print(response)
