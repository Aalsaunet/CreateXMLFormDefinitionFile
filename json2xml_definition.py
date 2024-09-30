import json
import os
import sys
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom

# List of components to exclude because they do not represent questions 
EXCLUDED_COMPONENTS = {"Header", "Image", "NavigationButtons", "Paragraph", "Button", ""}

def json_to_xml(json_obj, schemaid):
    """Converts a JSON object to the desired XML format, excluding certain qtypes and components without simpleBinding."""
    root = Element("altinnform", {
        "schemaid": str(schemaid),
        "name": json_obj.get("appId")
    })

    questions = SubElement(root, "questions")
    pcount = 1; qcount = 1

    for page in json_obj.get("pages", []):
        pagetitle = ""
        for component in page.get("components", []):
            ctype = component.get("type", "")
            
            # Skip if the ctype is in the exclusion list
            if ctype in EXCLUDED_COMPONENTS:
                if str(ctype) == "Header" and pagetitle == "": # Store for later component attribute usage?
                    pagetitle = component.get("texts", {})[0].get("text", {})[0].get("value", "")
                continue

            # Get the qid from dataModelBindings.simpleBinding
            data_model_bindings = component.get("dataModelBindings", {})
            qid = data_model_bindings.get("simpleBinding", None)

            # If qid (i.e a simpleBinding) is not available, skip this component
            if not qid:
                continue

            # Create the main question element
            question = SubElement(questions, "question", {
                "qid": str(qid),
                "qtype": str(ctype),
                "pageorder": str(pcount),
                "pagetitle": str(pagetitle),
                "qorder": str(qcount)
            })

            qcount += 1

            # Add the question text
            for text_item in component.get("texts", []):
                if text_item.get("type") == "title":
                    for text in text_item.get("text", []):
                        questiontext = SubElement(question, "questiontext", {
                            "languageid": text.get("language", "")
                        })
                        questiontext.set("qtext", text.get("value", ""))

            # Add the options if present
            if "options" in component:
                options = SubElement(question, "options")
                for option in component["options"]:
                    option_element = SubElement(options, "option")
                    for label in option.get("label", []):
                        label_element = SubElement(option_element, "label")
                        label_element.text = label.get("value", "")
                    value_element = SubElement(option_element, "value")
                    value_element.text = str(option.get("value", ""))
        pcount += 1

    return root


def pretty_print_xml(xml_element):
    """Pretty prints an XML element."""
    raw_string = tostring(xml_element, encoding='utf-8', method='xml', xml_declaration=True)
    dom = xml.dom.minidom.parseString(raw_string)
    return dom.toprettyxml(indent="  ")


def convert_json_file_to_xml(json_file_path, schemaid):
    """Converts the JSON file to the specified XML format, excluding certain qtypes and components without simpleBinding."""
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
    xml_tree = json_to_xml(json_data, schemaid)

    # Generate the XML file path
    xml_file_path = os.path.splitext(json_file_path)[0] + '.xml'

    # Pretty print the XML tree and save it
    with open(xml_file_path, 'w', encoding='utf-8') as xml_file:
        pretty_xml_as_string = pretty_print_xml(xml_tree)
        xml_file.write(pretty_xml_as_string)

    print(f"XML file created successfully: {xml_file_path}")


if __name__ == "__main__":
    # Check if the correct arguments are passed
    if len(sys.argv) != 3:
        print("Usage: python json_to_xml.py <json-file-path> <schemaid>")
    else:
        json_file_path = sys.argv[1]
        schemaid = sys.argv[2]
        convert_json_file_to_xml(json_file_path, schemaid)