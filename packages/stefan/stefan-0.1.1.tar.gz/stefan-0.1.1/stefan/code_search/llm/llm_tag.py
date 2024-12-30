from enum import Enum

class LLMTag(Enum):
    # Agents
    AGENT_PLANNER = "agent_planner"
    AGENT_CODER = "agent_coder"
    AGENT_SEARCH_CODE = "agent_search_code"
    AGENT_SAMPLES_PROVIDER = "agent_samples_provider"
    AGENT_TEXTS_UPDATER = "agent_texts_updater"

    # Code search
    CODE_SEARCH_DIRECTORY_DESCRIPTION = "code_search_directory_description"
    CODE_SEARCH_FILE_DESCRIPTION = "code_search_file_description"
    CODE_SEARCH_FILE_RELEVANCY = "code_search_file_relevancy"

    MONTE_CARLO_SOLUTION_EVALUATION = "monte_carlo_solution_evaluation"
