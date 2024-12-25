#!/bin/env python

import atexit
import click
import datetime
import os
import requests
import yaml
import json

from pathlib import Path
from prompt_toolkit import PromptSession, HTML
from prompt_toolkit.history import FileHistory
from rich.console import Console
from rich.markdown import Markdown

WORK_DIR = Path(__file__).parent
HOME = os.getenv("HOME")
CONFIG_DIR = Path(os.getenv("XDG_CONFIG_HOME"), "llmux")
DATA_DIR = Path(os.getenv("XDG_DATA_HOME"), "llmux")
SESSION_FILE = Path(
    DATA_DIR, "session-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".json"
)
HISTORY_FILE = Path(DATA_DIR, "history")
BASE_ENDPOINT = os.environ.get("OPENAI_BASE_ENDPOINT", "https://api.openai.com/v1")
ENV_VAR = "OPENAI_API_KEY"

# NOTE: Leaving out legacy models.
# https://platform.openai.com/docs/models
# https://openai.com/pricing
PRICING_RATE = {
    "o1-preview": {
        "prompt": 0.000015,
        "completion": 0.000060,
        "context_window": 128000,
    },
    "o1-preview-2024-09-12": {
        "prompt": 0.000015,
        "completion": 0.000060,
        "context_window": 128000,
    },
    "o1-mini": {"prompt": 0.000003, "completion": 0.000012, "context_window": 128000},
    "gpt-4o": {"prompt": 0.000005, "completion": 0.000015, "context_window": 128000},
    "gpt-4o-2024-08-06": {
        "prompt": 0.0000025,
        "completion": 0.00001,
        "context_window": 128000,
    },
    "gpt-4o-2024-05-13": {
        "prompt": 0.000005,
        "completion": 0.000015,
        "context_window": 128000,
    },
    "gpt-4o-mini": {
        "prompt": 0.0000015,
        "completion": 0.000006,
        "context_window": 128000,
    },
    "gpt-4o-mini-2024-07-18": {
        "prompt": 0.0000015,
        "completion": 0.000006,
        "context_window": 128000,
    },
    "gpt-4-0125-preview": {
        "prompt": 0.01,
        "completion": 0.03,
        "context_window": 128000,
        "is_legacy": True,
    },
    "gpt-4-turbo-preview": {
        "prompt": 0.01,
        "completion": 0.03,
        "context_window": 128000,
        "is_legacy": True,
    },
    "gpt-4-1106-preview": {
        "prompt": 0.01,
        "completion": 0.03,
        "context_window": 128000,
        "is_legacy": True,
    },
    "gpt-4": {
        "prompt": 0.03,
        "completion": 0.06,
        "context_window": 8192,
        "is_legacy": True,
    },
    "gpt-4-0613": {
        "prompt": 0.03,
        "completion": 0.06,
        "context_window": 8192,
        "is_legacy": True,
    },
    "gpt-4-32k": {
        "prompt": 0.06,
        "completion": 0.12,
        "context_window": 32768,
        "is_legacy": True,
    },
    "gpt-4-32k-0613": {
        "prompt": 0.06,
        "completion": 0.12,
        "context_window": 32768,
        "is_legacy": True,
    },
    "gpt-3.5-turbo-0125": {
        "prompt": 0.0005,
        "completion": 0.0015,
        "context_window": 16385,
        "is_legacy": True,
    },
    "gpt-3.5-turbo": {
        "prompt": 0.0005,
        "completion": 0.0015,
        "context_window": 4096,
        "is_legacy": True,
    },
    "gpt-3.5-turbo-1106": {
        "prompt": 0.0005,
        "completion": 0.0015,
        "context_window": 16385,
        "is_legacy": True,
    },
    "gpt-3.5-turbo-instruct": {
        "prompt": 0.0015,
        "completion": 0.002,
        "context_window": 4096,
        "is_legacy": True,
    },
    "gpt-3.5-turbo-16k": {
        "prompt": 0.0005,
        "completion": 0.0015,
        "context_window": 16385,
        "is_legacy": True,
    },
    "gpt-3.5-turbo-0613": {
        "prompt": 0.0005,
        "completion": 0.0015,
        "context_window": 4096,
        "is_legacy": True,
    },
    "gpt-3.5-turbo-16k-0613": {
        "prompt": 0.0005,
        "completion": 0.0015,
        "context_window": 16385,
        "is_legacy": True,
    },
}

# NOTE: While gpt-4-32k is not officialy tagged as legacy it makes sense to use gpt-4-turbo instead (cheaper and with larger context. Though this might not be case. Is the larger context due to summarization?

# Initialize the messages history list
# It's mandatory to pass it at each API call in order to have a conversation
messages = []
# Initialize the token counters
prompt_tokens = 0
completion_tokens = 0
# Initialize the console
console = Console()


def load_config() -> dict:
    """
    Set defaults and read config from global and local config files.
    """

    config = {
        "api-key": "",
        "model": "gpt-4o",
        "temperature": 1,
        "markdown": True,
    }

    global_config_file = Path(CONFIG_DIR, "config.yaml")
    local_config_file = Path(WORK_DIR, "llmux.yaml")

    for file in [global_config_file, local_config_file]:
        if os.path.isfile(file):
            with open(file) as config_file:
                config_overrides = yaml.load(config_file, Loader=yaml.FullLoader)
                config = {**config, **config_overrides}

    return config


def load_history_data(history_file: str) -> dict:
    """
    Read a session history json file and return its content
    """
    with open(history_file) as file:
        content = json.loads(file.read())

    return content


def get_last_save_file() -> str:
    """
    Return the timestamp of the last saved session
    """
    files = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]
    if files:
        ts = [f.replace("session-", "").replace(".json", "") for f in files]
        ts.sort()
        return ts[-1]
    return None


def init_dir(dir_path: str) -> None:
    """
    Create a directory if it doesn't exist.
    """
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def add_markdown_system_message() -> None:
    """
    Try to force ChatGPT to always respond with well formatted code blocks and tables if markdown is enabled.
    """
    instruction = "Always use code blocks with the appropriate language tags. If asked for a table always format it using Markdown syntax."
    messages.append({"role": "system", "content": instruction})


def calculate_expense(
    prompt_tokens: int,
    completion_tokens: int,
    prompt_pricing: float,
    completion_pricing: float,
) -> float:
    """
    Calculate the expense, given the number of tokens and the pricing rates
    """
    expense = ((prompt_tokens / 1000) * prompt_pricing) + (
        (completion_tokens / 1000) * completion_pricing
    )

    # Format to display in decimal notation rounded to 6 decimals
    expense = "{:.6f}".format(round(expense, 6))

    return expense


def display_expense(model: str) -> None:
    """
    Given the model used, display total tokens used and estimated expense
    """
    total_expense = calculate_expense(
        prompt_tokens,
        completion_tokens,
        PRICING_RATE[model]["prompt"],
        PRICING_RATE[model]["completion"],
    )
    console.print(
        f"\nTotal tokens used: [green bold]{prompt_tokens + completion_tokens}"
    )
    console.print(f"Estimated expense: [green bold]${total_expense}")


def start_prompt(session: PromptSession, config: dict) -> None:
    """
    Ask the user for input, build the request and perform it
    """

    # TODO: Refactor to avoid a global variables
    global prompt_tokens, completion_tokens

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['api-key']}",
    }

    message = session.prompt(HTML(f"<b>[{prompt_tokens + completion_tokens}] >>> </b>"))

    if message.lower().strip() == "/q":
        raise EOFError
    if message.lower() == "":
        raise KeyboardInterrupt

    messages.append({"role": "user", "content": message})

    # Base body parameters
    body = {
        "model": config["model"],
        "temperature": config["temperature"],
        "messages": messages,
    }
    # Optional parameter
    if "context_window" in config:
        body["context_window"] = config["context_window"]

    try:
        r = requests.post(
            f"{BASE_ENDPOINT}/chat/completions", headers=headers, json=body
        )
    except requests.ConnectionError:
        console.print("Connection error, try again...", style="red bold")
        messages.pop()
        raise KeyboardInterrupt
    except requests.Timeout:
        console.print("Connection timed out, try again...", style="red bold")
        messages.pop()
        raise KeyboardInterrupt

    if r.status_code == 200:
        response = r.json()

        message_response = response["choices"][0]["message"]
        usage_response = response["usage"]

        console.line()
        if config["markdown"]:
            console.print(Markdown(message_response["content"].strip()))
        else:
            console.print(message_response["content"].strip())
        console.line()

        # Update message history and token counters
        messages.append(message_response)
        prompt_tokens += usage_response["prompt_tokens"]
        completion_tokens += usage_response["completion_tokens"]
        with open(os.path.join(DATA_DIR, SESSION_FILE), "w") as f:
            json.dump(
                {
                    "model": config["model"],
                    "messages": messages,
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                },
                f,
                indent=4,
            )

    elif r.status_code == 400:
        response = r.json()
        if "error" in response:
            if response["error"]["code"] == "context_length_exceeded":
                console.print("Maximum context length exceeded", style="red bold")
                raise EOFError
                # TODO: Develop a better strategy to manage this case
        console.print("Invalid request", style="bold red")
        raise EOFError

    elif r.status_code == 401:
        console.print("Invalid API Key", style="bold red")
        raise EOFError

    elif r.status_code == 429:
        console.print("Rate limit or maximum monthly limit exceeded", style="bold red")
        messages.pop()
        raise KeyboardInterrupt

    elif r.status_code == 502 or r.status_code == 503:
        console.print("The server seems to be overloaded, try again", style="bold red")
        messages.pop()
        raise KeyboardInterrupt

    else:
        console.print(f"Unknown error, status code {r.status_code}", style="bold red")
        console.print(r.json())
        raise EOFError


@click.command()
@click.option(
    "-c",
    "--context",
    "context",
    type=click.File("r"),
    help="Path to a context file",
    multiple=True,
)
@click.option("-k", "--key", "api_key", help="Set the API Key")
@click.option("-m", "--model", "model", help="Set the model")
@click.option(
    "-ml", "--multiline", "multiline", is_flag=True, help="Use the multiline input mode"
)
@click.option(
    "-r",
    "--restore",
    "restore",
    help="Restore a previous chat session (input format: YYYYMMDD-hhmmss or 'last')",
)
def main(context, api_key, model, multiline, restore) -> None:
    console.print("ChatGPT CLI", style="bold")

    init_dir(DATA_DIR)

    history = FileHistory(HISTORY_FILE)

    if multiline:
        session = PromptSession(history=history, multiline=True)
    else:
        session = PromptSession(history=history)

    config = load_config()

    # Order of precedence for API Key configuration:
    # Command line option > Environment variable > Configuration file

    # If the environment variable is set overwrite the configuration
    if os.environ.get(ENV_VAR):
        config["api-key"] = os.environ[ENV_VAR].strip()
    # If the --key command line argument is used overwrite the configuration
    if api_key:
        config["api-key"] = api_key.strip()
    # If the --model command line argument is used overwrite the configuration
    if model:
        config["model"] = model.strip()

    # Run the display expense function when exiting the script
    atexit.register(display_expense, model=config["model"])

    console.print(f"Model in use: [green bold]{config['model']}")

    # Add the system message for code blocks in case markdown is enabled in the config file
    if config["markdown"]:
        add_markdown_system_message()

    # Context from the command line option
    if context:
        for c in context:
            console.print(f"Context file: [green bold]{c.name}")
            messages.append({"role": "system", "content": c.read().strip()})

    # Restore a previous session
    if restore:
        if restore == "last":
            last_session = get_last_save_file()
            restore_file = f"llmux-session-{last_session}.json"
        else:
            restore_file = f"llmux-session-{restore}.json"
        try:
            global prompt_tokens, completion_tokens
            # If this feature is used --context is cleared
            messages.clear()
            history_data = load_history_data(os.path.join(DATA_DIR, restore_file))
            for message in history_data["messages"]:
                messages.append(message)
            prompt_tokens += history_data["prompt_tokens"]
            completion_tokens += history_data["completion_tokens"]
            console.print(f"Restored session: [bold green]{restore}")
        except FileNotFoundError:
            console.print(f"[red bold]File {restore_file} not found")

    console.rule()

    while True:
        try:
            start_prompt(session, config)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break


if __name__ == "__main__":
    main()
