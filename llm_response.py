from langchain_core.prompts import ChatPromptTemplate

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
        question = """
        Based on the experiences they wrote about in the journal, suggest 4 famous quotes that the writer of the journal would find inspiring
        Output your answer in the format specified below, replacing each instance of "quote" with a quote, and each instance of "author" with the name of its author:

        quote
        \n-author

        quote
        \n-author

        quote
        \n-author

        quote
        \n-author
        """

        prompt = self.prompt_template.invoke({
            "context": self.journal,
            "question": question
        })

        return self.model.invoke(prompt)
    
    def poem_response(self):
        question = """
        Write a short poem inspired by the contents of the journal that would help the author feel better about any concerns they wrote about.  
        """

        prompt = self.prompt_template.invoke({
            "context": self.journal,
            "question": question
        })

        return self.model.invoke(prompt)
    



        





