import sys
from loguru import logger
from typing import List, Optional
from datetime import datetime

from stefan.execution_context import ExecutionContext

class LLMLogger:

    def __init__(self, global_enabled: bool = True):
        logger.add(sys.stdout, filter=lambda record: "console" in record["extra"])
        logger.add(".kmpcoder/log/full_{time}.log", filter=lambda record: "full" in record["extra"])
        logger.add(".kmpcoder/log/short_{time}.log", filter=lambda record: "short" in record["extra"])
        logger.add(".kmpcoder/log/path_{time}.log", filter=lambda record: "path" in record["extra"])
        logger.add(".kmpcoder/log/price_{time}.log", filter=lambda record: "price" in record["extra"])
        logger.add(".kmpcoder/log/executor_{time}.log", filter=lambda record: "executor" in record["extra"])
        self.global_enabled = global_enabled

    def log_input(
        self,
        tag: str,
        model_name: str,
        messages: List[dict],
        llm_request_id: str,
        enabled: bool | None = None,
    ):
        if enabled is None:
            enabled = self.global_enabled

        if not enabled:
            return
        
        # Full log
        messages_original = messages
        messages_original_str = "".join(["----- " + msg.get("role") + " -----"  + "\n" + msg.get("content") + "\n" for msg in messages_original])
        full_message = f"\n----- LLM INPUT {model_name} - {tag} - {llm_request_id} -----\n{messages_original_str}"
        logger.bind(full=True).info(full_message)

        # Short log
        messages_shortened = [
            {**msg, "content": "system" if msg.get("role") == "system" else msg.get("content")}
            for msg in messages
        ]
        messages_shortened_str = "".join(["----- " + msg.get("role") + " -----" + "\n" + msg.get("content") + "\n\n" for msg in messages_shortened])
        short_message = f"----- LLM INPUT {model_name} - {tag} - {llm_request_id} -----\n{messages_shortened_str}"
        logger.bind(short=True).info(short_message)

        # Console log
        logger.bind(console=True).info(short_message)

    def log_output(
        self,
        tag: str,
        model_name: str,
        response: str,
        llm_request_id: str,
        enabled: bool | None = None,
    ):
        if enabled is None:
            enabled = self.global_enabled

        if not enabled:
            return
        
        # Full log
        full_message = f"\n----- LLM OUTPUT {model_name} - {tag} - {llm_request_id} -----\n{response}"
        logger.bind(full=True).info(full_message)

        # Short log
        short_message = f"----- LLM OUTPUT {model_name} - {tag} - {llm_request_id} -----\n{response}"
        logger.bind(short=True).info(short_message)

        # Console log
        logger.bind(console=True).info(short_message)

    def log_error(
        self,
        tag: str,
        model_name: str,
        message: str,
        error: Exception,
        llm_request_id: str,
        enabled: bool | None = None,
    ):
        if enabled is None:
            enabled = self.global_enabled

        if not enabled:
            return
        
        # Full log
        full_message = f"\n----- LLM ERROR {model_name} - {tag} - {llm_request_id} -----\n{message}\n{error}"
        logger.bind(full=True).error(full_message)

        # Short log
        short_message = f"----- LLM ERROR {model_name} - {tag} - {llm_request_id} -----\n{message}\n{error}"
        logger.bind(short=True).error(short_message)

        # Console log
        logger.bind(console=True).error(short_message)

    def log_tool_usage(
        self,
        agent_name: str,
        tool_name: str,
        execution_context: ExecutionContext,
    ):  
        space = " " * execution_context.depth * 2
        logger.bind(path=True).info(f"{space}{agent_name} started using {tool_name}")

    def log_tool_success(
        self,
        agent_name: str,
        tool_name: str,
        execution_context: ExecutionContext,
    ):  
        space = " " * execution_context.depth * 2
        logger.bind(path=True).info(f"{space}{agent_name} used {tool_name} OK")

    def log_tool_error(
        self,
        agent_name: str,
        tool_name: str,
        error: Exception,
        execution_context: ExecutionContext,
    ):  
        space = " " * execution_context.depth * 2
        logger.bind(path=True).info(f"{space}{agent_name} used {tool_name} with error: {error}")

    def log_agent_started(
        self,
        execution_context: ExecutionContext,
    ):  
        if execution_context.current_agent is None:
            raise ValueError("Current agent is None")

        space = " " * execution_context.depth * 2
        logger.bind(path=True).info(f"{space}New agent started: {execution_context.current_agent.name}")

    def log_agent_finished(
        self,
        execution_context: ExecutionContext,
    ):     
        if execution_context.current_agent is None:
            raise ValueError("Current agent is None")
  
        space = " " * execution_context.depth * 2
        logger.bind(path=True).info(f"{space}Agent finished: {execution_context.current_agent.name}")

    def log_agent_finished_with_error(
        self,
        error: Exception,
        execution_context: ExecutionContext,
    ):
        space = " " * execution_context.depth * 2
        logger.bind(path=True).error(f"{space}Agent ' {execution_context.current_agent.name}' finished with error: {error}")

    def log_llm_price(
        self,
        tag: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        cost: float,
        total_cost: float,
        execution_context: ExecutionContext,
    ):
        space = " " * execution_context.depth * 2
        logger.bind(price=True).info(f"{space}LLM call: {tag} - {model} - {input_tokens} input tokens - {output_tokens} output tokens - {cost} cost - Total cost: {total_cost}")

    def log_executor(
        self,
        message: str,
    ):
        logger.bind(executor=True).info(message)


global_llm_logger = LLMLogger()

if __name__ == "__main__":
    llm_logger = global_llm_logger
    llm_logger.log(tag="test", model_name="model", messages=[{"role": "system", "content": "system message"}, {"role": "user", "content": "user message"}], llm_request_id="test")