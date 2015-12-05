from font import Font

current_black_print = 0
current_white_print = 0


def sentence_within_word(sentence):
    return lambda arg: sentence[current_black_print % len(sentence)]


def sentence_within_char(sentence, word, font):
    word_map = [font.character_map[c] for c in word]
    replace_word_map = []
    sentence_index = 0
    for c in word_map:
        replace_c_map = []
        for row in c:
            replace_row_map = []
            for pixel in row:
                if pixel:
                    replace_row_map.append(sentence[sentence_index % len(sentence)])
                    sentence_index += 1
                else:
                    replace_row_map.append(' ')
            replace_c_map.append(replace_row_map)
        replace_word_map.append(replace_c_map)

    def internal_function(arg):
        row = arg['row']
        x = arg['x']
        char_index = arg['char_index']
        return replace_word_map[char_index][row][x]
    return internal_function


def default_black_func(arg):
    return arg['word'][arg['char_index']]


def default_white_func(arg):
    return ' '


def print_word(word, font, black_func=default_black_func, white_func=default_white_func):
    global current_black_print
    current_black_print = 0
    global current_white_print
    current_white_print = 0
    # Assemble the text row by row and print it
    for row in range(font.char_height):
        s = ''
        for char_index in range(len(word)):
            s += single_row_char(word, char_index, font, row, black_func=black_func, white_func=white_func)
        print(s.rstrip(' '))


def single_row_char(word, char_index, font, row, black_func=default_black_func, white_func=default_white_func):
    arg = locals()
    # Writes each character out of its own character if no black specified
    char = word[char_index]
    c_map = font.character_map[char]
    # Use spacing or the character data
    if char == ' ':
        return white_func(arg) * (font.word_spacing - font.letter_spacing)
    else:
        s = ''
        for x in range(font.character_widths[char]):
            arg['x'] = x
            if c_map[row][x]:
                s += black_func(arg)
                global current_black_print
                current_black_print += 1
            else:
                s += white_func(arg)
                global current_white_print
                current_white_print += 1
        return s + white_func(arg) * font.letter_spacing

if __name__ == '__main__':
    default_font = Font("letters5x5.png", monospaced=False)
    in_text = input("Input text: ")
    # Example displays:
    print("\n-- Default display --")
    print_word(in_text, default_font)
    print("\n-- Sentence within characters --")
    print_word(in_text, default_font, black_func=sentence_within_char('SENTENCEWITHINCHARACTERS', in_text, default_font))
    print("\n-- Sentence within the entire word(s) --")
    print_word(in_text, default_font, black_func=sentence_within_word('SENTENCEWITHINWORDS'))
    print("\n-- Negative --")
    print_word(in_text, default_font, black_func=lambda arg: ' ', white_func=lambda arg: 'X')