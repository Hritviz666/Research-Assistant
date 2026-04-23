import re
from fpdf import FPDF


def clean(text: str) -> str:
    replacements = {
        "\u2013": "-",
        "\u2014": "--",
        "\u2015": "--",
        "\u2018": "'",
        "\u2019": "'",
        "\u201a": ",",
        "\u201b": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u201e": '"',
        "\u2022": "-",
        "\u2023": "-",
        "\u2024": ".",
        "\u2025": "..",
        "\u2026": "...",
        "\u2027": ".",
        "\u2032": "'",
        "\u2033": '"',
        "\u2039": "<",
        "\u203a": ">",
        "\u2044": "/",
        "\u00a0": " ",
        "\u00ab": '"',
        "\u00bb": '"',
        "\u00b7": "-",
        "\u2010": "-",
        "\u2011": "-",
        "\u2012": "-",
        "\u00e9": "e",
        "\u00e8": "e",
        "\u00ea": "e",
        "\u00eb": "e",
        "\u00e0": "a",
        "\u00e1": "a",
        "\u00e2": "a",
        "\u00e4": "a",
        "\u00f1": "n",
        "\u00f6": "o",
        "\u00fc": "u",
        "\u00df": "ss",
        "\u00e7": "c",
        "\u00ae": "(R)",
        "\u00a9": "(C)",
        "\u2122": "(TM)",
        "\u00b0": " degrees",
        "\u00b1": "+/-",
        "\u00d7": "x",
        "\u00f7": "/",
        "\u2248": "~",
        "\u2260": "!=",
        "\u2264": "<=",
        "\u2265": ">=",
        "\u00bc": "1/4",
        "\u00bd": "1/2",
        "\u00be": "3/4",
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)

    # Final fallback: strip anything still non-ASCII
    text = text.encode("ascii", errors="ignore").decode("ascii")
    return text


class PDFReport(FPDF):

    def header(self):
        self.set_font("Helvetica", style="I", size=9)
        self.set_text_color(130, 130, 130)
        self.cell(0, 8, "AI Research Assistant", align="R")
        self.ln(3)
        self.set_draw_color(210, 210, 210)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", style="I", size=8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def markdown_to_pdf(content: str, title: str = "Research Report") -> bytes:
    pdf = PDFReport()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(15, 15, 15)
    pdf.add_page()

    lines = content.split("\n")

    for line in lines:
        stripped = clean(line.strip())

        # H1
        if stripped.startswith("# ") and not stripped.startswith("## "):
            pdf.set_font("Helvetica", style="B", size=18)
            pdf.set_text_color(20, 20, 20)
            pdf.multi_cell(0, 10, stripped[2:].strip())
            pdf.ln(2)

        # H2
        elif stripped.startswith("## ") and not stripped.startswith("### "):
            pdf.set_font("Helvetica", style="B", size=14)
            pdf.set_text_color(40, 40, 40)
            pdf.ln(3)
            pdf.multi_cell(0, 9, stripped[3:].strip())
            pdf.set_draw_color(210, 210, 210)
            pdf.line(15, pdf.get_y(), 195, pdf.get_y())
            pdf.ln(4)

        # H3
        elif stripped.startswith("### "):
            pdf.set_font("Helvetica", style="B", size=12)
            pdf.set_text_color(60, 60, 60)
            pdf.ln(2)
            pdf.multi_cell(0, 8, stripped[4:].strip())
            pdf.ln(2)

        # Horizontal rule
        elif stripped in ("---", "***", "___"):
            pdf.set_draw_color(200, 200, 200)
            pdf.ln(2)
            pdf.line(15, pdf.get_y(), 195, pdf.get_y())
            pdf.ln(4)

        # Table row
        elif stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if all(re.match(r"^[-: ]+$", c) for c in cells):
                continue
            col_width = 175 / max(len(cells), 1)
            is_header = any("**" in c for c in cells)
            pdf.set_font("Helvetica", style="B" if is_header else "", size=9)
            pdf.set_text_color(30, 30, 30)
            pdf.set_fill_color(235, 235, 235)
            for cell in cells:
                cell_text = re.sub(r"\*\*(.*?)\*\*", r"\1", cell)
                cell_text = re.sub(r"\*(.*?)\*", r"\1", cell_text)
                pdf.cell(
                    col_width, 8,
                    cell_text[:40],
                    border=1,
                    fill=is_header,
                    align="L"
                )
            pdf.ln()

        # Bullet point
        elif stripped.startswith("- ") or stripped.startswith("* "):
            text = stripped[2:].strip()
            text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
            text = re.sub(r"\*(.*?)\*", r"\1", text)
            pdf.set_font("Helvetica", size=10)
            pdf.set_text_color(30, 30, 30)
            pdf.set_x(18)
            pdf.cell(6, 7, "-")
            pdf.multi_cell(0, 7, text)

        # Numbered list
        elif re.match(r"^\d+\.", stripped):
            text = re.sub(r"^\d+\.\s*", "", stripped)
            text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
            text = re.sub(r"\*(.*?)\*", r"\1", text)
            pdf.set_font("Helvetica", size=10)
            pdf.set_text_color(30, 30, 30)
            pdf.set_x(18)
            pdf.multi_cell(0, 7, text)

        # Empty line
        elif stripped == "":
            pdf.ln(3)

        # Normal paragraph
        else:
            text = re.sub(r"\*\*(.*?)\*\*", r"\1", stripped)
            text = re.sub(r"\*(.*?)\*", r"\1", text)
            text = re.sub(r"`(.*?)`", r"\1", text)
            pdf.set_font("Helvetica", size=10)
            pdf.set_text_color(30, 30, 30)
            pdf.multi_cell(0, 7, text)

    return bytes(pdf.output())