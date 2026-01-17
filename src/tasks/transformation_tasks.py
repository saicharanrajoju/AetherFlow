from crewai import Task
from src.agents.data_transformer_agent import transformer_agent

def create_transformation_task(dataset_name: str, source_path: str, target_format: str, validation_task):
    return Task(
        description=f"""Transform the dataset '{dataset_name}' from '{source_path}' to '{target_format}' format.
        
        Based on the validation report, perform:
        1. Handle missing values (use pandas_tool with fillna_mean or dropna)
        2. Remove duplicates (use pandas_tool with remove_duplicates)
        3. Clean text columns if needed (use regex_cleaner)
        4. Document all transformations performed
        
        Return transformation log with operations performed and output file path.""",
        expected_output='Transformation log with operations performed, output file path, and success status',
        agent=transformer_agent,
        context=[validation_task]
    )
