#!/usr/bin/env python3

# Quadretta un foglio

import fpdf
import math

A4Width = 210.0
A4Height = 297.0

class Quadretti:

    def __init__(self, margin, side, sheet_offset, thick, vertical):
        self.page_number = 0
        self.border_width = 0.4
        self.thick_line_width = 0.2
        self.line_width = 0.05
        self.line_color = (127.5, 127.5, 127.5)
        self.border_color = (0, 0, 0)
        self.width = A4Width
        self.height = A4Height
        self.margin = margin
        self.side = side
        self.sheet_offset = sheet_offset
        self.thick = thick
        self.vertical = vertical
        self.nx = int(round((self.width - 2 * self.margin - self.sheet_offset) / self.side))
        self.ny = int(round((self.height - 2 * self.margin) / self.side))
        self.mx = (self.width  - self.sheet_offset - self.side * self.nx) / 2
        self.my = (self.height - self.side * self.ny) / 2

        self.pdf = fpdf.FPDF('P', 'mm', 'A4')
        self.pdf.set_creator('quadretti.py')
        self.pdf.set_title(f'Foglio quadrettato - {self.side}mm x {self.side}mm - {self.thick}')
        self.pdf.set_font('Arial', '', 10)
        self.pdf.set_auto_page_break(False)

    def grid(self, dx, dy):

        self.dx = dx
        self.dy = dy

        grid_width = self.side * self.nx
        grid_height = self.side * self.ny

        self.pdf.set_draw_color(*self.line_color)

        # righe orizz
        for i in range(1, self.ny):
            if self.thick == 0 or i % self.thick != 0:
                self.pdf.set_line_width(self.line_width)
            else:
                self.pdf.set_line_width(self.thick_line_width)
            self.line(0, i * self.side, grid_width, i * self.side)

# righe vert
        for i in range(1, self.nx):
            if self.vertical and i % self.thick  == 0:
                self.pdf.set_line_width(self.thick_line_width)
            else:
                self.pdf.set_line_width(self.line_width)
            self.line(i * self.side, 0, i * self.side, grid_height)

# contorno
        self.pdf.set_line_width(self.border_width)
        self.pdf.set_draw_color(*self.border_color)
        self.line(0, 0, grid_width, 0)
        self.line(grid_width, 0, grid_width, grid_height)
        self.line(grid_width, grid_height, 0, grid_height)
        self.line(0, grid_height, 0, 0)

    def line(self, x0, y0, x1, y1):
        self.pdf.line(self.dx + x0, self.dy + y0, self.dx + x1, self.dy + y1)

    def fill_circle(self, x, y, r):
        self.pdf.ellipse(self.dx + x, self.dy + y, r, r, 'F')

    def q_to_w(self, q_coords):
        return (q_coords[0] * self.side, q_coords[1] * self.side)

    def q_m(self, x, y):
        self.q_cur = (x, y)

    def q_rm(self, x, y):
        self.q_cur = (self.q_cur[0] + x, self.q_cur[1] + y)

    def q_rl(self, x, y):
        q_from = self.q_cur
        self.q_cur = (q_from[0] + x, q_from[1] + y)
        self.line(*self.q_to_w(q_from), *self.q_to_w(self.q_cur))

    def q_dot(self):
        self.fill_circle(*self.q_to_w(self.q_cur), 0.5)

    def q_rs(self, pts):
        p = pts[0]
        for i in range(len(pts) - 1):
            t = 0
            s = pts[i]
            e = pts[i+1]
            while t < 1.0:
                t += 0.1
                d = (
                     s[0] * (t-1.0) + e[0] * t,
                     s[1] * (t-1.0) + e[1] * t
                )
                self.q_rl(d[0] - p[0], d[1] - p[1])
                p = d
         
        
    def char(self, c):
        if c == ' ':
            self.q_rm(2, 0)
        elif c == '.':
            self.q_dot()
            self.q_rm(1, 0)

        elif c.lower() == 'a':
            self.q_rl(0.5, -2)
            self.q_rl(0.5, 2)
            self.q_rm(-0.75, -1)
            self.q_rl(0.5, 0)
            self.q_rm(1.25, 1)
        elif c.lower() == 'b':
            self.q_rs([(0, 0), (1,1)])
        else:
            raise NotImplementedError(f'Character "{c}" not implemented.')

    def write(self, text):
        for c in text:
            self.char(c)


    def page(self):
        self.pdf.add_page()
        self.page_number += 1


        page = f'Pagina: {self.page_number}'
        width = self.pdf.get_string_width(page)

        if self.page_number % 2 == 1:
# self.pdf.text(self.width - self.mx - width, self.my / 2 + 3, page)
            self.grid(self.sheet_offset + self.mx, self.my)
        else:
# self.pdf.text(self.mx, self.my / 2 + 3, page)
            self.grid(self.mx, self.my)

    def save(self, filename):
        if not filename.lower().endswith('.pdf'):
            filename += '.pdf'
        self.pdf.output(filename, 'F')

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description='Crea un foglio quadrettato (PDF).')
    parser.add_argument('-p', '--pages', type=int, nargs='?', help='Number of pages to create', default=1)
    parser.add_argument('-m', '--margin', type=float, nargs='?', help='Margin to leave around the grid', default=16.0)
    parser.add_argument('-s', '--side', type=float, nargs='?', help='Side of squares of grid', default=4.0)
    parser.add_argument('-o', '--sheet-offset', type=float, nargs='?', help='Additional offset on left (odd pages) or right (even pages)', default=0.0)
    parser.add_argument('-t', '--thick', type=int, nargs='?', help='Make every n-th orizontal line thicker', default=3)
    parser.add_argument('-v', '--vertical', action='store_true', help='Also make every n-th vertical line thicker')
    parser.add_argument('file', type=str, nargs='?', help='Output file', default='out.pdf')

    args = parser.parse_args()

    c = Quadretti(args.margin, args.side, args.sheet_offset, args.thick, args.vertical)

    for p in range(args.pages):
        c.page()
        c.q_m(1, 3)
        c.write('A b aa. AA aa.')
        c.save(args.file)

