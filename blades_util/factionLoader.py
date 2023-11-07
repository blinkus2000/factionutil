import json
import re

def parseToJSON(src, dest):
    # Regular expression to match the pattern "name (rating): description"
    # The description can span multiple sentences, so we capture everything up to the final period.
    pattern = re.compile(r'(.+?) \((.+?)\): (.*\.)')

    # Read the source file
    with open(src, 'r', encoding='utf-8') as file:
        content = file.read()

    # Find all matches in the file content
    matches = pattern.findall(content)

    # Parse the matches into a list of dictionaries
    data = [
        {'name': name.strip(), 'rating': rating.strip(), 'description': description.strip()}
        for name, rating, description in matches
    ]

    # Write the data to the destination JSON file
    with open(dest, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)





# Example usage:
# parseToJSON('faction.txt', 'factions.json')
