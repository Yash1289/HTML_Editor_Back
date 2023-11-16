"""
Contains HTML table generator module
"""

from weasyprint.text.fonts import FontConfiguration
from weasyprint import HTML, CSS

from dominate import document
from dominate.tags import *
from tinycss2 import parse_declaration_list, serialize


GRAY_ROW_COLOR = '#d9d9d9'


def report_table(doc, df, column_widths,colored_rows,bold_rows, header_cell_color={},
                 bold_columns=[], cell_color=[], footers=[], class_='dataframe', multi_headers={}):
    # Create the table element
    with doc.add(table(border='1', cls=class_)):
        # Create the table header
        if multi_headers:
            # in case of multi-level headers
            with thead():
                # creating the first level:
                with tr():
                    for i, hval in enumerate(multi_headers):
                        if hval['levels'] == 1:
                            style_str = ""
                            if i in column_widths:
                                width = column_widths[i]
                                style_str += f"width:{width};"
                            if hval['color']:
                                clr = hval['color']
                                style_str += f"background-color:{clr}"
                            th(hval['name'], style=style_str, rowspan=2)
        
                        if hval['levels'] == 2:
                            # take the first level
                            upper = hval['level1']
                            style_str = ""
                            if i in column_widths:
                                width = column_widths[i]
                                style_str += f"width:{width};"
                            if upper['color']:
                                clr = upper['color']
                                style_str += f"background-color:{clr}"
                            th(upper['name'], style=style_str, colspan=len(hval['level2']))
                            
                            
                # creating the next level
                with tr():
                    for i, hval in enumerate(multi_headers):
                        if hval['levels'] == 2:
                            lower = hval['level2']
                            for cell in lower:
                                style_str = ""
                                if i in column_widths:
                                    width = column_widths[i]
                                    style_str += f"width:{width};"
                                if cell['color']:
                                    clr = cell['color']
                                    style_str += f"background-color:{clr}"
                                th(cell['name'], style=style_str)
        # regular headers
        else:
            with thead():
                with tr():
                    for i, col in enumerate(df.columns.tolist()):
                        style_str = ""
                        if i in column_widths:
                            width = column_widths[i]
                            style_str += f"width:{width};"
                        if i in header_cell_color:
                            clr = header_cell_color[i]
                            style_str += f"background-color:{clr}"
                        
                        th(col, style=style_str)

        # Create the table body
        with tbody():
            for i, row in df.iterrows():
                # Determine if the current row needs to be colored
                color_row = i in colored_rows
                bold_row = i in bold_rows

                # Create the table row
                with tr(style=f"background-color:{GRAY_ROW_COLOR};" if color_row else ""):
                    for col, value in enumerate(row.values):
                        style_cell = ""
                        if bold_row or (col in bold_columns):
                            style_cell += "font-weight:bold;"
                        if (i, col) in cell_color:
                            cclr = cell_color[(i, col)]
                            style_cell += f"background-color:{cclr};"
                        cellcont = div()
                        if '<br>' in str(value):
                             fv = value.split('<br>')
                             for br_sub in fv:
                                cellcont.add(br_sub)
                                cellcont.add(br())
                        else:
                             cellcont.add(value)
                        td(cellcont, style= style_cell)
        # adding captions
        if footers:
            for caption_text, alignment in footers:
                foo_cls = "footer-left"
                if alignment == 'right':
                    foo_cls = "footer-right"
                if alignment == 'center':
                    foo_cls = "footer-center"
                caption_ = caption(cls=foo_cls)
                with caption_:
                    caption_.add(caption_text)
                table.add(caption_)
                            
    return

def sub_header(text_,cls_='sub_header'):
    txt = text_
    h = h3(cls = cls_)
    with  h:
            h.add(txt)
    return h
 
def header(txt):
    h = h2(cls = "header_5")
    with  h:
            h.add(txt)
    return h

def header_2(txt):
    h = h3(cls = "header_6")
    with  h:
            h.add(txt)
    return h

def sub_header_left(text_):
    txt = text_
    h = h3(cls = 'sub_header_left')
    with  h:
            h.add(txt)
    return h

def header_2_left(txt):
    h = h3(cls = "header_6_left")
    with  h:
            h.add(txt)
    return h

def page_footer_left(txt):
    h = div(cls = 'left_footer')
    with h:
        h.add(txt)
    return h


def page_break():
    return div(style="page-break-before: always;")


def page_foot_head(top_left='', top_right='', bottom_left='', bottom_right=''):
    """
    Page footer and heading texts. Default is set to blank
    """
    from Utils.page_formatter_client import PAGE

    page_styles = CSS(string=PAGE.format(top_left=top_left, top_right=top_right,
                                         bottom_left=bottom_left, bottom_right=bottom_right))
    return page_styles
