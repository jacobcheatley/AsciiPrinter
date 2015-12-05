from PIL import Image


class Font:
    def __init__(self, image_path, char_width=5, char_height=5, monospaced=True, letter_spacing=2, word_spacing=4):
        self.image_path = image_path
        self.char_width = char_width
        self.char_height = char_height
        self.monospaced = monospaced
        self.letter_spacing = letter_spacing
        self.word_spacing = word_spacing
        self.character_widths = dict()
        self.character_map = dict()
        self.set_up_font()

    def set_up_font(self):
        image = Image.open(self.image_path)
        image_width, image_height = image.size
        images_per_row = image_width / self.char_width

        # Get image data
        pixels = list(image.getdata())
        image_data = []
        for y in range(image_height):
            row_data = [not bool(x[0]) for x in pixels[y * image_width:(y + 1) * image_width]]
            image_data.append(row_data)

        # Set up each character
        for char_index in range(0, 96):
            character = chr(char_index + 32)

            # Get character data from image
            x_start = int((char_index * self.char_width) % image_width)
            y_start = int(char_index // images_per_row * self.char_height)
            char_data = []
            for y in range(y_start, y_start + self.char_height):
                row_data = image_data[y][x_start: x_start + self.char_width]
                char_data.append(row_data)

            # Reduce character width if less than full size and proportional font
            if not self.monospaced and char_index != 0:
                x = self.char_width - 1
                to_remove = 0
                while x >= 0:
                    all_white = True
                    for y in range(0, self.char_height):
                        if char_data[y][x]:
                            all_white = False
                            break
                    if all_white:
                        to_remove += 1
                    x -= 1

                self.character_widths[character] = self.char_width - to_remove
            else:
                self.character_widths[character] = self.char_width

            self.character_map[character] = char_data
