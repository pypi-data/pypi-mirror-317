from dataclasses import dataclass
from typing import Literal, Optional
from PIL import Image, ImageDraw, ImageFont, ImageColor
from .utils import format_text_multiple_lines

CARD_WIDTH = 640
CARD_HEIGHT = 880
MARGIN_SIDE = 50

PositionEffect = Literal["up", "down", "full"]
PositionStats = Literal["left", "right"]


@dataclass
class BasicCardElement:
    text: Optional[str] = None
    color: Optional[any] = "black"
    background_color: Optional[any] = "white"
    font: Optional[any] = ImageFont.load_default()
    icon_path: Optional[str] = None
    stroke_width: Optional[int] = 1


class CardCreator:
    def __init__(
        self, background_image_path: str = None, background_color: ImageColor = None
    ):
        if background_image_path:
            try:
                self.background = Image.open(background_image_path).resize(
                    (CARD_WIDTH, CARD_HEIGHT)
                )
            except FileNotFoundError:
                raise FileNotFoundError(f"Image {background_image_path} not found")
        else:
            self.background = Image.new(
                "RGBA", (CARD_WIDTH, CARD_HEIGHT), background_color
            )

        self.draw = ImageDraw.Draw(self.background, "RGBA")

    def add_title(self, title_element: BasicCardElement):
        if title_element.background_color:
            overlay = Image.new("RGBA", (CARD_WIDTH, CARD_HEIGHT), (255, 255, 255, 0))
            overlay_draw = ImageDraw.Draw(overlay, "RGBA")
            overlay_draw.rounded_rectangle(
                (MARGIN_SIDE, MARGIN_SIDE, CARD_WIDTH - MARGIN_SIDE, 100),
                radius=10,
                fill=title_element.background_color,
                outline="grey",
            )
            self.background.paste(overlay, (0, 0), overlay)

        bbox = self.draw.textbbox((0, 0), title_element.text, font=title_element.font)
        title_width = bbox[2] - bbox[0]
        self.draw.text(
            ((CARD_WIDTH - title_width) / 2, 50),
            title_element.text,
            fill=title_element.color,
            font=title_element.font,
            stroke_width=title_element.stroke_width,
        )

    def add_category(self, category_element: BasicCardElement):
        bbox_type = self.draw.textbbox(
            (0, 0), category_element.text, font=category_element.font
        )
        type_width = bbox_type[2] - bbox_type[0]
        self.draw.rounded_rectangle(
            (
                (CARD_WIDTH - type_width - 20) / 2,
                110,
                (CARD_WIDTH + type_width + 20) / 2,
                145,
            ),
            radius=10,
            fill=category_element.background_color,
            outline="grey",
        )
        self.draw.text(
            ((CARD_WIDTH - type_width - 20) / 2 + 10, 115),
            category_element.text,
            fill=category_element.color,
            font=category_element.font,
            stroke_width=category_element.stroke_width,
        )

    def add_effect(
        self,
        effect_element: BasicCardElement,
        position: PositionEffect = "up",
        effect_type_element: Optional[BasicCardElement] = None,
    ):
        if position == "up":
            x_top, y_top = MARGIN_SIDE + (50 if effect_type_element else 0), 440
            x_bottom, y_bottom = CARD_WIDTH - MARGIN_SIDE, 440 + 180
        elif position == "down":
            x_top, y_top = (
                MARGIN_SIDE + (50 if effect_type_element else 0),
                440 + 180 + 30,
            )
            x_bottom, y_bottom = CARD_WIDTH - MARGIN_SIDE, CARD_HEIGHT - MARGIN_SIDE
        elif position == "full":
            x_top, y_top = (
                MARGIN_SIDE + (50 if effect_type_element else 0),
                440,
            )
            x_bottom, y_bottom = CARD_WIDTH - MARGIN_SIDE, CARD_HEIGHT - MARGIN_SIDE

        if effect_element.background_color:
            overlay = Image.new("RGBA", (CARD_WIDTH, CARD_HEIGHT), (255, 255, 255, 0))
            overlay_draw = ImageDraw.Draw(overlay, "RGBA")
            overlay_draw.rounded_rectangle(
                (x_top, y_top, x_bottom, y_bottom),
                radius=10,
                fill=effect_element.background_color,
                outline="grey",
            )
            self.background.paste(overlay, (0, 0), overlay)

        self.draw.text(
            (x_top + 20, y_top + 20),
            format_text_multiple_lines(effect_element.text),
            fill=effect_element.color,
            font=effect_element.font,
            stroke_width=effect_element.stroke_width,
            spacing=5,
        )
        if effect_type_element:
            self.draw.circle(
                (MARGIN_SIDE + 20, y_top + 90), 40, effect_type_element.background_color
            )
            if effect_type_element.icon_path:
                icon = (
                    Image.open(effect_type_element.icon_path)
                    .convert("RGBA")
                    .resize((34, 34))
                )
                self.background.paste(icon, (MARGIN_SIDE + 3, y_top + 73), icon)

    def add_stats(self, stats_element: BasicCardElement, position: PositionStats):
        if position == "left":
            x_cost = 70
            y_cost = MARGIN_SIDE + 25
        elif position == "right":
            x_cost = CARD_WIDTH - 70
            y_cost = MARGIN_SIDE + 25
        circle_rad = 40
        self.draw.circle((x_cost, y_cost), circle_rad, stats_element.background_color)
        bbox = self.draw.textbbox((0, 0), stats_element.text, font=stats_element.font)
        title_width = bbox[2] - bbox[0]
        title_height = bbox[3] - bbox[1]
        self.draw.text(
            (x_cost - title_width / 2, y_cost - title_height),
            stats_element.text,
            fill=stats_element.color,
            stroke_width=stats_element.stroke_width,
            font=stats_element.font,
        )

    def add_action(self, action):
        pass

    def save(self, output_path: str):
        self.background.save(output_path)
