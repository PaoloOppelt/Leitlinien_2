# Importing necessary modules and classes
import json
import param  # For defining parameters in classes
from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder

# Document class definition
class Document(BaseModel):
    """Interface for interacting with a document."""
    page_content: str
    metadata: dict = Field(default_factory=dict)

    def to_json(self):
        return self.model_dump_json(by_alias=True, exclude_unset=True)

# cbfs class definition
class cbfs(param.Parameterized):
    chat_history = param.List([])
    count = param.List([])

    def __init__(self, **params):
        super(cbfs, self).__init__(**params)
        # self.qa = Init_model() # Commented out since we're not using the model for test

    def load_model(self, Database):
        # For testing, this can be left empty or modified as needed
        pass

    def convchain(self, query):
        # Directly using a test result instead of processing the query
        result_test = {
            'question': query,
            'chat_history': self.chat_history,
            'answer': 'Test answer to current question',
            # Including mock data for source documents
            'source_documents': [
                Document(page_content='nation der Versorgung. Dazu erscheint die nachfolgende Auftei-\nlung der Aufgaben sinnvoll:\nGrundsätzlich können Basisuntersuchungen (siehe Kapitel\nDiagnostik) vom Hausarzt durchgeführt werden. Die zur endgültigenDiagnosesicherung notwendigen endoskopischen Untersuchungenwerden meist von Gastroenterologen durchgeführt. Die Diagnose-mitteilung erfolgt durch den Hausarzt und/oder Gastroenterologen.\nDie Basismaßnahme bei jeder Erstmaßnahme ist die Patienten-\nedukation (siehe Kapitel 4) durch Hausarzt und/oder Gastroente-\nrologen. Wesentliche Informationen dabei sind:▪Die Beschwerden sind „echt “(nicht „eingebildet “). Es sind\norganische Veränderungen nachweisbar. Diese Veränderungensind nicht mit den Methoden der klinischen Routinediagnostikdarstellbar.\n▪Die Lebenserwartung ist normal. Das Risiko für andere somati-\nsche Krankheiten ist nicht erhöht.\n▪Die Betroffenen verfügen über Möglichkeiten (z. B. Ernäh-\nrungsumstellung, Stressreduktion), durch eigene Aktivitätendie Beschwerden zu lindern und die Lebensqualität zu verbes-sern.\n1356 Layer P et al. Update S3-Leitlinie Reizdarmsyndrom …Z Gastroenterol 2021; 59: 1323 –1415 | © 2021. Thieme. All rights reserved.Leitlinie', metadata={'source': 'Database/Gastroenterologie, Verdauungs- und Stoffwechselkrankheiten/021-016l_S3_Definition-Pathophysiologie-Diagnostik-Therapie-Reizdarmsyndroms_2022-02.pdf', 'page': 56, 'Gültigkeit': 'Gültig'}),
                Document(page_content='content of source 2', metadata={'source': 'namepdfsource2.pdf', 'page': 8, 'Gültigkeit': 'Abgelaufen'}),
                Document(page_content='content of source 3', metadata={'source': 'pdfnamesource3.pdf', 'page': 7, 'Gültigkeit': 'Gültig'})
            ]
        }

        # Update the chat history
        self.chat_history.extend([(query, result_test["answer"])])

        # Convert the result to a serializable format
        serializable_result = jsonable_encoder(result_test)

        # Serialize the result to JSON
        # result_json = json.dumps(serializable_result, ensure_ascii=False, indent=4)

        # Print the result to the console for debugging
        # print(result_json)

        return serializable_result

    def clr_history(self):
        self.chat_history = []

    # Test function to demonstrate JSON serialization
    def test_default_prompt(self):
        default_prompt = "Wie behandel ich einen Patienten mit Gastritis?"
        result_json = self.convchain(default_prompt)
        try:
            # Attempt to parse the JSON string back into a dictionary
            result_dict = json.loads(result_json)
            print("The result is a valid JSON object.")
            print(result_dict)
        except json.JSONDecodeError:
            print("The result is not a valid JSON object.")

# If this file is run as a script, execute the test function
if __name__ == "__main__":
    cbfs_instance = cbfs()
    cbfs_instance.test_default_prompt()
