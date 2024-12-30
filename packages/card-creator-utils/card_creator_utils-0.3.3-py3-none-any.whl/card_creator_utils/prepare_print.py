from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image
import os


def mm_to_points(mm):
    """Convertit les millimètres en points (1 mm = 2.83465 points)"""
    return mm * 2.83465


page_width, page_height = A4
margin_mm = 8
margin = mm_to_points(margin_mm)


def prepare_pdf_from_cards_folder(
    card_images_folder,
    output_pdf,
    card_width_mm=59,
    card_height_mm=86,
    nb_occurences=1,
):
    card_width = mm_to_points(card_width_mm)
    card_height = mm_to_points(card_height_mm)
    margin = mm_to_points(margin_mm)

    images = [
        f
        for f in os.listdir(card_images_folder)
        if f.lower().endswith(".png") or f.lower().endswith(".jpg") or f.lower().endswith(".jpeg") or f.lower().endswith(".heic")
    ]
    if not images:
        print("Aucune image trouvée dans le dossier spécifié.")
        return

    # Initialiser le PDF
    pdf = canvas.Canvas(output_pdf, pagesize=A4)

    # Position initiale
    x, y = margin, page_height - card_height - margin

    for image_file in images:
        image_path = os.path.join(card_images_folder, image_file)

        with Image.open(image_path) as img:
            img_width, img_height = img.size
            if img_width != mm_to_points(card_width_mm) or img_height != mm_to_points(card_height_mm):
                print(f"Image {image_file} redimensionnée")
                img = img.resize((int(card_width) * 5, int(card_height) * 5))
                img.save(image_path)

        for _ in range(nb_occurences):
            print(f"Ajout de l'image {image_file} à la position {x}, {y}")
            x, y = add_image_to_pdf(pdf, image_path, x, y, card_width, card_height)

    pdf.save()
    print(f"PDF généré avec succès : {output_pdf}")


def add_image_to_pdf(
    pdf: canvas.Canvas,
    image_path: str,
    x: float,
    y: float,
    card_width: float,
    card_height: float,
):

    pdf.drawImage(image_path, x, y, width=card_width, height=card_height)

    x += card_width + margin
    if x + card_width + margin > page_width:  # Si la prochaine carte dépasse la largeur de la page
        x = margin
        y -= card_height + margin

    # Si la prochaine carte dépasse la hauteur de la page
    if y < margin:
        pdf.showPage()  # Créer une nouvelle page
        x, y = margin, page_height - card_height - margin

    return x, y
