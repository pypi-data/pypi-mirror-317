from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from .storage import get_storage_adapter, add_code_run_history, add_tool, add_suggestion
from .config import MetaToolConfig
from pydantic import create_model, Field
from typing import Optional
from .schemas import SavedTool, CodeRunHistory
from langchain_core.tools import StructuredTool
from interpreter import interpreter
from uuid import uuid4
from langchain_community.agent_toolkits import FileManagementToolkit
from .storage.base import ToolStatus
import os


class MetaTool:
    """Main interface for metatool functionality"""

    def __init__(self, **config):
        """
        Initialize MetaTool with configuration.

        Args:
            **config: Configuration parameters that match MetaToolConfig
        """
        # Add type mapping as class attribute
        self.TYPE_MAPPING = {
            "string": str,
            "number": float,
            "integer": int,
            "boolean": bool,
            "array": list,
            "object": dict,
        }

        # Add code run history as class attribute
        self.code_run_history = []

        self.config = MetaToolConfig(**config)

        if not self.config.openai_api_key:
            self.config.openai_api_key = os.environ.get("OPENAI_API_KEY")
            if not self.config.openai_api_key:
                raise ValueError(
                    "OpenAI API key is not set. Please provide it in the config or set the OPENAI_API_KEY environment variable."
                )

        if not os.path.exists(self.config.root_dir):
            os.makedirs(self.config.root_dir)

        self.storage = get_storage_adapter(self.config)

        self._setup_agent()

    def run_python_code(self, code: str) -> str:
        """Run python code using Open Interpreter and return the result.

        Args:
            code: The python code to execute as a string

        Returns:
            The output of the code execution
        """
        interpreter.reset()
        result = interpreter.computer.run("python", code)
        result_str = str(result)

        self.code_run_history.append(CodeRunHistory(code=code, result=result_str))
        code_run_history_uuid = add_code_run_history(uuid4(), code, result_str)
        suggested_tool = self.extract_tool()
        suggested_tool_uuid = add_tool(
            uuid4(), suggested_tool, status=ToolStatus.SUGGESTED
        )
        add_suggestion(uuid4(), code_run_history_uuid, suggested_tool_uuid)

        return result_str

    def run_bash_command(self, command: str) -> str:
        """Run bash command using Open Interpreter and return the result.

        Args:
            command: The bash command to execute as a string

        Returns:
            The output of the code execution
        """
        interpreter.reset()
        result = interpreter.computer.run("bash", command)
        result_str = str(result)

        return result_str

    def save_as_tool(self, tool_name: str = "", description: str = "") -> SavedTool:
        """Save the past code runs as a new tool with structured output.

        Args:
            tool_name: Optional name for the tool. If not provided, a descriptive name will be suggested.
            description: Optional description of what the tool does. If not provided, one will be generated.

        Returns:
            A SavedTool object containing:
                - code: Python function implementation as string
                - tool: JSON schema for the tool following ToolSchema format
        """
        tool = self.extract_tool(tool_name, description)
        add_tool(uuid4(), tool, status=ToolStatus.ACTIVE)
        return tool

    def _setup_agent(self):
        """Setup the internal agent with configured tools and model"""
        # Initialize LLM
        self.llm = ChatOpenAI(
            model_name=self.config.model_name,
            temperature=self.config.temperature,
            openai_api_key=self.config.openai_api_key,
        )

        # Setup file tools
        file_tools = FileManagementToolkit(
            root_dir="./temp",
            selected_tools=["list_directory", "file_search"],
        ).get_tools()

        # Combine with user-provided tools
        self.tools = [
            StructuredTool.from_function(self.run_python_code),
            StructuredTool.from_function(self.run_bash_command),
            StructuredTool.from_function(self.save_as_tool),
        ] + file_tools

        # Setup prompt
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"""You are a helpful AI assistant.
                    You have access to the following tools:
                    1. run_python_code
                    2. run_bash_command
                    3. save_as_tool
                    4. File tools to list files in a directory
                    5. File tools to search for files in a directory

                    For file operations you can also use python or bash tool to accomplish the goal.
                    
                    The current directory is {self.config.root_dir}
                    And to access the files, use {self.config.root_dir}/<file_name>
                    
                    IMPORTANT: don't ask back to user which file to specify, before that try to list_directory first""",
                ),
                MessagesPlaceholder(variable_name="messages"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        # Create agent
        self.agent = create_openai_functions_agent(self.llm, self.tools, self.prompt)

        # Create executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=self.config.verbose,
            return_intermediate_steps=self.config.verbose,
        )

    def convert_saved_tool_to_structured(self, saved_tool: SavedTool) -> StructuredTool:
        """Convert a SavedTool to a StructuredTool"""
        # Create a new module-like namespace for the function
        namespace = type("ModuleType", (), {"__dict__": {}})()

        # Execute the function code in its own namespace
        exec(saved_tool.code, namespace.__dict__)
        func = namespace.__dict__[saved_tool.tool_schema.name]

        # Create input schema dynamically from ToolSchema
        field_definitions = {}
        for name, param in saved_tool.tool_schema.parameters.items():
            # Get Python type from mapping
            python_type = self.TYPE_MAPPING.get(
                param.type, str
            )  # default to str if type not found

            # Handle optional parameters
            if name not in saved_tool.tool_schema.required:
                field_definitions[name] = (
                    Optional[python_type],
                    Field(description=param.description, default=param.default),
                )
            else:
                field_definitions[name] = (
                    python_type,
                    Field(description=param.description),
                )

        # Create the input schema model dynamically
        InputSchema = create_model(
            f"{saved_tool.tool_schema.name}Input",
            **field_definitions,
        )

        return StructuredTool.from_function(
            func=func,
            name=saved_tool.tool_schema.name,
            description=saved_tool.tool_schema.description,
            args_schema=InputSchema,
            return_direct=True,
        )

    def extract_tool(self, tool_name: str = "", description: str = "") -> SavedTool:
        """Extract the past code runs as a new tool with structured output.

        Args:
            tool_name: Optional name for the tool. If not provided, a descriptive name will be suggested.
            description: Optional description of what the tool does. If not provided, one will be generated.

        Returns:
            A SavedTool object containing:
                - code: Python function implementation as string
                - tool: JSON schema for the tool following ToolSchema format
        """
        if len(self.code_run_history) == 0:
            return {"error": "No code run history available in this session"}

        last_run = self.code_run_history[-1]

        prompt = f"""Based on this code and its output:
        
        Code:
        {last_run.code}
        
        Output:
        {last_run.result}
        
        Create a reusable Python function tool with the following:
        1. Function name: {tool_name if tool_name else '[suggest a descriptive name]'}
        2. Description: {description if description else '[generate a helpful description]'}
        3. Parameters with JSON Schema types and descriptions
        4. Return type in JSON Schema format
        
        Return the response in this JSON format:
        {{
            "code": "complete python function implementation as string",
            "tool": {{
                "name": "function_name",
                "description": "function description",
                "parameters": {{
                    "param_name": {{
                        "type": "string|number|integer|boolean|array|object",
                        "description": "parameter description",
                        "required": true,
                        "default": null
                    }},
                    ...
                }},
                "required": ["required_param1", "required_param2"],
                "returns": {{
                    "type": "string|number|integer|boolean|array|object",
                    "description": "return value description"
                }}
            }}
        }}
        """

        # Bind schema to model and use self.llm
        llm_with_structure_output = self.llm.with_structured_output(SavedTool)
        # Invoke the model to produce structured output that matches the schema
        tool = llm_with_structure_output.invoke(prompt)

        return tool

    def run(self, instructions: str) -> str:
        """
        Process natural language instructions.

        Args:
            instructions: The natural language instructions to process

        Returns:
            str: The response from processing the instructions
        """
        result = self.agent_executor.invoke(
            {"messages": [HumanMessage(content=instructions)]}
        )

        # Display tool call history if verbose
        if self.config.verbose and "intermediate_steps" in result:
            print("\n    MetaTool, Tool Call History:")
            for step in result["intermediate_steps"]:
                action = step[0]
                output = step[1]
                print(f"\n    🔧 Tool: {action.tool}")
                print(f"    📥 Input: {action.tool_input}")
                print(f"    📤 Output: {output}")

        return result["output"]
