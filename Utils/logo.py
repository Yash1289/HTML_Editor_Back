from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
import os
from PIL import Image
import asyncio

LOGO_FILE = "Dhruva Logo.png"
LOGO_PATH = os.path.join(os.path.dirname(__file__), "..", LOGO_FILE)


x_start = (10) * mm
y_start = (-84.6) * mm
logo_width = (24) * mm

async def add_logo_to_pdf(input_file,output_file,img_file,x_start, y_start,logo_width):
 
    packet = '_tmp.pdf' 
    # read the existing PDF 

    existing_pdf = PdfReader(open(input_file, "rb")) 
    output = PdfWriter()
    can = canvas.Canvas(packet, pagesize=A4)
    
    for i in range(1, len(existing_pdf.pages) + 1):
#         img_file.onload = function() {can.drawImage(img_file, x_start, y_start, width=logo_width, preserveAspectRatio=True, mask='auto');}
        can.drawImage(LOGO_PATH, x_start, y_start, width=logo_width, preserveAspectRatio=True, mask='auto')
        can.showPage()
    can.save()
 
    new_pdf = PdfReader(packet)
   
    for i in range(len(existing_pdf.pages)):
        page = existing_pdf.pages[i]
        page.merge_page(new_pdf.pages[i])
        output.add_page(page)
 
    outputStream = open(output_file, "wb")
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, output.write, outputStream)
    outputStream.close()
    os.remove(packet)