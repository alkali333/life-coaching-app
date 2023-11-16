import re


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
