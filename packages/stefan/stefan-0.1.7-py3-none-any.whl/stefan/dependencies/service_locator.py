from stefan.code_search.code_search_full_text import CodeSearchFullText
from stefan.code_search.code_search_relevancy import CodeSearchRelevancy
from stefan.code_search.code_search_persistence import CodeSearchPersistence
from stefan.code_search.code_search_tree_creator import CodeSearchTreeCreator
from stefan.code_search.code_search_tree_processor import CodeSearchTreeProcessor
from stefan.code_search.llm.llm_directory_description import DirectoryDescriptionLLMProcessor
from stefan.code_search.llm.llm_file_description import FileDescriptionLLMProcessor
from stefan.code_search.llm.llm_file_relevancy import FileRelevancyLLMProcessor
from stefan.code_search.llm.llm_executor import LLMExecutor
from stefan.execution_tree.execution_tree_builder import ExecutionTreeBuilder
from stefan.project_configuration import ProjectContext
from stefan.utils.async_execution import AsyncExecution
from stefan.utils.singleton import singleton

@singleton
class ServiceLocator:

    def __init__(self):
        self.services = {}
        self.EXECUTION_TREE_BUILDER = "execution_tree_builder"

    def set_project_context(self, project_context: ProjectContext):
        self.project_context = project_context

    def get_project_context(self) -> ProjectContext:
        self._assert_initialized()
        return self.project_context

    def initialize_execution_tree_builder_as_singleton(self):
        self._assert_initialized()
        self._assert_service_not_initialized(self.EXECUTION_TREE_BUILDER)
        
        execution_tree_builder = ExecutionTreeBuilder(self.project_context)
        self.services[self.EXECUTION_TREE_BUILDER] = execution_tree_builder
        return execution_tree_builder
    
    def get_execution_tree_builder(self) -> ExecutionTreeBuilder:
        self._assert_initialized()
        self._assert_service_initialized(self.EXECUTION_TREE_BUILDER)

        return self.services[self.EXECUTION_TREE_BUILDER]

    def create_llm_executor(self):
        self._assert_initialized()

        return LLMExecutor()
    
    def create_async_execution(self):
        self._assert_initialized()

        return AsyncExecution()
    
    def create_code_search(self):
        self._assert_initialized()

        llm_executor = self.create_llm_executor()
        async_execution = self.create_async_execution()
        file_desc_processor = FileDescriptionLLMProcessor(
            llm_executor=llm_executor,
        )
        dir_desc_processor = DirectoryDescriptionLLMProcessor(
            llm_executor=llm_executor,
        )
        file_relevancy_processor = FileRelevancyLLMProcessor(
            llm_executor=llm_executor,
            async_execution=async_execution,
        )
        tree_processor = CodeSearchTreeProcessor(
            llm_file_processor=file_desc_processor,
            llm_directory_processor=dir_desc_processor,
        )
        tree_builder = CodeSearchTreeCreator(
            project_context=self.project_context,
        )
        persistence = CodeSearchPersistence()
        
        return CodeSearchRelevancy(
            tree_processor=tree_processor,
            tree_builder=tree_builder,
            llm_file_relevancy=file_relevancy_processor,
            persistence=persistence,
            project_context=self.project_context,
        )
    
    def create_full_text_search(self):
        self._assert_initialized()

        return CodeSearchFullText(
            tree_builder=CodeSearchTreeCreator(
                project_context=self.project_context,
            ),
            project_context=self.project_context,
        )
    
    def _assert_service_initialized(self, service_name: str):
        if service_name not in self.services:
            raise ValueError(f"Service {service_name} is not initialized")
    
    def _assert_service_not_initialized(self, service_name: str):
        if service_name in self.services:
            raise ValueError(f"Service {service_name} is already initialized")

    def _assert_initialized(self):
        if not hasattr(self, 'project_context'):
            raise ValueError("ServiceLocator is not initialized")