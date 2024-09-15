import os
import re
from PIL import Image, ImageDraw, ImageFont
import textwrap


def get_unique_filename(filename):
    """
    Generate a unique filename by appending a number if a file with the same name already exists.
    """
    if not os.path.exists(filename):
        return filename
    
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = f"{base}_{counter}{ext}"
    
    while os.path.exists(new_filename):
        counter += 1
        new_filename = f"{base}_{counter}{ext}"
    
    return new_filename


def save_image_with_unique_name(image, path):
    unique_path = get_unique_filename(path)
    image.save(unique_path)
    print(f"Image saved as: {unique_path}")
    
def find_text_in_answer(text):
    print("Full caption:", text)
    text = text.split("Caption:")[1]
    text = text.replace("\n", "")
    text = text.replace("model", "")
    # Remove everything that lookslike <>
    text = re.sub(r'<[^>]*>', '', text)
    
    # Remove non-alphanumeric characters (keeping spaces)
    text = re.sub(r'[^a-zA-Z0-9\?\!\s]', '', text)
    print("Filtered caption:", text)
    if text:
        return text
    else:
        return "Me when I couldn't parse the model's answer but I still want you to smile :)"
    
    
def draw_text(draw, text, position, font, max_width, outline_color="black", text_color="white", outline_width=2):
    """
    Draw text on the image with an outline, splitting it into lines if necessary and returning the total height used by the text.
    The text is horizontally centered in the specified max_width.
    """
    print("Adding the caption on the image...")

    # Split the text into multiple lines based on the max width
    lines = []
    words = text.split()
    line = ''
    for word in words:
        test_line = f'{line} {word}'.strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]  # Width of the text
        if width <= max_width:
            line = test_line
        else:
            if line:  # Avoid appending empty lines
                lines.append(line)
            line = word
    if line:
        lines.append(line)

    y = position[1]

    # Draw the text with an outline (black) first, centered horizontally
    for line in lines:
        # Calculate the width of the line and adjust the x position to center it
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x = (max_width - line_width) // 2 + position[0]

        # Draw the outline by drawing the text multiple times around the original position
        for offset_x in [-outline_width, 0, outline_width]:
            for offset_y in [-outline_width, 0, outline_width]:
                if offset_x != 0 or offset_y != 0:
                    draw.text((x + offset_x, y + offset_y), line, font=font, fill=outline_color)

        # Draw the main text (white) on top of the outline
        draw.text((x, y), line, font=font, fill=text_color)
        y += bbox[3] - bbox[1]  # Update y position based on line height

    return y - position[1]  # Return the total height used by the text

def calculate_text_height(caption, font, max_width):
    """
    Calculate the height of the text when drawn, given the caption, font, and maximum width.
    """
    image = Image.new('RGB', (max_width, 1))
    draw = ImageDraw.Draw(image)
    return draw_text(draw, caption, (0, 0), font, max_width)

def add_caption(image_path, caption, output_path, top_margin=10, bottom_margin=10, max_caption_length=10, min_distance_from_bottom_mm=10):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    width, height = image.size

    # Convert mm to pixels (assuming 96 DPI)
    dpi = 96
    min_distance_from_bottom_px = min_distance_from_bottom_mm * dpi / 25.4

    # Split the caption into two parts if it is too long
    if len(caption.split()) > max_caption_length:
        font_size=20
        total_len = len(caption.split())
        mid = int(total_len / 2)

        top_caption = caption.split()[:mid]
        bottom_caption = caption.split()[mid:]

        top_caption = " ".join(top_caption)
        bottom_caption = " ".join(bottom_caption)
    else:
        top_caption = ""
        bottom_caption = caption
        font_size=30

    # Load a font
    font = ImageFont.truetype(r"fonts/Anton/Anton-Regular.ttf", font_size)

    # Top caption
    top_caption_position = (width // 10, top_margin)
    draw_text(draw, top_caption, top_caption_position, font, width - 2 * (width // 10))

    # Bottom caption
    if bottom_caption:  # Draw bottom caption only if it's not empty
        # Calculate the height of the bottom caption
        bottom_caption_height = calculate_text_height(bottom_caption, font, width - 2 * (width // 10))
        bottom_caption_position = (width // 10, height - min_distance_from_bottom_px - bottom_caption_height)
        draw_text(draw, bottom_caption, bottom_caption_position, font, width - 2 * (width // 10))

    save_image_with_unique_name(image, output_path)
    return image

    
def overlay_caption(text, img_path, output_dir):
  img_name = img_path.split("/")[-1]
  text = find_text_in_answer(text)
  text = text.strip(".")
  image = add_caption(img_path, text, output_dir+"/"+img_name)
  return image
