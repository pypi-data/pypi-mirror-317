#!/usr/bin/env python
import argparse
import json
import os
from pathlib import Path
import traceback
from datetime import datetime

from dotenv import load_dotenv

from stefan.scripts.script_sheet_happen import script_sheet_happen_show_all
from stefan.scripts.script_show_directory import script_show_directory
from stefan.agent.agent_coder import CoderAgent
from stefan.agent.agent_executor_new import AgentExecutorNew
from stefan.agent.agent_planner import PlannerAgent
from stefan.agent.agent_search_code import SearchCodeAgent
from stefan.agent.agent_texts_updater import TextsUpdaterAgent
from stefan.code_search.llm.llm_logger import initialize_global_llm_logger
from stefan.dependencies.service_locator import ServiceLocator
from stefan.execution_context import ExecutionContext
from stefan.execution_input_args import ExecutionInputArgs
from stefan.project_configuration import STEFAN_CONFIG_DIRECTORY, STEFAN_OUTPUTS_DIRECTORY, ExecutionTreeSettings, ProjectContext
from stefan.project_metadata import ProjectMetadata
from stefan.project_metadata_loader import ProjectMetadataLoader
from stefan.tool.tool_rip_grep import RipGrepToolDefinition
from stefan.utils.gspread.gspread_client import GspreadClient
from stefan.utils.xml_answer_parser import XMLAnswerParser

load_dotenv()

def start_agent(project_context: ProjectContext):
    args = get_arguments()
    initialize_global_llm_logger(project_context=project_context)

    service_locator = ServiceLocator()

    # Initialize agent executor with planner agent
    initial_agent = PlannerAgent.create_instance(allow_self_use=True)
    #initial_agent = TextsUpdaterAgent()

    context = ExecutionContext.initial(current_agent=initial_agent, project_context=project_context)
    agent_executor = AgentExecutorNew(agent=initial_agent, service_locator=service_locator)

    try:
        response = agent_executor.start_agent_by_user(user_request=args.task, context=context)
        if response.error is not None:
            raise response.error

        print(f"Process finished with success:\n\n")

        print(f"Answer raw:\n{response.result}\n\n")

        answer = XMLAnswerParser.parse_answer_xml(response.result)
        print("Answer formatted:\n" + json.dumps(answer.answer_dict, indent=2) + "\n\n")

    except Exception as e:
        print(f"Process failed with error:\n{e}\n\n")
        traceback.print_exc()

    print("")
    print(f"Total cost: {service_locator.get_execution_tree_builder().get_total_cost()}")

def _setup_python_project_and_create_project_context() -> ProjectContext:
    # Get command line arguments
    args = get_arguments()

    # Change working directory
    os.chdir(args.working_dir)

    # Initialize the service locator
    project_context = _create_python_project_context(args.working_dir)

    # Initialize the service locator
    _initialize_service_locator(project_context=project_context)

    return project_context

def _setup_kotlin_project_and_create_project_context() -> ProjectContext:
    # Get command line arguments
    args = get_arguments()

    # Change working directory
    os.chdir(args.working_dir)

    # Initialize the service locator
    project_context = _create_kotlin_project_context(args.working_dir)

    # Initialize the service locator
    _initialize_service_locator(project_context=project_context)

    return project_context

def _initialize_service_locator(project_context: ProjectContext):
    service_locator = ServiceLocator()
    service_locator.set_project_context(project_context)
    service_locator.initialize_execution_tree_builder_as_singleton()

def _create_kotlin_project_context(working_dir: Path):
    metadata_file_path = Path(working_dir) / STEFAN_CONFIG_DIRECTORY / "stefan_config.yaml"
    project_metadata = ProjectMetadataLoader().load_from_file(metadata_file_path)

    # Create absolute path for outputs
    outputs_dir = Path(working_dir) / STEFAN_OUTPUTS_DIRECTORY

    project_context = ProjectContext(
        execution_id=datetime.now().strftime('%Y%m%d_%H%M%S'),
        root_directory=Path(working_dir),
        execution_directory=outputs_dir,
        execution_tree_settings=ExecutionTreeSettings(save_on_update=True),
        metadata=project_metadata,
    )

    return project_context

def _create_python_project_context(working_dir: str):
    project_metadata = ProjectMetadata(
        exclude_patterns=[".*", "__pycache__", ".git", ".kpmcoder"],
        include_patterns=["*.py"],
    )

    # Create absolute path for outputs
    outputs_dir = Path(working_dir) / STEFAN_OUTPUTS_DIRECTORY

    project_context = ProjectContext(
        execution_id=datetime.now().strftime('%Y%m%d_%H%M%S'),
        root_directory=Path(working_dir),
        execution_directory=outputs_dir,
        execution_tree_settings=ExecutionTreeSettings(save_on_update=True),
        metadata=project_metadata,
    )

    return project_context
    
def get_arguments():
    """
    Get command line arguments
    """ 
    parser = argparse.ArgumentParser(
        description='Run Stefan The Coder with a task description',
    )
    parser.add_argument(
        '--task',
        nargs='?',
        required=True,
        help='Description of the task to perform',
    )
    parser.add_argument(
        '--working-dir',
        default='.',
        help='Specify the working directory from which the script will be executed',
    )
    args = parser.parse_args()

    return ExecutionInputArgs(
        task=args.task,
        working_dir=Path(args.working_dir),
    )

def main():
    project_context = _setup_kotlin_project_and_create_project_context()
    start_agent(project_context=project_context)
    #script_show_directory(project_context=project_context)
    #script_sheet_happen_show_all()

if __name__ == "__main__":
    main()