import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

class LLMResponse:
    def __init__(self, model, journal):
        self.model = model
        self.journal = journal

        #system prompt
        self.sys = """
        You are a thoughtful and emotional AI companion who makes observations and gives helpful reccomendations.
        """
        
        # add question section to prompt
        self.journal_prompt = """
        Your task is to read this journal and answer the following question about the journal.
        Here is the journal:\n\n{context}\n

        Question:\n\n{question}"""

        self.prompt_template = ChatPromptTemplate.from_messages(
        [("system", self.sys), ("user", self.journal_prompt)]
        )

    def quote_response(self):
        question = "Based on the content of the journal, suggest 3 famous quotes each related to a significant topic or theme in the journal"
        
        schema = {
            "name": "quotes",
                "description": "Three quotes.  Each quote should be in the format of 'quote' - 'author'",
                "parameters" : {
                    "type" : "object",
                    "properties" : {
        "quote 1" : {
            "type" : "string"
        },
        "quote 2" : {
            "type" : "string"
            },
        "quote 3" : {
            "type" : "string"
            },
                }
            }   
        }

        prompt = self.prompt_template.invoke({
            "context": self.journal,
            "question": question
        })

        # Get the model's response
        json_out = self.model.with_structured_output(schema)
        return json_out.invoke(prompt)
        
    
    def poem_response(self):
        question = """
        Write a short poem inspired by the contents of the journal that would help the author feel better about any concerns they wrote about.
        """

        poem_schema = {
            "name" : "poem",
            "description": "A short poem about the journal.  Limit the poem to 400 characters.",
            "parameters" :{
                "type" : "object",
                "properties" : {
                    "poem" : {
                    "type" : "string"
                },
            }}}

        prompt = self.prompt_template.invoke({
            "context": self.journal,
            "question": question
        })

        json_out = self.model.with_structured_output(poem_schema)
        return json_out.invoke(prompt)
    



        





