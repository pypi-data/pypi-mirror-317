from card_creator_utils.prepare_print import prepare_pdf_from_cards_folder
import os


def test_prepare_print():
    output_path = "tests/output/cards.pdf"
    prepare_pdf_from_cards_folder(
        card_images_folder="tests/resources/card_folder",
        output_pdf=output_path,
        nb_occurences=7,
    )
    assert os.path.exists(output_path)
    os.remove(output_path)
