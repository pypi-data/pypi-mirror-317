# FagFlag

A Python package to generate pride flags in bitmap (PNG) or vector (SVG) formats. Supports a variety of pride flag color schemes and allows generating flags in customizable sizes with the option to overlay PNG images.

## Features

- **Generate Bitmap Flags (PNG)**: Create pride flags in bitmap format with customizable sizes and optional PNG overlay.
- **Generate Vector Flags (SVG)**: Generate pride flags in SVG format with a fixed aspect ratio.
- **Color Schemes**: Includes several popular pride flag color schemes (e.g., Transgender, Gay, Bi, Nonbinary).
- **Output Flexibility**: Supports generating flags in either "bitmap" (PNG) or "vector" (SVG) formats.
- **Customizable Sizes**: Bitmap flags can be generated with user-defined width and height. By default, flags are generated with a 1:1 aspect ratio (e.g., 512x512).
- **Overlay PNG**: Option to overlay a PNG image on the generated bitmap flags. The image will be resized to fit the flag and centered without stretching.
- **Command-Line Interface**: You can generate flags directly from the command line with various options for sizes, formats, overlays, and more.

## Installation

To install the package, use pip:

```bash
pip install fagflag
```

Alternatively, you can clone the repository and install it locally:

```bash
git clone https://github.com/Red-Panda-Studios/fagflag
cd fagflag
pip install .
```

## Usage

### Importing the Package

```python
from fagflag import generate_flags
```

### Generating Flags Programmatically

You can generate flags by specifying the flag names, output format, width, height, output directory, and optionally, a PNG overlay image.

```python
from fagflag import generate_flags

# Example usage: Generate pride flags
flags = ["trans", "gay", "bi"]
output_format = "bitmap"  # Can be "bitmap" or "vector"
width = 256  # Flag width
height = 256  # Flag height
output_dir = "./generated_flags"
overlay_path = "./overlay_image.png"  # Optional overlay image path

generate_flags(flags, output_format, width, height, output_dir, overlay_path)
```

### Command-Line Usage

You can also generate flags from the command line using the following arguments:

```bash
python -m fagflag --create --flags trans,gay,bi --format bitmap --width 256 --height 256 --output ./generated_flags --overlay ./overlay_image.png
```

#### Available Arguments

- `--create`: Generate flags.
- `--flags`: Comma-separated list of flags to generate (e.g., `trans,gay,bi`).
- `--format`: Output format, either `bitmap` (PNG) or `vector` (SVG).
- `--width`: Width of the generated flags (overrides sizes for bitmap).
- `--height`: Height of the generated flags (overrides sizes for bitmap).
- `--output`: Directory to save the generated flags.
- `--overlay`: Optional path to a PNG image to overlay on the generated bitmap flags.

### Available Pride Flags

Here is a table of the available pride flags that you can generate:

| Flag Name       | Description        |
|-----------------|--------------------|
| `trans`         | Transgender Pride  |
| `gay`           | Gay Pride          |
| `bi`            | Bisexual Pride     |
| `nonbinary`     | Nonbinary Pride    |
| `pan`           | Pansexual Pride    |
| `asexual`       | Asexual Pride      |
| `genderfluid`   | Genderfluid Pride  |
| `lesbian`       | Lesbian Pride      |
| `aromantic`     | Aromantic Pride    |
| `demiboy`       | Demiboy Pride      |
| `demigirl`      | Demigirl Pride     |
| `transfemme`    | Transfemme Pride   |
| `transmasc`     | Transmasc Pride    |
| `mlm`           | MLM Pride          |

### Flag Color Schemes

Each flag's colors are defined by a list of hex codes. Here are the colors for the listed flags:

| Flag Name       | Colors                                                                                      |
|-----------------|---------------------------------------------------------------------------------------------|
| `trans`         | `["#5bcffa", "#f5a9b8", "#FFFFFF", "#f5a9b8", "#5bcffa"]`                                   |
| `gay`           | `["#e50203", "#ff8b01", "#feed00", "#008026", "#004dfe", "#750685"]`                        |
| `bi`            | `["#d70071", "#d70071", "#9c4e97", "#0035aa", "#0035aa"]`                                   |
| `nonbinary`     | `["#fff430", "#FFFFFF", "#9c59d1", "#292929"]`                                              |
| `pan`           | `["#ff1b8d", "#ffd900", "#1bb3ff"]`                                                        |
| `asexual`       | `["#000000", "#a4a4a5", "#ffffff", "#810081"]`                                              |
| `genderfluid`   | `["#ff75a2", "#ffffff", "#be18d6", "#000000", "#333ebd"]`                                  |
| `lesbian`       | `["#d62900", "#ff9b55", "#ffffff", "#d462a6", "#a40062"]`                                  |
| `aromantic`     | `["#3da542", "#a7d379", "#ffffff", "#a9a9a9", "#000000"]`                                  |
| `demiboy`       | `["#7f7f7f", "#c3c3c3", "#99d9ea", "#FFFFFF", "#99d9ea", "#c3c3c3", "#7f7f7f"]`            |
| `demigirl`      | `["#7f7f7f", "#c3c3c3", "#ffaec9", "#FFFFFF", "#ffaec9", "#c3c3c3", "#7f7f7f"]`            |
| `transfemme`    | `["#74deff", "#ffe1ed", "#ffb5d6", "#fe8cbf", "#ffb5d6", "#ffe1ed", "#74deff"]`             |
| `transmasc`     | `["#ff8bbf", "#cdf5ff", "#9aedff", "#76e0ff", "#9aedff", "#cdf5ff", "#ff8bbf"]`             |
| `mlm`           | `["#018e71", "#21cfac", "#99e9c2", "#ffffff", "#7cafe3", "#4f47cd", "#3a1379"]`             |

### Bitmap Flags

Bitmap flags are generated in PNG format. You can specify the `width` and `height` of the generated flags, and the images will be saved in the output directory with filenames like `flag_name_widthxheight.png`. You can also pass an optional PNG image to overlay on the flag (the image will be resized to fit the flag's size and centered).

### Vector Flags

Vector flags are generated in SVG format with a fixed height of 100 units and a 2:1 aspect ratio. To generate vector flags, use the `format="vector"` and specify the output width and height.

### Overlaying PNG

You can optionally provide a PNG image to overlay on the bitmap flags. The image will be resized to fit the width and height of the generated flag and will be centered without stretching. For example:

```python
overlay_path = "./overlay_image.png"  # Optional PNG overlay image path
```

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
