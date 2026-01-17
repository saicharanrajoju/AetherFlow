import unittest
from unittest.mock import MagicMock, patch
from src.crew.aetherflow_crew import AetherFlowCrew
from src.agents.data_validator_agent import validator_agent
from src.agents.data_transformer_agent import transformer_agent
from src.agents.pipeline_orchestrator_agent import orchestrator_agent

class TestAetherFlowCrew(unittest.TestCase):
    def setUp(self):
        self.crew_instance = AetherFlowCrew()

    def test_agents_initialization(self):
        self.assertIsNotNone(validator_agent)
        self.assertIsNotNone(transformer_agent)
        self.assertIsNotNone(orchestrator_agent)
        
    @patch('src.crew.data_pipeline_crew.Crew.kickoff')
    def test_crew_run(self, mock_kickoff):
        mock_kickoff.return_value = "Pipeline executed successfully"
        inputs = {
            'dataset_name': 'test_data',
            'source_path': './data/test.csv',
            'target_format': 'parquet'
        }
        result = self.crew_instance.run(inputs)
        self.assertEqual(result, "Pipeline executed successfully")
        mock_kickoff.assert_called_once_with(inputs=inputs)

    def test_agent_tools(self):
        self.assertTrue(len(validator_agent.tools) > 0)
        self.assertTrue(len(transformer_agent.tools) > 0)
        self.assertTrue(len(orchestrator_agent.tools) > 0)

if __name__ == '__main__':
    unittest.main()
