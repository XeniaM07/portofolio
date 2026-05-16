from utils import normalize_value
import re

class Rectangle:
    """
    Desenează un dreptunghi pe baza atributelor acestuia.

    Args:
        draw (ImageDraw): Contextul de desenare.
        attributes (dict): Atributele dreptunghiului.
        canvas_width (int): Lățimea canvas-ului.
        canvas_height (int): Înălțimea canvas-ului.
    """
    def __init__(self, attributes, canvas_width, canvas_height):
        self.x = normalize_value(attributes.get('x', '0'), canvas_width)
        self.y = normalize_value(attributes.get('y', '0'), canvas_height)
        self.width = normalize_value(attributes.get('width', '0'), canvas_width)
        self.height = normalize_value(attributes.get('height', '0'), canvas_height)
        self.fill = attributes.get('fill', 'none')
        self.stroke = attributes.get('stroke', 'none')

    def draw(self, draw_context):
        fill = None if self.fill == "none" else self.fill
        stroke = None if self.stroke == "none" else self.stroke
        draw_context.rectangle([self.x, self.y, self.x + self.width, self.y + self.height], fill=fill, outline=stroke)

class Circle:
    """
    Desenează un cerc pe baza atributelor acestuia.

    Args:
        draw (ImageDraw): Contextul de desenare.
        attributes (dict): Atributele cercului.
        canvas_width (int): Lățimea canvas-ului.
        canvas_height (int): Înălțimea canvas-ului.
    """
    def __init__(self, attributes, canvas_width, canvas_height):
        self.cx = normalize_value(attributes.get('cx', '0'), canvas_width)
        self.cy = normalize_value(attributes.get('cy', '0'), canvas_height)
        self.r = normalize_value(attributes.get('r', '0'), canvas_width)
        self.fill = attributes.get('fill', 'none')
        self.stroke = attributes.get('stroke', 'none')

    def draw(self, draw_context):
        fill = None if self.fill == "none" else self.fill
        stroke = None if self.stroke == "none" else self.stroke
        draw_context.ellipse([self.cx - self.r, self.cy - self.r, self.cx + self.r, self.cy + self.r], fill=fill, outline=stroke)

class Ellipse:
    """
    Desenează o elipsă pe canvas.

    Args:
        draw (ImageDraw): Contextul de desenare.
        attributes (dict): Atributele elipsei.
        canvas_width (int): Lățimea canvas-ului.
        canvas_height (int): Înălțimea canvas-ului.

    Note:
        Elipsa este definită prin centrul său (`cx`, `cy`) și razele pe axele orizontală (`rx`)
        și verticală (`ry`). Culorile de umplere și contur sunt specificate prin atributele
        `fill` și `stroke`, iar dacă acestea sunt `none`, nu se vor aplica.

    """
    def __init__(self, attributes, canvas_width, canvas_height):
        self.cx = normalize_value(attributes.get('cx', '0'), canvas_width)
        self.cy = normalize_value(attributes.get('cy', '0'), canvas_height)
        self.rx = normalize_value(attributes.get('rx', '0'), canvas_width)
        self.ry = normalize_value(attributes.get('ry', '0'), canvas_height)
        self.fill = attributes.get('fill', 'none')
        self.stroke = attributes.get('stroke', 'none')

    def draw(self, draw_context):
        fill = None if self.fill == "none" else self.fill
        stroke = None if self.stroke == "none" else self.stroke
        draw_context.ellipse([self.cx - self.rx, self.cy - self.ry, self.cx + self.rx, self.cy + self.ry], fill=fill, outline=stroke)

class Line:
    """
    Desenează o linie pe baza atributelor acesteia.

    Args:
        draw (ImageDraw): Contextul de desenare.
        attributes (dict): Atributele liniei.
        canvas_width (int): Lățimea canvas-ului.
        canvas_height (int): Înălțimea canvas-ului.
    """
    def __init__(self, attributes, canvas_width, canvas_height):
        self.x1 = normalize_value(attributes.get('x1', '0'), canvas_width)
        self.y1 = normalize_value(attributes.get('y1', '0'), canvas_height)
        self.x2 = normalize_value(attributes.get('x2', '0'), canvas_width)
        self.y2 = normalize_value(attributes.get('y2', '0'), canvas_height)
        self.stroke = attributes.get('stroke', 'none')
        self.stroke_width = int(attributes.get('stroke-width', 1))

    def draw(self, draw_context):
        stroke = None if self.stroke == "none" else self.stroke
        draw_context.line([self.x1, self.y1, self.x2, self.y2], fill=stroke, width=self.stroke_width)

class Polyline:
    """
    Desenează o polilinie pe canvas.

    Args:
        draw (ImageDraw): Contextul de desenare.
        attributes (dict): Atributele poliliniei.
        canvas_width (int): Lățimea canvas-ului.
        canvas_height (int): Înălțimea canvas-ului.

    Note:
        Dacă punctele formează o formă închisă, aceasta va fi umplută,
        altfel se va desena doar linia de contur.
    """
    def __init__(self, attributes, canvas_width, canvas_height):
        self.points = attributes['points'].strip().split()
        self.points = [
            tuple(
                map(
                    lambda v: normalize_value(v, canvas_width if i % 2 == 0 else canvas_height),
                    map(float, point.split(','))
                )
            )
            for i, point in enumerate(self.points)
        ]
        self.fill = attributes.get('fill', 'none')
        self.stroke = attributes.get('stroke', 'none')
        self.stroke_width = int(attributes.get('stroke-width', 1))

    def draw(self, draw_context):
        fill = None if self.fill == "none" else self.fill
        stroke = None if self.stroke == "none" else self.stroke

        # Dacă punctele formează o formă închisă, o desenăm ca polygon (umplută)
        if len(self.points) > 2 and self.points[0] == self.points[-1]:
            draw_context.polygon(self.points, fill=fill, outline=stroke)
        else:
            draw_context.line(self.points, fill=stroke, width=self.stroke_width)

class Path:
    """
    Desenează o cale (path) pe canvas.

    Args:
        draw (ImageDraw): Contextul de desenare.
        attributes (dict): Atributele căii.
        canvas_width (int): Lățimea canvas-ului.
        canvas_height (int): Înălțimea canvas-ului.

    Note:
        Suportă comenzi precum M, L, C, Q și Z din atributele `d` ale SVG-ului.
        Calea poate include segmente deschise sau închise.
    """
    def __init__(self, attributes, canvas_width, canvas_height):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.path_data = attributes['d']
        self.fill = attributes.get('fill', 'none')
        self.stroke = attributes.get('stroke', 'none')
        self.stroke_width = int(attributes.get('stroke-width', 1))

    def draw(self, draw_context):
        fill = None if self.fill == "none" else self.fill
        stroke = None if self.stroke == "none" else self.stroke

        # Extrage comenzile și coordonatele din atributul `d`
        path_commands = re.findall(r'[A-Za-z][^A-Za-z]*', self.path_data)
        points = []
        current_pos = None
        start_pos = None

        for command in path_commands:
            cmd = command[0]
            coords_str = command[1:].strip()

            if coords_str:
                try:
                    coords = list(map(float, re.split('[, ]+', coords_str)))
                except ValueError:
                    print(f"Coordonate invalide: {coords_str}")
                    continue
            else:
                coords = []

            if cmd == 'M' and len(coords) == 2:  # Move to
                current_pos = (
                    normalize_value(coords[0], self.canvas_width),
                    normalize_value(coords[1], self.canvas_height)
                )
                start_pos = current_pos
                points.append(current_pos)
            elif cmd == 'L' and len(coords) == 2:  # Line to
                if current_pos is not None:
                    next_pos = (
                        normalize_value(coords[0], self.canvas_width),
                        normalize_value(coords[1], self.canvas_height)
                    )
                    points.append(next_pos)
                    current_pos = next_pos
            elif cmd == 'C' and len(coords) == 6:  # Cubic Bezier Curve
                if current_pos is not None:
                    next_pos = (
                        normalize_value(coords[4], self.canvas_width),
                        normalize_value(coords[5], self.canvas_height)
                    )
                    points.append(next_pos)
            elif cmd == 'Q' and len(coords) == 4:  # Quadratic Bezier Curve
                if current_pos is not None:
                    next_pos = (
                        normalize_value(coords[2], self.canvas_width),
                        normalize_value(coords[3], self.canvas_height)
                    )
                    points.append(next_pos)
            elif cmd == 'Z' and current_pos is not None and start_pos is not None:  # Close Path
                points.append(start_pos)

        if points:
            draw_context.polygon(points, fill=fill, outline=stroke)
