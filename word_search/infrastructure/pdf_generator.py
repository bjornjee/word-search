from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from word_search.domain import Puzzle

TITLE_MAP = {
    "letters": "WORD SEARCH",
    "numbers": "NUMBER SEARCH",
    "chinese": "CHINESE SEARCH",
    "shapes": "SHAPE SEARCH",
}

LABEL_MAP = {
    "letters": "Find the words:",
    "numbers": "Find the numbers:",
    "chinese": "Find the words:",
    "shapes": "Find the shapes:",
}

FONT_MAP = {
    "letters": "Vera",
    "numbers": "Vera",
    "chinese": "STSong-Light",
    "shapes": "Courier",
}


def build_pdf(puzzle: Puzzle, filename: str) -> None:
    pdfmetrics.registerFont(TTFont("Vera", "Vera.ttf"))

    puzzle_type = puzzle.puzzle_type
    grid = puzzle.grid

    doc = SimpleDocTemplate(filename, pagesize=A4, topMargin=28, creator="Bjorn")

    cell_size = cm * 1.5
    data = [grid.data[i : i + grid.width] for i in range(0, len(grid.data), grid.width)]
    table = Table(data, len(data[0]) * [cell_size], len(data) * [cell_size])

    table_style = [
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 1, colors.black),
        ("FONTSIZE", (0, 0), (-1, -1), 22),
    ]

    if puzzle_type == "chinese":
        pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
        table_style.append(("FONTNAME", (0, 0), (-1, -1), "STSong-Light"))

    table.setStyle(TableStyle(table_style))

    font_name = FONT_MAP.get(puzzle_type, "Vera")
    heading_style = ParagraphStyle(
        "heading",
        fontName="Vera",
        fontSize=32,
        alignment=1,
    )
    label_style = ParagraphStyle(
        "label",
        fontName="Vera",
        fontSize=18,
        leading=30,
        spaceBefore=10,
        spaceAfter=10,
    )
    words_style = ParagraphStyle(
        "words",
        fontName=font_name,
        fontSize=18,
        leading=30,
        spaceBefore=10,
        spaceAfter=10,
    )

    title = TITLE_MAP.get(puzzle_type, "PUZZLE")
    label = LABEL_MAP.get(puzzle_type, "Find:")

    elements = [
        Paragraph(title, heading_style),
        Spacer(1, 2 * cm),
        table,
        Spacer(1, 0.5 * cm),
        Paragraph(label, label_style),
    ]

    words = puzzle.words
    mid = len(words) // 2
    elements.append(Paragraph(", ".join(words[:mid]), words_style))
    elements.append(Paragraph(", ".join(words[mid:]), words_style))

    doc.build(elements)
