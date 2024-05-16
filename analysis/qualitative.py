import torch
from transformers import RagTokenizer, RagRetriever, RagTokenForGeneration

class QualitativeAnalysisRAG:
    """
    A class for generating qualitative analysis paragraphs using the RAG system.

    Attributes:
    model_name (str): The name of the RAG model.
    retriever_name (str): The name of the retriever model.
    data (dict): The input data in JSON format.
    """

    def __init__(self, model_name="facebook/rag-token-nq", retriever_name="facebook/dpr-question_encoder-single-nq-base", data=None):
        """
        Initializes the QualitativeAnalysisRAG class.

        Args:
        model_name (str, optional): The name of the RAG model. Defaults to "facebook/rag-token-nq".
        retriever_name (str, optional): The name of the retriever model. Defaults to "facebook/dpr-question_encoder-single-nq-base".
        data (dict, optional): The input data in JSON format. Defaults to None.
        """
        self.model_name = model_name
        self.retriever_name = retriever_name
        self.data = data

    def generate_insights(self, research_question):
        """
        Generates qualitative analysis paragraphs based on the research question and input data.

        Args:
        research_question (str): The research question or heading for the analysis.

        Returns:
        str: Qualitative analysis paragraphs generated by the RAG model.
        """
        # Load tokenizer, retriever, and generator
        tokenizer = RagTokenizer.from_pretrained(self.model_name)
        retriever = RagRetriever.from_pretrained(self.retriever_name)
        model = RagTokenForGeneration.from_pretrained(self.model_name)

        # Prepare input data for model
        input_text = research_question + " " + self.format_data_as_text()

        # Encode input text and retrieve relevant documents
        inputs_dict = tokenizer.prepare_input_seq2seq_batch(input_text, return_tensors="pt")
        docs = retriever.retrieve(inputs_dict["input_ids"].tolist(), top_k=3)

        # Generate qualitative analysis
        with torch.no_grad():
            generated = model.generate(inputs_dict["input_ids"], retriever=docs, max_length=300)

        # Decode output and return as string
        return tokenizer.decode(generated[0], skip_special_tokens=True)

    def format_data_as_text(self):
        """
        Formats input data from JSON format to text format.

        Returns:
        str: Input data formatted as text.
        """
        if self.data is None:
            return ""
        
        text = ""
        for key, value in self.data.items():
            text += f"{key}: {value}\n"
        return text



# Initialize QualitativeAnalysisRAG instance
analysis_rag = QualitativeAnalysisRAG(data=data_json)

# Generate qualitative analysis using RAG
analysis_result_rag = analysis_rag.generate_insights(research_question)

print(analysis_result_rag)