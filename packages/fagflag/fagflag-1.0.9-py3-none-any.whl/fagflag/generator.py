from PIL import Image, ImageDraw
import os

PRIDE_FLAGS = {
    "trans": ["#5bcffa", "#f5a9b8", "#FFFFFF", "#f5a9b8", "#5bcffa"],
    "gay": ["#e50203", "#ff8b01", "#feed00", "#008026", "#004dfe", "#750685"],
    "bi": ["#d70071", "#d70071", "#9c4e97", "#0035aa", "#0035aa"],
    "nonbinary": ["#fff430", "#FFFFFF", "#9c59d1", "#292929"],
    "pan": ["#ff1b8d", "#ffd900", "#1bb3ff"],
    "asexual": ["#000000", "#a4a4a5", "#ffffff", "#810081"],
    "genderfluid": ["#ff75a2", "#ffffff", "#be18d6", "#000000", "#333ebd"],
    "lesbian": ["#d62900", "#ff9b55", "#ffffff", "#d462a6", "#a40062"],
    "aromantic": ["#3da542", "#a7d379", "#ffffff", "#a9a9a9", "#000000"],
    "demiboy": ["#7f7f7f", "#c3c3c3", "#99d9ea", "#FFFFFF", "#99d9ea", "#c3c3c3", "#7f7f7f"],
    "demigirl": ["#7f7f7f", "#c3c3c3", "#ffaec9", "#FFFFFF", "#ffaec9", "#c3c3c3", "#7f7f7f"],
    "transfemme": ["#74deff", "#ffe1ed", "#ffb5d6", "#fe8cbf", "#ffb5d6", "#ffe1ed", "#74deff"],
    "transmasc": ["#ff8bbf", "#cdf5ff", "#9aedff", "#76e0ff", "#9aedff", "#cdf5ff", "#ff8bbf"],
    "mlm": ["#018e71", "#21cfac", "#99e9c2", "#ffffff", "#7cafe3", "#4f47cd", "#3a1379"],
    # Add more flags here as needed
}


def generate_bitmap_flag(flag_name, colors, width, height, output_dir, overlay_path=None):
    """Generate bitmap pride flags with custom width and height, with optional overlay."""
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    # Draw stripes
    stripe_height = height // len(colors)
    for i, color in enumerate(colors):
        draw.rectangle(
            [(0, i * stripe_height), (width, (i + 1) * stripe_height)],
            fill=color,
        )

    # Overlay PNG if provided
    if overlay_path:
        overlay = Image.open(overlay_path).convert("RGBA")

        # Resize the overlay to fit within the flag while maintaining its aspect ratio
        overlay_width, overlay_height = overlay.size
        aspect_ratio = overlay_width / overlay_height

        # Calculate the new size of the overlay while maintaining its aspect ratio
        if overlay_width > overlay_height:
            new_width = int(width * 0.8)  # Use 80% of the flag's width
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = int(height * 0.8)  # Use 80% of the flag's height
            new_width = int(new_height * aspect_ratio)

        overlay = overlay.resize((new_width, new_height), Image.LANCZOS)

        # Calculate position to center the overlay
        x_offset = (width - new_width) // 2
        y_offset = (height - new_height) // 2

        # Paste the overlay onto the flag at the center position
        img.paste(overlay, (x_offset, y_offset), overlay)

    # Save image
    output_path = os.path.join(output_dir, f"{flag_name}_{width}x{height}.png")
    img.save(output_path)
    print(f"Saved bitmap flag: {output_path}")


def generate_vector_flag(flag_name, colors, output_dir):
    """Generate a vector pride flag as an SVG."""
    height = 100  # Fixed height for simplicity
    stripe_height = height / len(colors)
    width = height

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


def generate_flags(flags, output_format, output_dir, overlay_path=None, width=None, height=None):
    """
    Generate pride flags based on input arguments.
    Args:
        flags (list): List of pride flags to generate (e.g., ["trans", "gay"]).
        output_format (str): Output format, either "bitmap" or "vector".
        output_dir (str): Directory to save the generated files.
        overlay_path (str, optional): Path to a PNG image to overlay on the flags.
        width (int, optional): Width for bitmap flags.
        height (int, optional): Height for bitmap flags.
    """
    for flag_name in flags:
        if flag_name not in PRIDE_FLAGS:
            print(f"Unknown flag: {flag_name}. Skipping...")
            continue

        colors = PRIDE_FLAGS[flag_name]

        if width is None or height is None:
            print(f"Width and height must be specified for {flag_name}. Skipping...")
            continue

        if output_format == "bitmap":
            generate_bitmap_flag(flag_name, colors, width, height, output_dir, overlay_path)
        elif output_format == "vector":
            generate_vector_flag(flag_name, colors, output_dir)


if __name__ == "__main__":
    print("This module is intended to be imported, not run directly.")
