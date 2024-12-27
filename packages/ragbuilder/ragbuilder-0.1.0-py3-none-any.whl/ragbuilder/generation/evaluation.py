
from abc import ABC, abstractmethod
from datasets import Dataset
import pandas as pd
from ragbuilder.config.generator import EvalDataset
# from ragbuilder.generation.utils import get_eval_dataset
from ragas.metrics import (
    answer_relevancy,
    faithfulness,
    context_recall,
    context_precision,
    answer_correctness
)
from ragas import evaluate, RunConfig
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from datetime import datetime
from datasets import Dataset
import pandas as pd
from ragbuilder.config.generator import EvalDataset
from typing import List

from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

class Evaluator(ABC):
    @abstractmethod
    def evaluate(self, eval_dataset: Dataset) -> Dataset:
        """
        Evaluate the prompt generation Phase and returns detailed results.
        
        Returns:
        Dataset: A dataset containing the evaluation results.
        """
        pass
    def __init__(self) -> None:
        super().__init__()
        self.eval_dataset = None

class RAGASEvaluator(Evaluator):
    def __init__(self) -> None:
        super().__init__()
        print("RAGASEvaluator initiated")

    def get_eval_dataset(self,eval_dataset_path) -> Dataset:
            """
            This function reads a CSV file, validates the required columns (`question` and `ground_truth`),
            converts each row to a Pydantic model, and returns a Dataset for Ragas compatibility.

            Args:
            - csv_file_path (str): Path to the CSV file.

            Returns:
            - Dataset: A Ragas-compatible dataset.

            Raises:
            - ValueError: If required columns (`question` and `ground_truth`) are missing or invalid.
            """
            # Load the CSV into a DataFrame
            df = pd.read_csv(eval_dataset_path)

            # Check if the required columns are present
            required_columns = ['question', 'ground_truth']
            missing_columns = [col for col in required_columns if col not in df.columns]
            df = df.dropna(subset=['ground_truth'])
            if missing_columns:
                raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

            # Convert the dataframe to a Pydantic model and validate
            try:
                eval_dataset_model = EvalDataset.from_dataframe(df)
            except ValueError as e:
                raise ValueError(f"Validation error: {e}")

            # Convert the validated Pydantic model to a dataset for Ragas
            result_dict = [item.dict() for item in eval_dataset_model.items]
            eval_dataset = Dataset.from_list(result_dict)
            self.eval_dataset=eval_dataset
            return eval_dataset
    def evaluate(self, eval_dataset: Dataset,llm= AzureChatOpenAI(model="gpt-4o-mini"), embeddings=AzureOpenAIEmbeddings(model="text-embedding-3-large"))-> Dataset:
        result = evaluate(
                eval_dataset,
                metrics=[
                    answer_correctness,
                    faithfulness,
                    answer_relevancy,
                    context_precision,
                    context_recall,
                ],
                raise_exceptions=False, 
                is_async=True,
                run_config=RunConfig(timeout=240, max_workers=1, max_wait=180, max_retries=10)
            )
        result_df = result.to_pandas()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_csv_path = 'rag_eval_results_'+timestamp+'.csv'
        selected_columns = ["prompt_key","prompt","question","answer","ground_truth","answer_correctness","faithfulness","answer_relevancy","context_precision","context_recall",'config']
        result_df[selected_columns].to_csv(output_csv_path, index=False)
        print("evaluate_prompts completed")
        print(Dataset.from_pandas(result_df[selected_columns]))
        return Dataset.from_pandas(result_df[selected_columns])