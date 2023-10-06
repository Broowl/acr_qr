import base64
import os
from pathlib import Path
from urllib.parse import quote
import qrcode
import qrcode.image.svg
import reportlab.pdfgen.canvas
import reportlab.graphics.renderPDF
import svglib.svglib



def remove_existing_file(name: str) -> None:
    if os.path.exists(name):
        os.remove(name)


def create_parent_directories(file_name: str) -> None:
    dir_name = os.path.dirname(file_name)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def save_svg(data: str, svg_file_name: str) -> None:
    remove_existing_file(svg_file_name)
    qr = qrcode.QRCode(border=0, image_factory=qrcode.image.svg.SvgPathImage)
    qr.add_data(data)
    img = qr.make_image()
    img.save(svg_file_name)


def save_png(data: str, png_file_name: str) -> None:
    remove_existing_file(png_file_name)
    img = qrcode.make(data)
    img.save(png_file_name)


def save_pdf(svg_file_name: str, pdf_file_name: str, flyer_file_name: Path | None) -> None:
    border_size = 10
    remove_existing_file(pdf_file_name)
    canvas = reportlab.pdfgen.canvas.Canvas(pdf_file_name)
    qr_drawing = svglib.svglib.svg2rlg(svg_file_name)
    scale = 298/(qr_drawing.height + 2 * border_size)  # scale to width of A5
    qr_drawing_size = qr_drawing.height * scale
    qr_drawing.scale(scale, scale)
    reportlab.graphics.renderPDF.draw(
        qr_drawing, canvas=canvas, x=border_size, y=border_size)
    if flyer_file_name is not None:
        reader = reportlab.pdfgen.canvas.ImageReader(flyer_file_name)
        flyer_size = reader.getSize()
        scaled_flyer_size = [qr_drawing_size, flyer_size[1]
                             * (qr_drawing_size / flyer_size[0])]
        canvas.drawImage(reader, x=border_size, y=qr_drawing_size + 2 * border_size,
                         width=scaled_flyer_size[0], height=scaled_flyer_size[1])
        canvas.setPageSize(
            [qr_drawing_size + 2 * border_size,  qr_drawing_size + 3 * border_size + scaled_flyer_size[1]])
    else:
        canvas.setPageSize(
            [qr_drawing_size + 2 * border_size,  qr_drawing_size + 2 * border_size])
    canvas.save()


def save_ticket(data: str, file_name: str, flyer_file_name: Path | None) -> None:
    create_parent_directories(file_name)
    svg_file_name = f"{file_name}.svg"
    save_svg(data, svg_file_name)
    pdf_file_name = f"{file_name}.pdf"
    save_pdf(svg_file_name, pdf_file_name, flyer_file_name)
    remove_existing_file(svg_file_name)


def save_public_key(data: str, file_name: str) -> None:
    create_parent_directories(file_name)
    png_file_name = f"{file_name}.png"
    save_png(data, png_file_name)


def add_signature_to_message(message: str, signature: bytes) -> str:
    decoded_signature = quote(base64.b64encode(signature))
    return f"{message}__{decoded_signature}"
