# generator.py

from PIL import Image, ImageDraw
import os

# Define color schemes for various pride flags
PRIDE_FLAGS = {
    "trans": ["#55CDFC", "#F7A8B8", "#FFFFFF", "#F7A8B8", "#55CDFC"],
    "gay": ["#FF0018", "#FFA52C", "#FFFF41", "#008018", "#0000F9", "#86007D"],
    "bi": ["#D60270", "#D60270", "#9B4F96", "#0038A8", "#0038A8"],
    "nonbinary": ["#FFF430", "#FFFFFF", "#9C59D1", "#000000"],
    # Add more flags here as needed
}

def generate_bitmap_flag(flag_name, colors, sizes, output_dir):
    """Generate bitmap pride flags at specified sizes."""
    for size in sizes:
        width, height = int(size), int(size) // 2
        img = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(img)

        # Draw stripes
        stripe_height = height // len(colors)
        for i, color in enumerate(colors):
            draw.rectangle(
                [(0, i * stripe_height), (width, (i + 1) * stripe_height)],
                fill=color,
            )

        # Save image
        output_path = os.path.join(output_dir, f"{flag_name}_{size}.png")
        img.save(output_path)
        print(f"Saved bitmap flag: {output_path}")


def generate_vector_flag(flag_name, colors, output_dir):
    """Generate a vector pride flag as an SVG."""
    height = 100  # Fixed height for simplicity
    stripe_height = height / len(colors)
    width = height * 2  # Fixed aspect ratio 2:1

    svg_lines = [
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
        '<svg xmlns="http://www.w3.org/2000/svg" version="1.1"',
        f'     width="{width}" height="{height}">',
    ]

    for i, color in enumerate(colors):
        y = i * stripe_height
        svg_lines.append(
            f'    <rect x="0" y="{y}" width="{width}" height="{stripe_height}" fill="{color}" />'
        )

    svg_lines.append("</svg>")
    output_path = os.path.join(output_dir, f"{flag_name}.svg")
    with open(output_path, "w", encoding="utf-8") as svg_file:
        svg_file.write("\n".join(svg_lines))
    print(f"Saved vector flag: {output_path}")


def generate_flags(flags, output_format, sizes, output_dir):
    """
    Generate pride flags based on input arguments.
    Args:
        flags (list): List of pride flags to generate (e.g., ["trans", "gay"]).
        output_format (str): Output format, either "bitmap" or "vector".
        sizes (list): List of sizes for bitmap or "svg" for vector.
        output_dir (str): Directory to save the generated files.
    """
    for flag_name in flags:
        if flag_name not in PRIDE_FLAGS:
            print(f"Unknown flag: {flag_name}. Skipping...")
            continue

        colors = PRIDE_FLAGS[flag_name]

        if output_format == "bitmap":
            bitmap_sizes = [s for s in sizes if s.isdigit()]
            generate_bitmap_flag(flag_name, colors, bitmap_sizes, output_dir)

        elif output_format == "vector" and "svg" in sizes:
            generate_vector_flag(flag_name, colors, output_dir)


if __name__ == "__main__":
    print("This module is intended to be imported, not run directly.")
