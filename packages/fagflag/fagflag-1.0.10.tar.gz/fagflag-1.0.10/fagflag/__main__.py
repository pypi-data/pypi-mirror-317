# __main__.py

from fagflag.generator import generate_flags
import argparse
import os

def main():
    parser = argparse.ArgumentParser(
        description="Generate pride flags as bitmap or vector images."
    )
    parser.add_argument(
        "--create",
        action="store_true",
        help="Create pride flags.",
    )
    parser.add_argument(
        "--flags",
        type=str,
        required=True,
        help="Comma-separated list of flags to generate (e.g., trans,gay,bi).",
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["bitmap", "vector"],
        required=True,
        help="Output format (bitmap or vector).",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output directory to save the generated flags.",
    )
    parser.add_argument(
        "--overlay",
        type=str,
        help="Path to a PNG image to overlay on the generated bitmap flags (optional).",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=512,  # Default width set to 512
        help="Width of the generated flags. Overrides size in bitmap mode.",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=512,  # Default height set to 512
        help="Height of the generated flags. Overrides size in bitmap mode.",
    )

    args = parser.parse_args()

    if args.create:
        # Parse arguments
        flags = args.flags.split(",")
        overlay_path = args.overlay

        # Ensure output directory exists
        os.makedirs(args.output, exist_ok=True)

        # Generate the flags with the updated arguments
        generate_flags(
            flags,
            args.format,
            args.output,
            overlay_path=overlay_path,
            width=args.width,
            height=args.height
        )

if __name__ == "__main__":
    main()
