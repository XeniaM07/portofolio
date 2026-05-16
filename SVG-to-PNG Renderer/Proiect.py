"""
Proiect SVG to Image Renderer

Acest script parcurge un fișier SVG, extrage informațiile despre forme
și le redă pe un canvas, salvând rezultatul într-un fișier PNG.

Autor: Mariei Xenia
Grupa: B2
An: 3
Data: 17.12.2024

Scop: Proiect universitar pentru cursul de "Programare in Python".
"""
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw
from shapes import Rectangle, Circle, Ellipse, Line, Polyline, Path

class SVGRenderer:
    """
    Clasa care procesează un fișier SVG și îl convertește într-o imagine PNG.

    Atribut:
        svg_file (str): Calea către fișierul SVG de procesat.
        shapes (list): Lista de forme desenabile extrase din fișierul SVG.

    Metode:
        parse_svg() -> tuple: Extrage și returnează dimensiunile canvas-ului și formele din SVG.
        create_shape(tag, attributes, canvas_width, canvas_height) -> obiect: Creează un obiect formă pe baza tagului.
        render(): Desenează formele pe un canvas și salvează imaginea în format PNG.
    """

    def __init__(self, svg_file):
        """
        Inițializează un obiect `SVGRenderer` cu fișierul SVG și o listă de forme.

        Args:
            svg_file (str): Calea către fișierul SVG de procesat.
        """
        self.svg_file = svg_file
        self.shapes = []

    def parse_svg(self):
        """
        Parcurge fișierul SVG și extrage dimensiunile canvas-ului și formele grafice.

        Returnează:
            tuple: Dimensiunile canvas-ului și o listă de forme extrase din fișierul SVG.
        """
        supported_shapes = ['rect', 'circle', 'ellipse', 'line', 'polyline', 'path']
        try:
            tree = ET.parse(self.svg_file)
            root = tree.getroot()
        except ET.ParseError as e:
            print(f"Eroare la citirea fișierului SVG: {e}")
            return 500, 500

        width = float(root.attrib.get('width', 500))
        height = float(root.attrib.get('height', 500))

        for element in root.iter():
            tag = element.tag.split('}')[-1]
            attributes = element.attrib
            if tag in supported_shapes:
                shape = self.create_shape(tag, attributes, width, height)
                if shape:
                    self.shapes.append(shape)

        return int(width), int(height)  # Convertim float în int

    @staticmethod
    def create_shape(tag, attributes, canvas_width, canvas_height):
        """
        Creează un obiect formă pe baza tagului și atributelor.

        Args:
            tag (str): Tipul formei (de exemplu, 'rect', 'circle').
            attributes (dict): Atributele formei (ex: 'x', 'y', 'fill').
            canvas_width (int): Lățimea canvas-ului.
            canvas_height (int): Înălțimea canvas-ului.

        Returnează:
            obiect: O instanță a formei corespunzătoare.
        """
        if tag == 'rect':
            return Rectangle(attributes, canvas_width, canvas_height)
        elif tag == 'circle':
            return Circle(attributes, canvas_width, canvas_height)
        elif tag == 'ellipse':
            return Ellipse(attributes, canvas_width, canvas_height)
        elif tag == 'line':
            return Line(attributes, canvas_width, canvas_height)
        elif tag == 'polyline':
            return Polyline(attributes, canvas_width, canvas_height)
        elif tag == 'path':
            return Path(attributes, canvas_width, canvas_height)
        return None

    def render(self):
        """
        Desenează formele extrase din SVG pe un canvas și salvează imaginea ca fișier PNG.

        Această metodă creează un canvas alb, desenează formele din lista `shapes` și salvează rezultatul
        ca fișier PNG.

        Returnează:
            None
        """
        canvas_width, canvas_height = self.parse_svg()
        image = Image.new('RGB', (canvas_width, canvas_height), 'white')
        draw_context = ImageDraw.Draw(image)

        for shape in self.shapes:
            shape.draw(draw_context)

        image.show()
        image.save("output.png")
        print("Imaginea a fost salvată ca 'output.png'.")


if __name__ == "__main__":
    """
    Punctul de intrare principal al aplicației care citește fișierul SVG și îl convertește într-o imagine PNG.

    Acesta inițializează obiectul `SVGRenderer`, procesează fișierul SVG și generează imaginea finală.
    """
    svg_renderer = SVGRenderer("test.xml")
    svg_renderer.render()
