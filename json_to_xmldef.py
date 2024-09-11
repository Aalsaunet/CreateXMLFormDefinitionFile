import json
import xml.etree.ElementTree as ET
import sys
import os

def json_to_xml(json_obj, line_padding=""):
    """Converts a JSON object to an XML string."""
    result_list = []

    # Process dictionary items
    if isinstance(json_obj, dict):
        for tag_name in json_obj:
            sub_obj = json_obj[tag_name]
            result_list.append(f"{line_padding}<{tag_name}>")
            result_list.append(json_to_xml(sub_obj, line_padding + "\t"))
            result_list.append(f"{line_padding}</{tag_name}>")

    # Process list items
    elif isinstance(json_obj, list):
        for sub_elem in json_obj:
            result_list.append(json_to_xml(sub_elem, line_padding))

    # Process other data types
    else:
        result_list.append(f"{line_padding}{json_obj}")

    return "\n".join(result_list)


def convert_json_file_to_xml(json_file_path):
    """Converts a JSON file to an XML file with the same name (except extension)."""
    # Check if the file exists
    if not os.path.exists(json_file_path):
        print(f"File '{json_file_path}' does not exist.")
        return

    # Load JSON data from the file
    with open(json_file_path, 'r') as json_file:
        try:
            json_data = json.load(json_file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return

    # Convert JSON to XML
    xml_data = json_to_xml(json_data)

    # Generate the XML file path
    xml_file_path = os.path.splitext(json_file_path)[0] + '.xml'

    # Save the XML data to a new file
    with open(xml_file_path, 'w') as xml_file:
        xml_file.write(f"<?xml version=\"1.0\" ?>\n")
        xml_file.write("<root>\n")  # Add a root element for the XML structure
        xml_file.write(xml_data)
        xml_file.write("\n</root>")

    print(f"XML file created successfully: {xml_file_path}")


if __name__ == "__main__":
    # Check if a file path is passed as an argument
    if len(sys.argv) != 2:
        print("Usage: python json_to_xml.py <json-file-path>")
    else:
        json_file_path = sys.argv[1]
        convert_json_file_to_xml(json_file_path)