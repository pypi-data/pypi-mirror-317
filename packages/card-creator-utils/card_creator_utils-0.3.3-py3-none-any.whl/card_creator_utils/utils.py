def format_text_multiple_lines(text: str, max_letters_per_line: int = 38) -> str:
    new_text = ""
    current_line_size = 0
    for word in text.split(" "):
        if current_line_size + len(word) > max_letters_per_line:
            new_text += "\n"
            current_line_size = 0
        new_text += word + " "
        current_line_size += len(word) + 1
    return new_text
