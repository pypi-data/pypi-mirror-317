from typing import List
from stefan.project_configuration import STEFAN_OUTPUTS_DIRECTORY, ExecutionTreeSettings, ProjectContext
from stefan.project_metadata import AvailableCommand, ProjectMetadata

def create_dummy_project_context(path: str = "", exclude_patterns: List[str] = [], include_patterns: List[str] = []):
    project_metadata = ProjectMetadata(
        available_commands=[],
        modules_description=[],
        code_samples=[],
        exclude_patterns=exclude_patterns,
        include_patterns=include_patterns,
    )

    project_context = ProjectContext(
        execution_id="123test123",
        root_directory=path,
        execution_directory=STEFAN_OUTPUTS_DIRECTORY,
        execution_tree_settings=ExecutionTreeSettings(save_on_update=False),
        metadata=project_metadata,
    )

    return project_context