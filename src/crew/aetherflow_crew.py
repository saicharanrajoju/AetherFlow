from crewai import Crew, Process
from src.agents.data_validator_agent import validator_agent
from src.agents.data_transformer_agent import transformer_agent
from src.agents.pipeline_orchestrator_agent import orchestrator_agent
from src.tasks.validation_tasks import create_validation_task
from src.tasks.transformation_tasks import create_transformation_task
from src.tasks.orchestration_tasks import create_orchestration_task
import time

class AetherFlowCrew:
    def run(self, inputs: dict):
        start_time = time.time()
        
        # Create tasks
        validation_task = create_validation_task(
            dataset_name=inputs['dataset_name'],
            source_path=inputs['source_path']
        )
        
        transformation_task = create_transformation_task(
            dataset_name=inputs['dataset_name'],
            source_path=inputs['source_path'],
            target_format=inputs.get('target_format', 'csv'),
            validation_task=validation_task
        )
        
        orchestration_task = create_orchestration_task(
            dataset_name=inputs['dataset_name'],
            validation_task=validation_task,
            transformation_task=transformation_task
        )
        
        # Create crew
        crew = Crew(
            agents=[validator_agent, transformer_agent, orchestrator_agent],
            tasks=[validation_task, transformation_task, orchestration_task],
            process=Process.sequential,
            verbose=2,
            memory=True
        )
        
        # Execute
        result = crew.kickoff()
        
        execution_time = time.time() - start_time
        
        return {
            'result': result,
            'execution_time': execution_time,
            'status': 'success'
        }
