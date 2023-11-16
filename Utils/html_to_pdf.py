from Utils.logo import *
from Utils.report import *
import os
from werkzeug.utils import secure_filename

def PDFPrint(html_path, top_left = "", top_right = "", bottom_left = ""):

    with open(html_path, 'r', encoding='utf-8') as fh:
        html_string = fh.read()

    CSS_FILE = "css/report_br_client.css"
    CSS_PATH = os.path.join(os.path.dirname(__file__), "..", CSS_FILE)

    pdf_path = html_path.replace(".html", ".pdf")
    
    #pdf_file_path = f"""[Madhya Pradesh] AC CATI R1 | {title['chapter_title']} - Summary Report.pdf""" 
    font_config = FontConfiguration()

    # page headers and footers
    page_styles = page_foot_head(top_left = "", top_right='गोपनीय',
                                 bottom_left = "")

    HTML(string=html_string).write_pdf(pdf_path,stylesheets=[CSS_PATH, page_styles],
                                       presentational_hints= True, font_config=font_config)
    
    add_logo_to_pdf(pdf_path, pdf_path, LOGO_PATH,x_start, y_start,logo_width)
