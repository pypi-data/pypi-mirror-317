def to_camel_case(text:str):
    # Split the string by spaces, underscores, or hyphens
    words = text.replace("-", " ").replace("_", " ").split()
    # Capitalize the first letter of each word except the first one
    # and join them together
    return words[0].lower() + ''.join(word.capitalize() for word in words[1:])


