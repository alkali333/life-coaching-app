import re
import os
import streamlit as st


def extract_dictionary(input_string):
    # This regex pattern matches a dictionary that starts with '{' and ends with '}'
    # It uses non-greedy matching to capture the shortest string that fits the pattern
    pattern = r"{.*?}"
    match = re.search(pattern, input_string, re.DOTALL)

    if match:
        # Extract the dictionary string from the match
        dict_string = match.group(0)
        return dict_string
    else:
        return None


def display_image_if_exists(image_path, caption=None):
    if os.path.exists(image_path):
        st.image(image_path, caption=caption, use_column_width=True)
        return True
    else:
        return False


def find_mp3_file(input_string):
    # Convert the string to lowercase and replace spaces with underscores
    formatted_string = input_string.lower().replace(" ", "_")

    # Append ".mp3" to the formatted string
    file_name = formatted_string + ".mp3"

    # Construct the file path
    file_path = os.path.join("./music", file_name)

    # Check if the file exists
    if os.path.exists(file_path):
        return file_path
    else:
        return False
