from PIL import Image, ImageDraw, ImageFont
import textwrap


def Images_for_Chunks(text, chunk_number, image_path):
    img = Image.open(image_path)
    draw_instance = ImageDraw.Draw(img)

    text_box_position = (10, img.height - 150, img.width - 10, img.height - 10)
    text_position = (25, img.height - 135)

    draw_instance.rectangle(text_box_position, fill="white", outline="black", width=8)
    chunk_size = 45
    words = text.split()
    text_chunks = [words[i : i + chunk_size] for i in range(0, len(words), chunk_size)]

    # Add text to image for each chunk
    myFont = ImageFont.truetype("Cabal-w5j3.ttf", 24)
    for index, chunk in enumerate(text_chunks, start=1):
        # Create a new image for each chunk
        chunk_img = img.copy()

        chunk_draw = ImageDraw.Draw(chunk_img)

        chunk_text = " ".join(chunk)
        wrapped_text = textwrap.fill(chunk_text, width=70)
        chunk_draw.text(text_position, wrapped_text, font=myFont, fill="black")
        chunk_img.save(f"VN_Images/out_{chunk_number}_{index}.png")
