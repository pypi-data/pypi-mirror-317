import pytest
import os
from card_creator_utils.card_creator import CardCreator, BasicCardElement
from PIL import Image, ImageFont
import numpy as np


def test_card_creation_with_background_image():
    test_output_path = "tests/resources/test-background-image.png"
    card = CardCreator(background_image_path="tests/resources/image.webp")
    card.save(test_output_path)
    assert os.path.exists(test_output_path)
    assert _compare_images(
        test_output_path, "tests/references/test-background-image.png"
    )
    os.remove(test_output_path)


def test_card_creation_with_background_color():
    test_output_path = "tests/resources/test-background-color.png"
    card = CardCreator(background_color=(255, 200, 200))
    card.save(test_output_path)
    assert os.path.exists(test_output_path)
    assert _compare_images(
        test_output_path, "tests/references/test-background-color.png"
    )
    os.remove(test_output_path)


def test_card_creation_with_title():
    test_output_path = "tests/resources/test-title.png"
    card = CardCreator(background_color=(255, 200, 200))
    card.add_title(
        title_element=BasicCardElement(text="Test Title", background_color=None)
    )
    card.save(test_output_path)
    assert os.path.exists(test_output_path)
    assert _compare_images(test_output_path, "tests/references/test-title.png")
    os.remove(test_output_path)


def test_card_creation_with_effect_and_type():
    test_output_path = "tests/resources/test-effect-with-type.png"
    card = CardCreator(background_image_path="tests/resources/image.webp")
    card.add_effect(
        effect_element=BasicCardElement(
            text="Test Effect", background_color=(255, 255, 255, 200), stroke_width=0
        ),
        position="up",
        effect_type_element=BasicCardElement(
            background_color=(0, 255, 0),
            icon_path="tests/resources/infinite.png",
        ),
    )
    card.save(test_output_path)
    assert os.path.exists(test_output_path)
    assert _compare_images(
        test_output_path, "tests/references/test-effect-with-type.png"
    )
    os.remove(test_output_path)


def test_card_creation_with_effect():
    test_output_path = "tests/resources/test-effect.png"
    card = CardCreator(background_image_path="tests/resources/image.webp")
    card.add_effect(
        effect_element=BasicCardElement(
            text="Test Effect", background_color=(255, 255, 255, 200), stroke_width=0
        ),
        position="full",
    )
    card.save(test_output_path)
    assert os.path.exists(test_output_path)
    assert _compare_images(test_output_path, "tests/references/test-effect.png")
    os.remove(test_output_path)


def test_card_creation_with_stats():
    test_output_path = "tests/resources/test-stats.png"
    card = CardCreator(background_image_path="tests/resources/image.webp")
    card.add_stats(
        stats_element=BasicCardElement(
            text="22",
            background_color="red",
            font=ImageFont.truetype("tests/resources/Montserrat.ttf", 25),
        ),
        position="left",
    )
    card.save(test_output_path)
    assert os.path.exists(test_output_path)
    assert _compare_images(test_output_path, "tests/references/test-stats.png")
    os.remove(test_output_path)


def _compare_images(
    image1_path: str,
    image2_path: str,
) -> bool:
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)

    arr1 = np.array(image1.convert("RGB"))
    arr2 = np.array(image2.convert("RGB"))

    if arr1.shape != arr2.shape:
        image2 = image2.resize(image1.size)
        arr2 = np.array(image2.convert("RGB"))

    diff = np.abs(arr1 - arr2)
    difference_percentage = (np.count_nonzero(diff) / diff.size) * 100

    return difference_percentage <= 0.01
