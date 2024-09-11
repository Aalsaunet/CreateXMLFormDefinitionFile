# CreateXMLFormDefinitionFile
This repo is for the script file called json2xml_definition.py. This script takes in a json file and schema id as input parameters and produce an xml definition file that is used for an undisclosed backend system.

## Example input:
```
{
    "appId": "stipendsoknad-fgt",
    "formId": "form",
    "pages": [
        {
            "pageId": "Side2b",
            "sortOrder": 2,
            "components": [
                {
                    "id": "form1-page2b-question1",
                    "type": "RadioButtons",
                    "dataModelBindings": {
                        "simpleBinding": "Q9"
                    },
                    "texts": [
                        {
                            "id": "ssfgt.page2b.q1.title",
                            "type": "title",
                            "text": [
                                {
                                    "language": "nb",
                                    "value": "Jeg ettersender dokumentasjon for"
                                }
                            ]
                        }
                    ],
                    "options": [
                        {
                            "value": 1,
                            "label": [
                                {
                                    "language": "nb",
                                    "value": "Eksamensavgifter VGS"
                                }
                            ]
                        },
                        {
                            "value": 2,
                            "label": [
                                {
                                    "language": "nb",
                                    "value": "Annet"
                                }
                            ]
                        }
                    ],
                    "sortOrder": 2
                }
            ]
        }
    ]
}
```

## Example output: 
```
<?xml version="1.0" ?>
<root>
  <questions>
    <question schemaid="SELK" qid="Q9" qtype="500" pageorder="Side2b" qorder="2">
      <questiontext languageid="nb" qtext="Jeg ettersender dokumentasjon for"/>
      <options>
        <option>
          <label>Eksamensavgifter VGS</label>
          <value>1</value>
        </option>
        <option>
          <label>Annet</label>
          <value>2</value>
        </option>
      </options>
    </question>
  </questions>
</root>
```