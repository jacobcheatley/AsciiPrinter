from font import Font


def print_word(word, font, black=None, white=' '):
    # Assemble the text row by row and print it
    for row in range(font.char_height):
        s = ''
        for char in word:
            s += single_row_char(char, font, row, black=black, white=white)
        print(s.rstrip(' '))


def single_row_char(char, font, row, black=None, white=' '):
    # Writes each character out of its own character if no black specified
    if black is None:
        black = char
    c_map = font.character_map[char]
    # Use spacing or the character data
    if char == ' ':
        return white * (font.word_spacing - font.letter_spacing)
    else:
        s = ''
        for x in range(font.character_widths[char]):
            s += black if c_map[row][x] else white
        return s + white * font.letter_spacing


if __name__ == "__main__":
    default_font = Font("letters5x5.png", monospaced=False)
    print_word(input("Input text: "), default_font)
