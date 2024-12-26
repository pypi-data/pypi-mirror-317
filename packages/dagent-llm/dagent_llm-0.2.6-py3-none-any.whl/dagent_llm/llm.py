# coding=utf-8
# @Time    : 2024-10-12 09:05:22
# @Author  : zhaosheng@nuaa.edu.cn
# @Describe: LLM.py

import concurrent.futures
import logging
import re
from typing import Any, Dict, List


from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field, create_model
from rich.console import Console
from rich.table import Table

import dagent_llm.version as INFO

console = Console()
# Get the logger for 'httpx'
httpx_logger = logging.getLogger("httpx")
# Set the logging level to WARNING to ignore INFO and DEBUG logs
httpx_logger.setLevel(logging.CRITICAL)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
# print(__name__)
logger.setLevel(logging.CRITICAL)


class LLM:
    def __init__(
        self,
        llm_server="ollama",
        redundancy=-1,
        max_retries=2,
        temperature=0,
        api_key=None,
        base_url=None,
        model_name=None,
        history=None,
        sql_setup=None,
    ):
        """Initialize the LLM class.

        Args:
            llm_server (str, optional): LLM server type. Defaults to "ollama".
            max_retries (int, optional): Max try times when generating structured output. Defaults to 2.
            temperature (int, optional): Defaults to 0.
            api_key (str, optional): Defaults to None.
            base_url (str, optional): Defaults to None.
            model_name (str, optional): Defaults to None.
            history (list, optional): Defaults to [].
            sql_setup (dict, optional): DSqlenv config. Defaults to None.
        """
        if sql_setup:
            try:
                from dsqlenv.core import SQL
                self.sql = SQL(sql_setup)
            except Exception as e:
                logger.error(f"Failed to initialize SQL: {str(e)}")
                console.print(f"[red][bold]Failed to initialize SQL: {str(e)}")
                console.print(
                    "[green]Please provide sql_setup when initializing dagent_llm.LLM()"
                )
                console.print(
                    "[green]Example: sql_setup = {{'DB_HOST': 'localhost', 'DB_PORT': 5432, ...}}"
                )
                console.print(
                    "[green]Please refer to the documentation of the dsqlenv package for more information."
                )
                console.print("[green]https://pypi.org/project/dsqlenv/[/green]")
                console.print(
                    "[yellow]Or you can specify the <api_key>, <base_url>, <model_name>, <temperature>, <max_retries> directly."
                )
                console.print(
                    "[yellow][bold]Example: [/bold][green]LLM(api_key='your_api_key', base_url='your_base_url', model_name='your_model_name', temperature=0.5, max_retries=2)"
                )
                # raise ValueError(f"Failed to initialize SQL: {str(e)}")
                self.sql = {}
        else:
            try:
                from dsqlenv.core import SQL
                # LLM with use dsqlenv to store the data by default
                self.sql = SQL()
            except Exception as e:
                logger.error(f"Failed to initialize SQL: {str(e)}")
                console.print(f"[red][bold]Failed to initialize SQL: {str(e)}")
                console.print(
                    "[green]Please provide sql_setup when initializing dagent_llm.LLM()"
                )
                console.print(
                    "[green]Example: sql_setup = {{'DB_HOST': 'localhost', 'DB_PORT': 5432, ...}}"
                )
                console.print(
                    "[green]Please refer to the documentation of the dsqlenv package for more information."
                )
                console.print("[green]https://pypi.org/project/dsqlenv/[/green]")
                console.print(
                    "[yellow]Or you can specify the <api_key>, <base_url>, <model_name>, <temperature>, <max_retries> directly."
                )
                console.print(
                    "[yellow][bold]Example: [/bold][green]LLM(api_key='your_api_key', base_url='your_base_url', model_name='your_model_name', temperature=0.5, max_retries=2)"
                )
                self.sql = {}
                # raise ValueError(f"Failed to initialize SQL: {str(e)}")
        # If sql is not set, try to use the default settings
        self.llm_server = llm_server
        self.base_url = self._get_or_raise(f"{self.llm_server}_base_url", base_url)
        self.api_key = self._get_or_raise(f"{self.llm_server}_api_key", api_key)
        self.model_name = self._get_or_raise(
            f"{self.llm_server}_model_name", model_name
        )
        self.temperature = self._get_or_raise(
            f"{self.llm_server}_temperature", temperature
        )
        self.max_retries = self._get_or_raise(
            f"{self.llm_server}_max_retries", max_retries
        )
        self.redundancy = redundancy
        # Initialize the model
        self.model = ChatOpenAI(
            model=self.model_name,
            temperature=float(self.temperature),
            max_retries=int(self.max_retries),
            api_key=self.api_key,
            base_url=self.base_url,
        )
        self.history = []
        self.load_history(history)
        self.input_tokens = 0
        self.output_tokens = 0
        self.total_tokens = 0
        if self.redundancy > 0:
            # VERSION, UPDATE, AUTHOR, EMAIL
            console.rule(
                f"DAgent LLM Version: {INFO.__version__} | Update: {INFO.__update__}"
            )
            console.print(f"[green] Copyright: {INFO.__author__}")
            console.print(f"[green] Server: {self.llm_server}")
            console.print(f"[green] Base URL: {self.base_url}")
            console.print(f"[green] Model Name: {self.model_name}")
            console.rule()

    def load_history(self, history):
        """Add a list of messages to the conversation history.

        Args:
            history (list): A list of messages to add to the history.

        Raises:
            ValueError: If the message type is not HumanMessage, SystemMessage, or AIMessage.
            ValueError: If the role is not human, ai, or system.
        """
        if not history:
            return
        for message in history:
            if isinstance(message, (HumanMessage, SystemMessage, AIMessage)):
                self.history.append(message)
            else:
                if isinstance(message, dict):
                    assert "role" in message, "Role is required in the message."
                    assert "content" in message, "Content is required in the message."
                    if message["role"] == "human" or message["role"] == "user":
                        self.history.append(HumanMessage(content=message["content"]))
                    elif (
                        message["role"] == "ai"
                        or message["role"] == "bot"
                        or message["role"] == "agent"
                        or message["role"] == "model"
                        or message["role"] == "assistant"
                        or message["role"] == "llm"
                    ):
                        self.history.append(AIMessage(content=message["content"]))
                    elif (
                        message["role"] == "system"
                        or message["role"] == "sys"
                        or message["role"] == "admin"
                    ):
                        self.history.append(SystemMessage(content=message["content"]))
                    else:
                        logger.error(f"Invalid role: {message['role']}")
                        logger.error(f"Message content: {message}")
                        raise ValueError(f"Invalid role: {message['role']}")
                logger.error(f"Invalid message type: {type(message)}")
                logger.error(f"Message content: {message}")
                logger.error(
                    "Only langchain_core.messages.HumanMessage, \
                    SystemMessage, and AIMessage are allowed."
                )
                raise ValueError(f"Invalid message type: {type(message)}")

    def chat(self, message: str, role: str = "human", add_to_history: bool = True, stream=False):
        """
        This method allows users to chat with the model.

        Args:
        - message: The message to send to the model.
        - role: The role of the user (human, ai, system).
        - add_to_history: Whether to log the conversation to history.
        """
        if role == "human":
            self.history.append(HumanMessage(content=message))
        elif role == "ai":
            self.history.append(AIMessage(content=message))
        elif role == "system":
            self.history.append(SystemMessage(content=message))
        else:
            raise ValueError(f"Invalid role: {role}")
        if stream:
            response = self.model.stream(message)
            # While Using stream mode:
            # content='' additional_kwargs={} response_metadata={} id='xxxx'
            # content='Hello' additional_kwargs={} response_metadata={} id='xxxx'
            # content='!' additional_kwargs={} response_metadata={} id='xxxx'
            # ...
        else:
            response = self.model.invoke(self.history)
            self._update_token_usage(response.usage_metadata)
            if add_to_history:
                self.history.append(response)
        return response

    def choose(
        self,
        options,
        prompt,
        option_type=None,
        need_reason=False,
        multiple=False,
        add_to_history=False,
        max_try=3,
        examples=None,
        notes=None,
    ):
        """
        This method allows users to provide options, a prompt, and other settings to choose an option.
        It supports few-shot learning through `examples` and allows `notes` to be added for customized behavior.

        Args:
        - options: List of options to choose from.
        - prompt: The question or task prompt.
        - option_type: String describing the type of options.
        - need_reason: Whether the model should provide reasons.
        - multiple: Whether multiple options can be selected.
        - add_to_history: Whether to log the conversation to history.
        - max_try: Maximum retries for invalid responses.
        - examples: Few-shot examples for better model context.
        - notes: A list of instructions or notes that the model should consider.

        Returns:
        - The selected option(s) and reasons (if applicable).
        """
        # print(f"Now history: {self.history}")
        if self.redundancy > 0:
            # Print prompt
            console.print(f"[bold]Prompt:[/bold] {prompt}")
            console.print(f"* Need Reason: {need_reason}")
            console.print(f"* Multiple: {multiple}")
            console.print(f"* Max Try: {max_try}")
            console.print(f"* Examples: {examples}")
            console.print(f"* Notes: {notes}")
            table = Table(title="Options")
            table.add_column("Index", justify="center", style="cyan")
            table.add_column("Option", justify="center", style="magenta")
            for i, option in enumerate(options):
                table.add_row(str(i), option)
            console.print(table)

        with console.status("[bold green] LLM is choosing..."):
            # if option_type is not provided， we will use the LLM to automatically generate it
            if not option_type:
                try:
                    logger.info("Option type not provided. Using LLM to generate it.")
                    # generate message
                    tmp_msg = "Now we want use LLM to choose the option from the following options: "
                    for i, option in enumerate(options):
                        tmp_msg += f"{i+1}. {option}, "
                    tmp_msg = tmp_msg[:-2] + "."
                    tmp_msg += "\n\nWhat is the option name?"
                    tmp_msg += "\nFor example, when the chooses is 'apple', 'banana', 'orange', the option type is 'fruit'."
                    tmp_msg += "\nPlease provide the option type.(just one or two word)"
                    option_type = self.model.invoke(tmp_msg).content
                    if self.redundancy > 0:
                        console.print(
                            "Option Type is not provided. Using LLM to generate it."
                        )
                        console.print(f"[bold]Option Type:[/bold] {option_type}")
                except Exception as e:
                    logger.error(f"Failed to generate option type: {str(e)}")
                    option_type = "option"
            if need_reason:

                class Choice(BaseModel):
                    choice: str = Field(
                        description=f"The chosen {option_type}, separate multiple choices by commas if allowed."
                    )
                    reason: str = Field(description="The reason for the choice.")

            else:

                class Choice(BaseModel):
                    choice: str = Field(
                        description=f"The chosen {option_type}, separate multiple choices by commas if allowed."
                    )

            structured_llm = self.model.with_structured_output(Choice)
            # Build the prompt with options and notes
            new_prompt = f"{prompt}\n\nOptions: {options}"
            new_prompt += f"\n\nPlease choose the {option_type}."
            if multiple:
                new_prompt += " (Multiple selections are allowed)"
            if need_reason:
                new_prompt += " and provide a reason."
            # Incorporate examples into the prompt if provided
            if examples:
                example_text = "\n\nHere are some examples for reference:\n"
                for example in examples:
                    example_text += f"- {example}\n"
                new_prompt += example_text
            # Add any additional notes to the prompt
            if notes:
                note_text = "\n\nConsider the following points:\n"
                for note in notes:
                    note_text += f"- {note}\n"
                new_prompt += note_text
            new_prompt += "\n\nMake sure all choices are from the provided options."
            # Chat interaction loop with retry
            result = []
            if add_to_history:
                self.history.append(HumanMessage(content=new_prompt))
            for attempt in range(max_try):
                response = structured_llm.invoke(new_prompt)
                if add_to_history:
                    self.history.append(response)
                choices = [
                    c.strip()
                    for c in response.choice.split(",")
                    if c.strip() in options
                ]
                if choices:
                    result = choices
                    break
                else:
                    logger.error(
                        f"Invalid choices: {response.choice}. Attempt {attempt + 1}/{max_try}."
                    )
                    if self.redundancy > 0:
                        console.print(
                            f"[red]Invalid choices: {response.choice}. Attempt {attempt + 1}/{max_try}."
                        )
            if not result:
                if self.redundancy > 0:
                    console.print("[red]Max retries reached. No valid options chosen.")
                raise ValueError("Max retries reached. No valid options chosen.")
            if need_reason:
                reason = response.reason
            else:
                reason = None
            r = result if multiple else result[0]
            return {"choice": r, "reason": reason}

    def choose_with_args(
        self,
        options,
        prompt,
        option_type,
        need_reason=False,
        multiple=False,
        add_to_history=False,
        max_try=3,
        examples=None,
        notes=None,
    ):
        """
        Presents options and prompts the user to choose one or more options.
        Arguments:
        - options: A list of choices to display.
        - prompt: The prompt for the choice.
        - option_type: The type of option being selected (e.g., function).
        - need_reason: If True, asks for a reason along with the choice.
        - multiple: If True, allows selecting multiple options.
        - add_to_history: If True, adds prompt and response to conversation history.
        - examples: Few-shot examples of inputs to guide the user.
        - note: Additional note to guide the user.
        """
        if self.redundancy > 0:
            # Print prompt
            console.print(f"[bold]Prompt:[/bold] {prompt}")
            console.print(f"* Need Reason: {need_reason}")
            console.print(f"* Multiple: {multiple}")
            console.print(f"* Max Try: {max_try}")
            console.print(f"* Examples: {examples}")
            console.print(f"* Notes: {notes}")
            table = Table(title="Options")
            table.add_column("Index", justify="center", style="cyan")
            table.add_column("Option", justify="center", style="magenta")
            for i, option in enumerate(options):
                table.add_row(str(i), option)
            console.print(table)

        if not option_type:
            try:
                tmp_msg = "Now we want use LLM to choose the option from the following options: "
                for i, option in enumerate(options):
                    tmp_msg += f"{i+1}. {option}, "
                tmp_msg = tmp_msg[:-2] + "."
                tmp_msg += "\n\nWhat is the option name?"
                tmp_msg += "\nFor example, when the chooses is 'apple', 'banana', 'orange', the option type is 'fruit'."
                tmp_msg += "\nPlease provide the option type.(just one or two word)"
                option_type = self.model.invoke(tmp_msg).content
                if self.redundancy > 0:
                    console.print(
                        "Option Type is not provided. Using LLM to generate it."
                    )
                    console.print(f"[bold]Option Type:[/bold] {option_type}")
            except Exception as e:
                logger.error(f"Failed to generate option type: {str(e)}")
                option_type = "option"

        if need_reason:

            class Choice(BaseModel):
                choice: str = Field(
                    description="name: The chosen option"
                    + (
                        "(s), please separate multiple options with commas"
                        if multiple
                        else ""
                    )
                )
                reason: str = Field(description="The reason for the choice")
                args: str = Field(
                    description="The arguments for the chosen option in the format \
                    <arg1_name>:<arg1_value>,<arg2_name>:<arg2_value>..."
                    + (
                        "(s), separate multiple arguments with commas"
                        if multiple
                        else ""
                    )
                )

        else:

            class Choice(BaseModel):
                choice: str = Field(
                    description="name: The chosen option"
                    + (
                        "(s), please separate multiple options with commas"
                        if multiple
                        else ""
                    )
                )
                args: str = Field(
                    description="The arguments for the chosen option in the format \
                    <arg1_name>:<arg1_value>,<arg2_name>:<arg2_value>..."
                    + (
                        "(s), separate multiple arguments with commas"
                        if multiple
                        else ""
                    )
                )

        # Initialize LLM with structured output handling
        structured_llm = self.model.with_structured_output(Choice)
        new_prompt = prompt + "\n\n" + f"Options: {options}"
        # Add prompt details
        new_prompt += f"\nPlease choose the {option_type}"
        if need_reason:
            new_prompt += " and provide a reason"
        if multiple:
            new_prompt += " (multiple options allowed)"
        # Adding notes or few-shot examples for user guidance
        if notes:
            note_text = "\n\nConsider the following points:\n"
            for note in notes:
                note_text += f"- {note}\n"
            new_prompt += note_text
        if examples:
            few_shot_text = "\nExamples:\n" + "\n".join(examples)
            new_prompt += few_shot_text
        new_prompt += "\n\nPlease note that the arguments should be in the format <arg1_name>:<arg1_value>,<arg2_name>:<arg2_value>..."
        if add_to_history:
            self.history.append(HumanMessage(content=new_prompt))

        for attempt in range(max_try):
            try:
                response = structured_llm.invoke(new_prompt)
                if add_to_history:
                    self.history.append(response)
                choice = response.choice
                args = response.args
                if need_reason:
                    reason = response.reason
                else:
                    reason = None
                return {"choice": choice, "args": args, "reason": reason}
            except Exception as e:
                logger.error(f"Failed to choose option: {str(e)}")
                if self.redundancy > 0:
                    console.print(f"[red]Failed to choose option: {str(e)}")
                    console.print(f"[red]Attempt {attempt + 1}/{max_try}")

    def function_choose(
        self,
        functions_info,
        prompt,
        need_reason=False,
        multiple=False,
        add_to_history=False,
        max_try=3,
        examples=None,
        notes=None,
    ):
        """
        Chooses a function from a list of available functions and collects its input arguments.
        Arguments:
        - functions_info: List of dictionaries with details about each function.
        - prompt: The prompt to display to the user for function selection.
        - need_reason: If True, asks the user to provide a reason for the choice.
        - multiple: If True, allows choosing multiple functions.
        - add_to_history: If True, adds the conversation to history.
        - max_try: Maximum attempts for input validation.
        - examples: Few-shot examples to guide the user.
        - notes: Additional note to help the user.
        """
        # Generate information about available functions
        choose_info = []
        for _index, data in enumerate(functions_info, 1):
            _ = f"name: {data['name']}"
            if "description" in data:
                _ += f", description: {data['description']}"
            if "input" in data:
                _ += f", input: {', '.join(data['input'])}"
            if "input_type" in data:
                _ += f", input type: {data['input_type']}"
            if "example_input" in data:
                _ += f", example input: {data['example_input']}"
            if "output_type" in data:
                _ += f", output type: {data['output_type']}"
            if "example_output" in data:
                _ += f", example output: {data['example_output']}"
            choose_info.append(_)

        while max_try > 0:
            max_try -= 1
            if self.redundancy > 0:
                console.print("[yellow]Available functions:")
                table = Table(title="Functions")
                table.add_column("Index", justify="center", style="cyan")
                table.add_column("Function", justify="center", style="magenta")
                for i, info in enumerate(choose_info):
                    table.add_row(str(i), info)
                console.print(table)

            r = self.choose_with_args(
                choose_info,
                prompt,
                "function name and provide input for the function",
                need_reason=need_reason,
                multiple=multiple,
                add_to_history=add_to_history,
                examples=examples,
                notes=notes,
            )
            function_name, args, reason = r["choice"], r["args"], r.get("reason", None)
            if self.redundancy > 0:
                console.print(f"[green]Function name: {function_name}")
                console.print(f"[green]Arguments: {args}")
            if need_reason and self.redundancy > 0:
                console.print(f"[red]Reasons: {reason}")

            # Parse arguments
            args_list = args.split(",")
            parsed_args = {}
            for arg in args_list:
                if ":" in arg:
                    key, value = arg.split(":")
                    parsed_args[key.strip()] = value.strip()

            # Verify if all needed arguments are provided
            needed_args = []
            for data in functions_info:
                if data["name"] == function_name:
                    needed_args = data["input"]

            if set(needed_args) == set(parsed_args.keys()):
                return {
                    "function_name": function_name,
                    "args": parsed_args,
                    "reason": reason,
                }
            else:
                logger.error(
                    f"Missing or incorrect arguments for function '{function_name}'. Needed: {set(needed_args)}, Provided: {set(parsed_args.keys())}"
                )

            if max_try == 0:
                raise ValueError(
                    "Maximum attempts reached. Function selection or argument matching failed."
                )
            if self.redundancy > 0:
                console.print(
                    f"[red]Missing or incorrect arguments for function '{function_name}'. Needed: {set(needed_args)}, Provided: {set(parsed_args.keys())}"
                )
                console.print(f"[red]Attempt {max_try}/{max_try}")

    def generate_jsons(
        self,
        prompt: str,
        fields: List[Dict[str, Any]],
        add_to_history: bool = False,
        max_try: int = 3,
    ):
        """
        动态创建 Pydantic BaseModel 子类，并生成结构化 JSON 输出。

        :param prompt: 用户输入的提示
        :param fields: 字段列表，每个字段是一个字典，包含 name, type, description, example
        :param add_to_history: 是否将此次请求添加到历史记录
        :return: 语言模型生成的结构化输出
        """
        # 初始化类的字段
        while max_try > 0:
            try:
                annotations = {}
                # 检查字段格式的完整性
                for _field in fields:
                    assert "name" in _field, "Field name is required."
                    assert "type" in _field, "Field type is required."
                    assert "description" in _field, "Field description is required."
                    assert "example" in _field, "Field example is required."
                    # 动态设置字段的注解和默认值
                    annotations[_field["name"]] = (
                        str,
                        Field(
                            ...,
                            description=_field["description"]
                            + "\nFor example: "
                            + _field["example"],
                        ),
                    )
                # 使用 pydantic 的 create_model 方法动态创建模型类
                JSONModel = create_model("JSONModel", **annotations)

                # 新建一个上层class，包含一个JSONModel的list
                class JSONList(BaseModel):
                    items: List[JSONModel]

                # 生成结构化的语言模型
                if self.redundancy > 0:
                    console.print(f"[bold]Prompt:[/bold] {prompt}")
                    console.print(f"* Fields: {fields}")
                    console.print(f"* Max Try: {max_try}")
                    console.print(f"* Add to History: {add_to_history}")
                    console.print("[green]Generating JSON...")

                structured_llm = self.model.with_structured_output(JSONList)
                # 如果选择添加到历史记录，记录prompt
                if add_to_history:
                    self.history.append(HumanMessage(content=prompt))
                # 调用模型并返回结果
                response = structured_llm.invoke(prompt)
                # 保存到历史记录
                if add_to_history:
                    self.history.append(response)
            except Exception as e:
                logger.error(f"Failed to generate JSON: {str(e)}")
                max_try -= 1
                if self.redundancy > 0:
                    console.print(f"[red]Failed to generate JSON: {str(e)}")
                    console.print(f"[red]Attempt {max_try}/{max_try}")
                continue
            return response.dict()["items"]  # should be a list
        raise ValueError("Maximum attempts reached. JSON generation failed.")

    def generate_json(
        self,
        prompt: str,
        fields: List[Dict[str, Any]],
        add_to_history: bool = False,
        max_try: int = 3,
    ):
        """
        动态创建 Pydantic BaseModel 子类，并生成结构化 JSON 输出。

        :param prompt: 用户输入的提示
        :param fields: 字段列表，每个字段是一个字典，包含 name, type, description, example
        :param add_to_history: 是否将此次请求添加到历史记录
        :return: 语言模型生成的结构化输出
        """
        # 初始化类的字段
        while max_try > 0:
            try:
                annotations = {}
                # 检查字段格式的完整性
                for _field in fields:
                    assert "name" in _field, "Field name is required."
                    assert "type" in _field, "Field type is required."
                    assert "description" in _field, "Field description is required."
                    assert "example" in _field, "Field example is required."
                    # 动态设置字段的注解和默认值
                    annotations[_field["name"]] = (
                        str,
                        Field(
                            ...,
                            description=_field["description"]
                            + "\nFor example: "
                            + _field["example"],
                        ),
                    )
                # 使用 pydantic 的 create_model 方法动态创建模型类
                if self.redundancy > 0:
                    console.print(f"[bold]Prompt:[/bold] {prompt}")
                    console.print(f"* Fields: {fields}")
                    console.print(f"* Max Try: {max_try}")
                    console.print(f"* Add to History: {add_to_history}")
                    console.print("[green]Generating JSON...")
                JSONModel = create_model("JSONModel", **annotations)
                # 生成结构化的语言模型
                structured_llm = self.model.with_structured_output(JSONModel)
                # 如果选择添加到历史记录，记录prompt
                if add_to_history:
                    self.history.append({"content": prompt})
                # 调用模型并返回结果
                response = structured_llm.invoke(prompt)
                # 保存到历史记录
                if add_to_history:
                    self.history.append(response)
            except Exception as e:
                logger.error(f"Failed to generate JSON: {str(e)}")
                max_try -= 1
                if self.redundancy > 0:
                    console.print(f"[red]Failed to generate JSON: {str(e)}")
                    console.print(f"[red]Attempt {max_try}/{max_try}")
                continue
            return response.dict()  # should be a dict
        raise ValueError("Maximum attempts reached. JSON generation failed.")

    def get_code(self, text, code_type=None) -> List[str]:
        # 从text中提取 ```<code_type_item> ``` 之间的代码, 返回提取的list
        code_list = []
        if not code_type:
            code_type = ["python", "py", ""]
        for code_type_item in code_type:
            r = re.findall(rf"```{code_type_item}(.*?)```", text, re.DOTALL)
            # 获取代码内容
            for code in r:
                if code.endswith("\n"):
                    code = code[:-1]
                if code.startswith("\n"):
                    code = code[1:]
                    code_list.append(code)

                # 利用re将已提取的内容替换为空
                text = re.sub(
                    rf"```{code_type_item}(.*?)```", "", text, flags=re.DOTALL
                )
        return code_list

    def _update_token_usage(self, usage_metadata):
        self.input_tokens += usage_metadata.get("input_tokens", 0)
        self.output_tokens += usage_metadata.get("output_tokens", 0)
        self.total_tokens += usage_metadata.get("total_tokens", 0)

    def _get_or_raise(self, key, default=None):
        if default:
            logger.warning(f"Using default value: {default}")
            return default
        try:
            value = self.sql.get_data_by_id(key)
            if value is None:
                logger.warning(f"{key} is not set in the database")
                raise ValueError(
                    f"{key} is not set in the database\
                    and no default value provided"
                )
        except Exception as e:
            logger.error(f"Failed to get {key}: {str(e)}")
            raise ValueError(f"Failed to get {key}: {str(e)}") from e
        return value

    # Multi-process
    def choose_multi_process(
        self,
        options_list,
        prompt_list,
        option_type_list,
        need_reason_list,
        multiple_list,
        max_try_list,
        examples_list,
        notes_list,
        num_processes=4,
    ):
        list_lengths = [
            len(options_list),
            len(prompt_list),
            len(option_type_list),
            len(need_reason_list),
            len(multiple_list),
            len(max_try_list),
            len(examples_list),
            len(notes_list),
        ]
        if len(set(list_lengths)) != 1:
            print(f"list_lengths: {list_lengths}")
            raise ValueError("All input lists must have the same length.")
        result_list = []
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=num_processes
        ) as executor:
            future_to_index = {
                executor.submit(
                    choose_task,
                    options_list[i],
                    prompt_list[i],
                    option_type_list[i],
                    need_reason_list[i],
                    multiple_list[i],
                    max_try_list[i],
                    examples_list[i],
                    notes_list[i],
                    self.model_name,
                    self.temperature,
                    self.max_retries,
                    self.api_key,
                    self.base_url,
                ): i
                for i in range(len(options_list))
            }
            for future in concurrent.futures.as_completed(future_to_index):
                idx = future_to_index[future]
                try:
                    result = future.result()
                except Exception as exc:
                    print(f"Task {idx} generated an exception: {exc}")
                    result = None
                result_list.append((idx, result))
        result_list.sort(key=lambda x: x[0])
        return [result for _, result in result_list]

    # Multi-process
    def choose_with_args_multi_process(
        self,
        options_list,
        prompt_list,
        option_type_list,
        need_reason_list,
        multiple_list,
        examples_list,
        notes_list,
        num_processes=4,
    ):
        list_lengths = [
            len(options_list),
            len(prompt_list),
            len(option_type_list),
            len(need_reason_list),
            len(multiple_list),
            len(examples_list),
            len(notes_list),
        ]

        if len(set(list_lengths)) != 1:
            raise ValueError("All input lists must have the same length.")

        result_list = []
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=num_processes
        ) as executor:
            future_to_index = {
                executor.submit(
                    choose_with_args_task,
                    options_list[i],
                    prompt_list[i],
                    option_type_list[i],
                    need_reason_list[i],
                    multiple_list[i],
                    examples_list[i],
                    notes_list[i],
                    self.model_name,
                    self.temperature,
                    self.max_retries,
                    self.api_key,
                    self.base_url,
                ): i
                for i in range(len(options_list))
            }
            for future in concurrent.futures.as_completed(future_to_index):
                idx = future_to_index[future]
                try:
                    result = future.result()
                except Exception as exc:
                    print(f"Task {idx} generated an exception: {exc}")
                    result = None

    # Multi-process chat
    def chat_multi_process(self, message_list, role_list, num_processes=4):
        list_lengths = [len(message_list), len(role_list)]
        if len(set(list_lengths)) != 1:
            raise ValueError("All input lists must have the same length.")
        result_list = []
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=num_processes
        ) as executor:
            future_to_index = {
                executor.submit(
                    chat_task,
                    message_list[i],
                    role_list[i],
                    self.model_name,
                    self.temperature,
                    self.max_retries,
                    self.api_key,
                    self.base_url,
                ): i
                for i in range(len(message_list))
            }
            for future in concurrent.futures.as_completed(future_to_index):
                idx = future_to_index[future]
                try:
                    result = future.result()
                except Exception as exc:
                    print(f"Task {idx} generated an exception: {exc}")
                    result = None
                result_list.append((idx, result))
        result_list.sort(key=lambda x: x[0])
        return [result for _, result in result_list]

    # Use dagent_llm to evaluate content
    def analyze_content(
        self,
        content,
        dimension,
        standard,
        options,
        multiple=False,
        add_to_history=False,
        notes=[],
        examples=[],
    ):
        prompt = f"<Content to be evaluated>\n{content}<Content to be evaluated>\nBased on the above content, \
            please evaluate whether it meets the requirements for the <{dimension}> dimension, \
                \nThe evaluation criteria are:\n{standard}>"
        r = self.choose(
            options,
            prompt,
            f"Does the content meet the requirements for the {dimension} dimension?",
            need_reason=True,
            multiple=multiple,
            add_to_history=add_to_history,
            notes=notes,
            examples=examples,
        )
        result, reason = r["choice"], r["reason"]
        result = result[0] if isinstance(result, list) else result
        return result, reason


def chat_task(
    message, role, model, temperature, max_retries, api_key, base_url, init_history=[]
):
    model = ChatOpenAI(
        model=model,
        temperature=float(temperature),
        max_retries=int(max_retries),
        api_key=api_key,
        base_url=base_url,
    )
    # TODO： add init_history
    # for message in init_history:
    #     if isinstance(message, (HumanMessage, SystemMessage, AIMessage)):
    #         self.history.append(message)
    #     else:
    #         raise ValueError(f"Invalid message type: {type(message)}")

    if role == "human":
        return model.invoke([HumanMessage(content=message)])
    elif role == "ai":
        return model.invoke([AIMessage(content=message)])
    elif role == "system":
        return model.invoke([SystemMessage(content=message)])
    else:
        raise ValueError(f"Invalid role: {role}")


def choose_with_args_task(
    options,
    prompt,
    option_type,
    need_reason,
    multiple,
    examples,
    notes,
    model,
    temperature,
    max_retries,
    api_key,
    base_url,
):
    model = ChatOpenAI(
        model=model,
        temperature=float(temperature),
        max_retries=int(max_retries),
        api_key=api_key,
        base_url=base_url,
    )
    if not option_type:
        try:
            tmp_msg = (
                "Now we want use LLM to choose the option from the following options: "
            )
            for i, option in enumerate(options):
                tmp_msg += f"{i+1}. {option}, "
            tmp_msg = tmp_msg[:-2] + "."
            tmp_msg += "\n\nWhat is the option name?"
            tmp_msg += "\nFor example, when the chooses is 'apple', 'banana', 'orange', the option type is 'fruit'."
            tmp_msg += "\nPlease provide the option type.(just one or two word)"
            option_type = model.invoke(tmp_msg).content
        except Exception as e:
            logger.error(f"Failed to generate option type: {str(e)}")
            option_type = "option"
    if need_reason:

        class Choice(BaseModel):
            choice: str = Field(
                description=f"The chosen {option_type}, separate multiple choices by commas if allowed."
            )
            reason: str = Field(description="The reason for the choice.")
            args: str = Field(
                description="The arguments for the chosen option in the format <arg1_name>:<arg1_value>,<arg2_name>:<arg2_value>..."
                + ("(s), separate multiple arguments with commas" if multiple else "")
            )

    else:

        class Choice(BaseModel):
            choice: str = Field(
                description=f"The chosen {option_type}, separate multiple choices by commas if allowed."
            )
            args: str = Field(
                description="The arguments for the chosen option in the format <arg1_name>:<arg1_value>,<arg2_name>:<arg2_value>..."
                + ("(s), separate multiple arguments with commas" if multiple else "")
            )

    structured_llm = model.with_structured_output(Choice)
    new_prompt = f"{prompt}\n\nOptions: {options}"
    new_prompt += f"\n\nPlease choose the {option_type}."
    if multiple:
        new_prompt += " (Multiple selections are allowed)"
    if need_reason:
        new_prompt += " and provide a reason."
    if examples:
        example_text = "\n\nHere are some examples for reference:\n"
        for example in examples:
            example_text += f"- {example}\n"
        new_prompt += example_text
    if notes:
        note_text = "\n\nConsider the following points:\n"
        for note in notes:
            note_text += f"- {note}\n"
        new_prompt += note_text
    new_prompt += "\n\nMake sure all choices are from the provided options."
    result = []
    for attempt in range(max_try):
        response = structured_llm.invoke(new_prompt)
        choices = [
            c.strip() for c in response.choice.split(",") if c.strip() in options
        ]
        if choices:
            result = choices
            break
        else:
            logger.error(
                f"Invalid choices: {response.choice}. Attempt {attempt + 1}/{max_try}."
            )
    if not result:
        raise ValueError("Max retries reached. No valid options chosen.")
    return result, response.args


def choose_task(
    options,
    prompt,
    option_type,
    need_reason,
    multiple,
    max_try,
    examples,
    notes,
    model,
    temperature,
    max_retries,
    api_key,
    base_url,
):
    model = ChatOpenAI(
        model=model,
        temperature=float(temperature),
        max_retries=int(max_retries),
        api_key=api_key,
        base_url=base_url,
    )
    if not option_type:
        try:
            tmp_msg = (
                "Now we want use LLM to choose the option from the following options: "
            )
            for i, option in enumerate(options):
                tmp_msg += f"{i+1}. {option}, "
            tmp_msg = tmp_msg[:-2] + "."
            tmp_msg += "\n\nWhat is the option name?"
            tmp_msg += "\nFor example, when the chooses is 'apple', 'banana', 'orange', the option type is 'fruit'."
            tmp_msg += "\nPlease provide the option type.(just one or two word)"
            option_type = model.invoke(tmp_msg).content
        except Exception as e:
            logger.error(f"Failed to generate option type: {str(e)}")
            option_type = "option"
    if need_reason:

        class Choice(BaseModel):
            choice: str = Field(
                description=f"The chosen {option_type}, separate multiple choices by commas if allowed."
            )
            reason: str = Field(description="The reason for the choice.")

    else:

        class Choice(BaseModel):
            choice: str = Field(
                description=f"The chosen {option_type}, separate multiple choices by commas if allowed."
            )

    structured_llm = model.with_structured_output(Choice)
    new_prompt = f"{prompt}\n\nOptions: {options}"
    new_prompt += f"\n\nPlease choose the {option_type}."
    if multiple:
        new_prompt += " (Multiple selections are allowed)"
    if need_reason:
        new_prompt += " and provide a reason."
    if examples:
        example_text = "\n\nHere are some examples for reference:\n"
        for example in examples:
            example_text += f"- {example}\n"
        new_prompt += example_text
    if notes:
        note_text = "\n\nConsider the following points:\n"
        for note in notes:
            note_text += f"- {note}\n"
        new_prompt += note_text
    new_prompt += "\n\nMake sure all choices are from the provided options."
    result = []
    for attempt in range(max_try):
        response = structured_llm.invoke(new_prompt)
        choices = [
            c.strip() for c in response.choice.split(",") if c.strip() in options
        ]
        if choices:
            result = choices
            break
        else:
            logger.error(
                f"Invalid choices: {response.choice}. Attempt {attempt + 1}/{max_try}."
            )
    if not result:
        raise ValueError("Max retries reached. No valid options chosen.")

    if need_reason:
        reason = response.reason
        # return result,reason if multiple else result[0],reason
        return {"choice": result, "reason": reason}
    else:
        # return result if multiple else result[0]
        return {"choice": result, "reason": None}


if __name__ == "__main__":
    llm = LLM("deepseek")
    # chat stream
    r = llm.chat("Hello, how are you?",stream=True)
    print(r)