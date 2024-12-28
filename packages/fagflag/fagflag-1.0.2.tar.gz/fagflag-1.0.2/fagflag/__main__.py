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
        "--sizes",
        type=str,
        required=True,
        help="Comma-separated list of sizes (e.g., 128,256,512 for bitmap or svg for vector).",
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
        default=None,
        help="Width of the generated flags. Overrides size in bitmap mode.",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=None,
        help="Height of the generated flags. Overrides size in bitmap mode.",
    )

    args = parser.parse_args()

    if args.create:
        # Parse arguments
        flags = args.flags.split(",")
        sizes = args.sizes.split(",")

        # Ensure output directory exists
        os.makedirs(args.output, exist_ok=True)

        # Generate the flags with the additional overlay, width, and height arguments
        generate_flags(
            flags,
            args.format,
            sizes,
            args.output,
            overlay_path=args.overlay,
            width=args.width,
            height=args.height
        )

if __name__ == "__main__":
    main()
