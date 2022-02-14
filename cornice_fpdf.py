#!/usr/bin/python2

import fpdf
import math


class cornice(object):
  
  def __init__(self, width, height, margin):
    self.f_dx = width
    self.f_dy = height
    self.c_margin = margin
    self.margin = 5
    self.overlap = 5
    self.c_radius = 5
    self.b_dx = self.f_dx - 2 * self.overlap
    self.b_dy = self.f_dy - 2 * self.overlap
    self.f_x = self.c_margin - self.overlap
    self.f_y = self.c_margin - self.overlap
    self.c_dx = 2 * self.c_margin + self.b_dx
    self.c_dy = 2 * self.c_margin + self.b_dy
    self.s_dx_c = 50
    self.s_dx_l = 80
    self.s_dl = self.c_dy * 4 / 5
    self.s_dx_i = 15
    self.s_dy_i = 20
    self.s_dl_i = (self.s_dl - self.s_dy_i * 3) / 2 
    self.s_r = self.s_dx_i + 5
    self.s_tx = self.s_dy_i * (self.s_dx_l - self.s_dx_c) / self.s_dl / 2
    
    orient = 'P'
    if width > height:
      orient = 'L'
    self.pdf = fpdf.FPDF(orient, 'mm', 'A4')
    self.pdf.set_creator('cornice.py')
    self.pdf.set_title('Cornice %d x %d - %d'%(width, height, margin))
    self.pdf.set_font('Arial', '', 10)

  def front(self):
    self.pdf.add_page()
    # Esterno
    self.r_rect(0, 0, self.c_dx, self.c_dy, self.c_radius)
    
    # Buco
    self.rect(self.c_margin, self.c_margin,  self.b_dx, self.b_dy)
    
    # Foto
    self.pdf.set_draw_color(255, 0 ,0)
    self.rect(self.f_x, self.f_y, self.f_dx, self.f_dy, 1)
    self.l(self.f_x,self.f_y, self.f_x + self.f_dx, self.f_y + self.f_dy, 1)
    self.l(self.f_x + self.f_dx ,self.f_y, self.f_x, self.f_y + self.f_dy, 1)
    self.pdf.set_draw_color(0, 0 ,0)
    
  def back(self):
    self.pdf.add_page()
    # Esterno
    self.r_rect(0, 0, self.c_dx, self.c_dy, self.c_radius)
    
    # Acc. colla
    self.l(self.c_dx / 2 - self.s_dx_c / 2, self.c_dy - self.s_dl, self.c_dx / 2 + self.s_dx_c / 2, self.c_dy - self.s_dl, 1)
    self.l(self.c_dx / 2 + self.s_dx_c / 2, self.c_dy - self.s_dl, self.c_dx / 2 + self.s_dx_c / 2 + self.s_tx, self.c_dy - self.s_dl + self.s_dy_i, 1)
    self.l(self.c_dx / 2 - self.s_dx_c / 2 - self.s_tx, self.c_dy - self.s_dl + self.s_dy_i, self.c_dx / 2 + self.s_dx_c / 2 + self.s_tx, self.c_dy - self.s_dl + self.s_dy_i, 1)
    self.l(self.c_dx / 2 - self.s_dx_c / 2 - self.s_tx, self.c_dy - self.s_dl + self.s_dy_i, self.c_dx / 2 - self.s_dx_c / 2, self.c_dy - self.s_dl, 1)
    self.pdf.text(self.c_dx / 2 - self.s_dx_c / 2+10, self.c_dy - self.s_dl+15, 'Colla')
    
    ty = self.c_dy - self.s_dl + (self.s_dl + self.s_dy_i - self.s_dl_i - self.s_dx_i + self.s_r) / 2
    self.rect(self.c_dx / 2 - self.s_dx_i / 2, ty + self.s_dl_i, self.s_dx_i, self.s_dx_i, 1)
    self.pdf.text(self.c_dx / 2 - self.s_dx_i / 2+10, ty + self.s_dl_i+15, 'Colla')
    # self.l(self.s_dx_l / 2 - self.s_dx_i / 2, ty + self.s_dl_i, self.s_dx_l / 2 + self.s_dx_i / 2, ty + self.s_dl_i, 1)
    
    # Foto
    self.pdf.set_draw_color(255, 0 ,0)
    self.rect(self.f_x, self.f_y, self.f_dx, self.f_dy, 1)
    self.l(self.f_x,self.f_y, self.f_x + self.f_dx, self.f_y + self.f_dy, 1)
    self.l(self.f_x + self.f_dx ,self.f_y, self.f_x, self.f_y + self.f_dy, 1)
    self.pdf.set_draw_color(0, 0 ,0)
    
  def accessories(self):
    self.pdf.add_page()
    # Acc esterno
    self.l(self.s_dx_l / 2 - self.s_dx_c / 2, 0, self.s_dx_l / 2 + self.s_dx_c / 2, 0)
    self.l(self.s_dx_l / 2 + self.s_dx_c / 2, 0, self.s_dx_l, self.s_dl)
    self.l(self.s_dx_l, self.s_dl, 0, self.s_dl)
    self.l(0, self.s_dl, self.s_dx_l / 2 - self.s_dx_c / 2, 0)
    
    self.l(self.s_dx_l / 2 - self.s_dx_c / 2 - self.s_tx,  self.s_dy_i, self.s_dx_l / 2 + self.s_dx_c / 2 + self.s_tx, self.s_dy_i, 1)
    
    # Acc buco
    # self.arc(self.s_dx_l / 2, self.s_dy_i + (self.s_dl - self.s_dy_i - self.s_dl_i - self.s_dx_i * 2.5) / 2, self.s_dx_i * 1.5, self.s_dx_i * 1.5, 180, 360, 10)
    ty = (self.s_dl + self.s_dy_i - self.s_dl_i - self.s_dx_i + self.s_r) / 2
    
    self.arc(self.s_dx_l / 2, ty, self.s_r, self.s_r, 180, 360, 10)
    self.l(self.s_dx_l / 2 - self.s_r, ty, self.s_dx_l / 2 - self.s_dx_i / 2, ty)
    self.l(self.s_dx_l / 2 + self.s_r, ty, self.s_dx_l / 2 + self.s_dx_i / 2, ty)
    self.l(self.s_dx_l / 2 - self.s_dx_i / 2, ty, self.s_dx_l / 2 - self.s_dx_i / 2, ty + self.s_dl_i + self.s_dx_i)
    self.l(self.s_dx_l / 2 + self.s_dx_i / 2, ty, self.s_dx_l / 2 + self.s_dx_i / 2, ty + self.s_dl_i + self.s_dx_i)
    self.l(self.s_dx_l / 2 - self.s_dx_i / 2, ty + self.s_dl_i + self.s_dx_i, self.s_dx_l / 2 + self.s_dx_i / 2, ty + self.s_dl_i + self.s_dx_i)
    self.l(self.s_dx_l / 2 - self.s_dx_i / 2, ty + self.s_dl_i, self.s_dx_l / 2 + self.s_dx_i / 2, ty + self.s_dl_i, 1)
    
    
  def save(self):
    self.pdf.output('cornice.pdf', 'F')
    
  def rect(self, x, y, dx, dy, dashed = 0):
    self.l(x, y, x + dx, y, dashed)
    self.l(x + dx, y, x + dx, y + dy, dashed)
    self.l(x + dx, y + dy, x, y + dy, dashed)
    self.l(x, y + dy, x, y, dashed)
      
  def r_rect(self, x, y, dx, dy, radius = 0, dashed = 0):
    self.l(x + radius, y, x + dx - radius, y, dashed)
    if radius > 0:
      # self.l(x + dx - radius, y,x + dx, y + radius, dashed)
      self.arc(x + dx - radius, y + radius, radius, radius, -90, 0)
    self.l(x + dx, y + radius , x + dx, y + dy - radius, dashed)
    if radius > 0:
      # self.l(x + dx, y + dy - radius, x + dx - radius, y + dy, dashed)
      self.arc(x + dx - radius, y + dy - radius, radius, radius, 0, 90)
    self.l(x + dx - radius, y + dy, x + radius, y + dy, dashed)
    if radius > 0:
      # self.l(x + radius, y + dy, x, y + dy - radius, dashed)
      self.arc(x + radius, y + dy - radius, radius, radius, 90, 180)
    self.l(x, y + dy - radius, x, y + radius, dashed)
    if radius > 0:
      # self.l(x, y + radius, x + radius, y, dashed)
      self.arc(x + radius, y + radius, radius, radius, 180, 270)
      
  def l(self, x0, y0, x1, y1, dashed=0):
    if dashed:
      self.pdf.dashed_line(self.margin + x0, self.margin + y0, self.margin + x1 , self.margin + y1)
    else:
      self.pdf.line(self.margin + x0, self.margin + y0, self.margin + x1 , self.margin + y1)
      
  def arc(self, xc, yc, rx, ry, ab, ae, n=5):
    rab = ab * math.pi / 180.0
    rae = ae * math.pi / 180.0
    for i in range(n):
      a0 = rab + (rae - rab) * i / n
      a1 = rab + (rae - rab) * (i+1) / n
      self.l(xc + rx * math.cos(a0), yc + ry * math.sin(a0), xc + rx * math.cos(a1), yc + ry * math.sin(a1))
    
    
def usage():
    print('''
Usage:   cornice.py [ width [ height [ margin ] ] ]

    Draws a frame to cut and glue for a picture. With a stand.
    Front, back and stand each on a separate sheet.

         width:   width of picture in mm
                  default: 103
         height:  height of picture in mm
                  default: 153
         margin:  width of border in mm
                  default: 45
''')

if __name__ == '__main__':
  import sys
  width = 103
  height = 153
  margin = 45
  
  if len(sys.argv) > 1 and sys.argv:
      try:
          width = float(sys.argv[1])
      except:
          usage()
          exit(1)

  if len(sys.argv) > 2 and sys.argv:
      try:
          height = float(sys.argv[2])
      except:
          usage()
          exit(1)

  if len(sys.argv) > 3 and sys.argv:
      try:
          margin = float(sys.argv[3])
      except:
          usage()
          exit(1)

  c = cornice(width, height, margin)
  c.c_radius = 10
  c.front()
  c.back()
  c.accessories()
  c.save()
