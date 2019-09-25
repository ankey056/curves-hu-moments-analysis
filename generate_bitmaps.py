#!/usr/bin/env python2

from xml.dom.minidom import parse
import re # , os
from lib.ink_shell import InkShell
from sys import argv

source = argv[1]
output_path =  argv[2]
ink_proc = InkShell()

vb_re = re.compile("\s+")
def get_svg_viewboxy (svg):
    vbs = svg.firstChild.getAttribute("viewBox")
    return float(vb_re.split(vbs)[3])


def find_figure_node (nodes):
    return next(node for node in nodes
                if not(node.nodeName in ["text", "#text"]))


ws_list = [30, 70, 100, 120, 150, 180, 210, 250, 300, 350, 400, 450, 500]
# ws_list = [ 50, 500]
# ws_list = [300]

def mk_raster (svgfile, output_path, id, png, width, vby):
    ink_proc.export_svg_object_in_png(svgfile, vby, output_path + "/" + png,
                                      id, width=2*width,
                                      bg='#ffffff',
                                      expansion=3.0)


sample_name_splitter_re = re.compile('\s*\+\s*')
special_name_re = re.compile("\s*\$exp\s*:\s*(.+)")

def determine_png_name (mreg, width):
    s = mreg.group(1).strip()
    name_parts = sample_name_splitter_re.split(s)
    if len(name_parts) > 1:
        ext = "."
    else:
        ext = ""
    fin = ext + '{0}.png'.format(str(width).zfill(4))
    return name_parts[0] + '.' + '_'.join(name_parts[1:]) + fin


def generate_png_files (svgfile, output_dir):
    svg = parse(svgfile)
    vby = get_svg_viewboxy(svg)
    text_elements = svg.getElementsByTagName("text")
    for text_element in text_elements:
        x = text_element.firstChild
        if x.hasChildNodes():
            t = x.firstChild.nodeValue
            m = special_name_re.match(t)
            if m:
                figure = find_figure_node(text_element.parentNode.childNodes)
                for w in ws_list:
                    mk_raster(svgfile, output_dir, figure.getAttribute("id"),
                              determine_png_name(m, w),
                              w, vby)



generate_png_files(source, output_path)

ink_proc.close()

