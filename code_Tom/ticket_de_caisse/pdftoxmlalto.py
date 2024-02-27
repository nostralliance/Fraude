import os
from easyocr import Reader
from lxml import etree

def generate_alto_from_image(image_path, alto_path):
    # Lecture du texte à partir de l'image
    reader = Reader(['fr'], gpu=False)  # Changer 'fr' avec la langue appropriée
    result = reader.readtext(image_path)

    # Création de l'élément racine du document ALTO
    alto = etree.Element("{http://www.loc.gov/standards/alto/ns-v4#}alto")

    # Création de l'élément Description
    description = etree.SubElement(alto, "Description")
    description.set("MeasurementUnit", "pixel")

    # Création de l'élément Layout
    layout = etree.SubElement(alto, "Layout")

    # Création de l'élément Page
    page = etree.SubElement(layout, "Page")
    page.set("ID", "page1")
    page.set("PHYSICAL_IMG_NR", "1")

    # Création de l'élément PrintSpace
    print_space = etree.SubElement(page, "PrintSpace")

    # Création des éléments TextBlock, TextLine et String pour chaque texte extrait
    for idx, (bbox, text, _) in enumerate(result):
        text_block = etree.SubElement(print_space, "TextBlock")
        text_block.set("ID", f"block{idx+1}")
        text_block.set("HPOS", str(int(bbox[0][0])))
        text_block.set("VPOS", str(int(bbox[0][1])))
        text_block.set("WIDTH", str(int(bbox[2][0] - bbox[0][0])))
        text_block.set("HEIGHT", str(int(bbox[1][1] - bbox[0][1])))

        text_line = etree.SubElement(text_block, "TextLine")
        text_line.set("ID", f"line{idx+1}")
        text_line.set("HPOS", str(int(bbox[0][0])))
        text_line.set("VPOS", str(int(bbox[0][1])))
        text_line.set("WIDTH", str(int(bbox[2][0] - bbox[0][0])))
        text_line.set("HEIGHT", str(int(bbox[1][1] - bbox[0][1])))

        string = etree.SubElement(text_line, "String")
        string.set("CONTENT", text)
        string.set("HPOS", str(int(bbox[0][0])))
        string.set("VPOS", str(int(bbox[0][1])))
        string.set("WIDTH", str(int(bbox[2][0] - bbox[0][0])))
        string.set("HEIGHT", str(int(bbox[1][1] - bbox[0][1])))

    # Génération du fichier XML
    xml_string = etree.tostring(alto, pretty_print=True, encoding="utf-8", xml_declaration=True)

    # Écriture du fichier
    with open(alto_path, "wb") as f:
        f.write(xml_string)

    print("Fichier ALTO généré avec succès.")

# Chemin de l'image d'entrée
image_file = r"C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\ticket_de_caisse\test2.jpg"

# Chemin du fichier ALTO de sortie
alto_file = r"C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\ticket_de_caisse\output.alto"

# Générer le fichier ALTO à partir de l'image OCR
generate_alto_from_image(image_file, alto_file)
