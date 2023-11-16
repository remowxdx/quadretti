# Quadretti
Create a PDF with squared sheets.

This is a command line tool written in Python to create PDF documents with
a grid of squares.

It uses the cairo library to build the PDF. If you don't have `pycairo` already installed,
type in your terminal:
```sh
    pip install pycairo
```
Or better, first create a virtual environment.

There are some command line switches to control the number of the pages, the size of the squares,
the width of the margin, and other options. To see the help, type:
```sh
    python3 quadretti.py --help
```



There is also an "elementary" font for writing some letters on the pages.

For example:
```sh
    python3 quadretti.py -p 10 -m 15 -o 10 -s 4 -w 'Hello, world!' hello.pdf
```
will create a 10 pages file named `hello.pdf` with 4mm squares, a left(right)
margin of 25mm and a right(left) margin of 15mm on odd(even) pages and
the text "Hello, world!".
