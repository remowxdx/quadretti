#!/usr/bin/env python3
"""
Disegna un foglio quadrettato
"""

import math
import cairo
from cairo import PDFMetadata  # pylint: disable=no-name-in-module

from elementary_font import ElementaryFont

A4WIDTH = 210.0
A4HEIGHT = 297.0


def mm_to_pt(length_mm):
    """Transform mm to pt."""
    return length_mm / 25.2 * 72


def lerp(p_0, p_1, t):
    """Linear interpolate between two points"""
    return (p_0[0] * (1.0 - t) + p_1[0] * t, p_0[1] * (1.0 - t) + p_1[1] * t)


class Quadretti:  # pylint: disable=too-many-instance-attributes
    """Squaring class"""

    # pylint: disable=too-many-arguments
    def __init__(self, margin, side, sheet_offset, thick, vertical):
        self.page_number = 0
        self.border_width = 0.4
        self.thick_line_width = 0.2
        self.line_width = 0.05
        self.line_color = (0.5, 0.5, 0.5)
        self.border_color = (0, 0, 0)
        self.width = A4WIDTH
        self.height = A4HEIGHT
        self.margin = margin
        self.side = side
        self.sheet_offset = sheet_offset
        self.thick = thick
        self.vertical = vertical
        self.num_x = int(
            round((self.width - 2 * self.margin - self.sheet_offset) / self.side)
        )
        self.num_y = int(round((self.height - 2 * self.margin) / self.side))
        self.m_x = (self.width - self.sheet_offset - self.side * self.num_x) / 2
        self.m_y = (self.height - self.side * self.num_y) / 2
        self.q_cur = 0

        # pylint: disable=no-member
        self.pdf = cairo.PDFSurface(
            "quadretti.pdf", mm_to_pt(self.width), mm_to_pt(self.height)
        )
        self.pdf.set_metadata(PDFMetadata.CREATOR, "quadretti.py")
        self.pdf.set_metadata(
            PDFMetadata.TITLE,
            f"Foglio quadrettato - {self.side}mm x {self.side}mm - {self.thick}",
        )
        self.ctx = cairo.Context(self.pdf)
        self.ctx.scale(mm_to_pt(1), mm_to_pt(1))
        self.ctx.select_font_face(
            "Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL
        )
        self.ctx.set_font_size(10)
        self.delta_x = 0
        self.delta_y = 0

    def grid(self, delta_x, delta_y):
        """Draw the grid."""

        self.delta_x = delta_x
        self.delta_y = delta_y

        grid_width = self.side * self.num_x
        grid_height = self.side * self.num_y

        self.ctx.set_source_rgb(*self.line_color)

        # righe orizz
        for i in range(1, self.num_y):
            if self.thick == 0 or i % self.thick != 0:
                self.ctx.set_line_width(self.line_width)
            else:
                self.ctx.set_line_width(self.thick_line_width)
            self.line(0, i * self.side, grid_width, i * self.side)

        # righe vert
        for i in range(1, self.num_x):
            if self.vertical and i % self.thick == 0:
                self.ctx.set_line_width(self.thick_line_width)
            else:
                self.ctx.set_line_width(self.line_width)
            self.line(i * self.side, 0, i * self.side, grid_height)

        # contorno
        self.ctx.set_line_width(self.border_width)
        self.ctx.set_source_rgb(*self.border_color)
        self.line(0, 0, grid_width, 0)
        self.line(grid_width, 0, grid_width, grid_height)
        self.line(grid_width, grid_height, 0, grid_height)
        self.line(0, grid_height, 0, 0)

    def line(self, x_0, y_0, x_1, y_1):
        """Draw line from (x_0, y_0) to (x_1, y_1)."""
        self.ctx.new_path()
        self.ctx.move_to(self.delta_x + x_0, self.delta_y + y_0)
        self.ctx.line_to(self.delta_x + x_1, self.delta_y + y_1)
        self.ctx.stroke()

    def fill_circle(self, x, y, radius):
        """Draw filles circle."""
        self.ctx.new_path()
        self.ctx.arc(self.delta_x + x, self.delta_y + y, radius, 0, 2 * math.pi)
        self.ctx.fill()

    def q_to_w(self, q_coords):
        """Trasform in square units"""
        return (q_coords[0] * self.side, q_coords[1] * self.side)

    def q_m(self, x, y):
        """Move to (x, y)"""
        self.q_cur = (x, y)

    def q_rm(self, x, y):
        """Move current position by (x, y)"""
        self.q_cur = (self.q_cur[0] + x, self.q_cur[1] + y)

    def q_l(self, x, y):
        """Line to absolute position."""
        q_from = self.q_cur
        self.q_cur = (x, y)
        self.line(*self.q_to_w(q_from), *self.q_to_w(self.q_cur))

    def q_rl(self, x, y):
        """Draw line relative to current position"""
        q_from = self.q_cur
        self.q_cur = (q_from[0] + x, q_from[1] + y)
        self.line(*self.q_to_w(q_from), *self.q_to_w(self.q_cur))

    def q_dot(self):
        """Draw a point in current position"""
        self.fill_circle(*self.q_to_w(self.q_cur), 0.5)

    def q_rs(self, pts):
        """Draw spline"""

        def spline(pts, t):
            """Spline points"""
            if len(pts) == 1:
                return pts[0]

            next_level = []
            for i in range(len(pts) - 1):
                next_level.append(lerp(pts[i], pts[i + 1], t))
            return spline(next_level, t)

        start = self.q_cur
        points = [start]
        for point in pts:
            points.append((points[-1][0] + point[0], points[-1][1] + point[1]))

        t = 0.0
        while t <= 1.0:
            self.q_l(*spline(points, t))
            t += 0.1
        # self.q_m(*start)
        # for point in pts:
        #     self.q_rl(*point)

    def q_lf(self):
        """Line feed"""
        self.q_cur = (1, self.q_cur[1] + 3)

    def write(self, text):
        """Write text."""
        self.ctx.set_line_cap(cairo.LINE_CAP_ROUND)  # pylint: disable=no-member
        font = ElementaryFont(self.q_rm, self.q_rl, self.q_rs, self.q_dot, self.q_lf)
        for character in text:
            font.char(character)

    def page(self):
        """Make new page"""
        self.page_number += 1

        # page = f"Pagina: {self.page_number}"
        # width = self.pdf.get_string_width(page)

        if self.page_number % 2 == 1:
            # self.pdf.text(self.width - self.mx - width, self.my / 2 + 3, page)
            self.grid(self.sheet_offset + self.m_x, self.m_y)
        else:
            # self.pdf.text(self.mx, self.my / 2 + 3, page)
            self.grid(self.m_x, self.m_y)

    def save(self, filename):
        """Save to file."""
        if not filename.lower().endswith(".pdf"):
            filename += ".pdf"
        self.pdf.show_page()


def main():
    """Parse cmdline args and do the show!"""

    parser = argparse.ArgumentParser(description="Crea un foglio quadrettato (PDF).")
    parser.add_argument(
        "-p",
        "--pages",
        type=int,
        nargs="?",
        help="Number of pages to create",
        default=1,
    )
    parser.add_argument(
        "-m",
        "--margin",
        type=float,
        nargs="?",
        help="Margin to leave around the grid",
        default=16.0,
    )
    parser.add_argument(
        "-s",
        "--side",
        type=float,
        nargs="?",
        help="Side of squares of grid",
        default=4.0,
    )
    parser.add_argument(
        "-o",
        "--sheet-offset",
        type=float,
        nargs="?",
        help="Additional offset on left (odd pages) or right (even pages)",
        default=0.0,
    )
    parser.add_argument(
        "-t",
        "--thick",
        type=int,
        nargs="?",
        help="Make every n-th orizontal line thicker",
        default=3,
    )
    parser.add_argument(
        "-v",
        "--vertical",
        action="store_true",
        help="Also make every n-th vertical line thicker",
    )
    parser.add_argument(
        "file", type=str, nargs="?", help="Output file", default="out.pdf"
    )

    args = parser.parse_args()

    quadretti = Quadretti(
        args.margin, args.side, args.sheet_offset, args.thick, args.vertical
    )

    for _page in range(args.pages):
        quadretti.page()
        try:
            quadretti.q_m(1, 3)
            quadretti.write("Aa Bb Cc Dd Ee Ff.\nGg Hh Ii Jj Kk Ll.\n")
            quadretti.write("Mm Nn Oo Pp Qq Rr.\nSs Tt Uu Vv Ww Xx.\n")
            quadretti.write("Yy Zz !! ?? -- ++.\n")
            quadretti.write("0123456789 ,, ==.\n")
            quadretti.write("3+5=8\n")
            quadretti.write("Il gatto sul tetto, si\nmangia il topo. Morto.\n")
        except NotImplementedError:
            pass
        quadretti.save(args.file)


if __name__ == "__main__":
    import argparse

    main()
