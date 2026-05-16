# SVG-to-PNG Renderer

SVG-to-PNG Renderer is a Python project that implements a simplified SVG rendering engine capable of parsing SVG files and converting them into raster PNG images.

The project was developed as part of a university assignment focused on graphics processing, XML parsing, and rendering pipelines.  
The implementation recreates core concepts used in rendering engines, including shape rasterization, coordinate handling, color processing, and scene rendering.

## Project Features

- XML/SVG parsing
- Internal scene representation
- SVG attribute extraction
- Raster rendering pipeline
- Rectangle rendering
- Circle and ellipse rendering
- Line and polyline rendering
- Path parsing support
- Stroke and fill handling
- PNG image export
- Rendering validation examples

## Technologies Used

- Python
- Pillow (PIL)
- XML processing

## Supported SVG Elements

- Rectangle
- Circle
- Ellipse
- Line
- Polyline
- Path

## Project Structure

```text
Proiect.py      -> main renderer logic
shapes.py       -> geometric shape implementations
utils.py        -> helper and utility functions
test.xml        -> sample SVG input
output-uri/     -> rendered PNG examples