import argparse
import sys
from pathlib import Path

from termites.config.config import load_default_model, load_weave_project, set_weave_project
from termites.generate import generate_response
from termites.cache import setup_cache_db, get_cached_response, get_cached_response_weave, cache_response
from termites.util import write_output


def run(prompt: str, model: str, output: Path | None = None, use_cache: bool = True, use_weave: bool = False) -> None:
    response = generate_response(prompt, model, use_cache=use_cache, use_weave=use_weave)
    write_output(response, output)

def main(): 
    # Ensure cache database exists
    setup_cache_db()
    default_model = load_default_model()
    
    parser = argparse.ArgumentParser(
        description="Termites - CLI tool for generating text using LLMs"
    )
    parser.add_argument(
        "prompt",
        nargs="+",
        help="The prompt to send to the LLM"
    )
    parser.add_argument(
        "--model",
        "-m",
        default=default_model,
        help=f"The LLM model to use (default: {default_model})"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Output file path (optional)"
    )
    parser.add_argument(
        "--no-cache",
        "-n",
        action="store_true",
        help="Disable cache and force new LLM call"
    )
    parser.add_argument(
        "--weave_project",
        "-w",
        type=str,
        help="Weave project name"
    )
    
    args = parser.parse_args()
    prompt = " ".join(args.prompt)

    weave_project = args.weave_project
    if weave_project:
        set_weave_project(weave_project)
    else:
        weave_project = load_weave_project()

    if weave_project:
        try:
            import weave
            weave.init(weave_project)
        except ImportError:
            print("Weave is not installed. Please install it to use this feature.", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error initializing Weave project: {e}", file=sys.stderr)
            sys.exit(1)
    
    run(prompt, args.model, args.output, not args.no_cache, weave_project is not None)

if __name__ == "__main__":
    main()
