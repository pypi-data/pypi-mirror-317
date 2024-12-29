import typer
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
from rich.table import Table
import questionary
from questionary import Choice
from typing import Optional
import time
import sys
import re
import select
from difflib import get_close_matches
import shutil
from pathlib import Path
import os
if os.name == 'nt':  # Windows
    import msvcrt
import subprocess
import pyperclip
import importlib.resources as pkg_resources
import importlib.metadata
import traceback
import csv

from .config_manager import ConfigManager
from .llm_connector import LLMConnector
import flowai  # Import the package to access resources

app = typer.Typer()
console = Console()

from flowai import __version__

# Global dictionary for provider URLs
provider_urls = {
    "google": "https://ai.google.dev/gemini-api/docs/api-key",
    "anthropic": "https://docs.anthropic.com/en/api/getting-started",
    "openai": "https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key",
    "groq": "https://console.groq.com/docs/api-keys",
    "ollama": "https://www.ollama.com"
}

def get_available_models(config):
    available_models = {}
    llm_connector = LLMConnector(config)
    
    for provider in ["openai", "anthropic", "groq", "google", "ollama"]:
        models = llm_connector.get_available_models(provider)
        if models and "Error fetching models" not in models[0]:
            available_models[provider] = [f"{provider}:{model}" for model in models]
        elif provider == "ollama" and "Error fetching models" in models[0]:
            console.print(f"[yellow]Ollama is not installed. Go to {provider_urls['ollama']} to install it.[/yellow]")
        elif "No API key set" in models[0]:
            console.print(f"[yellow]No API key detected for {provider}. See {provider_urls[provider]} to set one.[/yellow]")
        elif "Error fetching models" in models[0]:
            console.print(f"[yellow]Error fetching models for {provider}. Please check your configuration.[/yellow]")
    
    return available_models

def init_config():
    config_manager = ConfigManager()
    config = config_manager.load_config()

    # Ensure all necessary keys are present with default values
    default_config = {
        'default_model': 'openai:gpt-3.5-turbo',
        'openai_api_key': '',
        'anthropic_api_key': '',
        'groq_api_key': '',
        'google_api_key': '',
        'ollama_base_url': 'http://localhost:11434',
        'stream_mode': 'true'
    }

    for key, value in default_config.items():
        if key not in config['DEFAULT']:
            config['DEFAULT'][key] = value

    current_model = config['DEFAULT']['default_model']
    current_stream_mode = config.getboolean('DEFAULT', 'stream_mode')

    console.print(Panel.fit(
        f"[bold green]Welcome to FlowAI {__version__}![/bold green]\n\n"
        "flowai is a CLI tool for multi-agent LLM tasks. It allows you to interact with "
        "various Language Models from different providers and manage complex, multi-step tasks.\n\n"
        f"[bold blue]Current configuration:[/bold blue]\n"
        f"Model: [yellow]{current_model}[/yellow]\n"
        f"Stream mode: [yellow]{'On' if current_stream_mode else 'Off'}[/yellow]"
    ))

    available_models = get_available_models(config)
    
    # Prepare choices for providers with valid API keys
    provider_choices = []
    for provider, models in available_models.items():
        if models and models[0] not in [f"{provider}:No API key set", "Error fetching models"]:
            provider_choices.append(Choice(provider, value=provider))
        elif models[0] == f"{provider}:No API key set":
            console.print(f"[yellow]No API key detected for {provider}. See {provider_urls[provider]} to set one.[/yellow]")
        elif models[0] == "Error fetching models":
            console.print(f"[yellow]Error fetching models for {provider}. Please check your configuration.[/yellow]")

    if not provider_choices:
        console.print("[bold red]No models available. Please set at least one API key and try again.[/bold red]")
        for provider, url in provider_urls.items():
            console.print(f"[yellow]For {provider}, visit: {url}[/yellow]")
        return

    # First level: Select provider
    selected_provider = questionary.select(
        "Select a provider:",
        choices=provider_choices
    ).ask()

    if not selected_provider:
        console.print("[bold red]No provider selected. Exiting configuration.[/bold red]")
        return

    # Second level: Select model from the chosen provider
    model_choices = available_models[selected_provider]
    current_model = config['DEFAULT']['default_model']
    
    default_model = questionary.select(
        f"Select a model from {selected_provider}:",
        choices=model_choices,
        default=current_model if current_model in model_choices else model_choices[0]
    ).ask()

    if not default_model:
        console.print("[bold red]No model selected. Exiting configuration.[/bold red]")
        return

    stream_mode = questionary.confirm("Enable stream mode by default?", default=config.getboolean('DEFAULT', 'stream_mode')).ask()

    # Update the config
    config['DEFAULT'] = {
        'default_model': default_model,
        'stream_mode': str(stream_mode).lower(),
        'openai_api_key': config.get('DEFAULT', 'openai_api_key', fallback=''),
        'anthropic_api_key': config.get('DEFAULT', 'anthropic_api_key', fallback=''),
        'groq_api_key': config.get('DEFAULT', 'groq_api_key', fallback=''),
        'google_api_key': config.get('DEFAULT', 'google_api_key', fallback=''),
        'ollama_base_url': config.get('DEFAULT', 'ollama_base_url', fallback='http://localhost:11434')
    }
    config_manager.save_config(config)
    console.print(f"\n[bold green]Configuration updated![/bold green]")

    console.print(f"Your config file is located at: {config_manager.config_file}")
    console.print("You can update these values by editing the file or by running 'flowai --init' again.")

    # Create flowai-prompts directory and copy template files
    prompts_dir = Path.home() / "flowai-prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy prompt files from the package resources
    prompt_files = ["prompt-commit-message.txt", "prompt-pull-request.txt", "prompt-code-review.txt", "prompt-index.txt"]
    for prompt_file in prompt_files:
        with pkg_resources.path(flowai, prompt_file) as prompt_path:
            shutil.copy(prompt_path, prompts_dir / prompt_file)
    
    console.print(f"\n[bold green]Template files copied to {prompts_dir}[/bold green]")

def is_input_available():
    if os.name == 'nt':  # Windows
        return msvcrt.kbhit()
    else:  # Unix-based systems (Mac, Linux)
        return select.select([sys.stdin], [], [], 0.0)[0]

def generate_status_table(elapsed_time):
    table = Table.grid(padding=(0, 1))
    table.add_row(
        "[bold green]Generating response...",
        f"[bold blue]Elapsed time: {elapsed_time:.3f}s"
    )
    return table

def parse_prompt_index():
    """Parse the prompt index file using proper CSV parsing to handle commas in values."""
    prompts_dir = Path.home() / "flowai-prompts"
    index_file = prompts_dir / "prompt-index.txt"
    
    if not index_file.exists():
        raise ValueError("Prompt index file not found. Please run 'flowai --init' to set up the prompts directory.")
    
    commands = {}
    with open(index_file, 'r') as f:
        # Use csv module to properly handle commas within fields
        reader = csv.DictReader(f)
        for row in reader:
            commands[row['label']] = {
                'description': row['description'],
                'context_command': row['context_command'],
                'prompt_file': row['prompt_file'].replace('~', str(Path.home()))
            }
    return commands

def handle_user_prompts(command_str):
    """Extract user prompts from command string and get user input."""
    prompt_pattern = r'\[(.*?)\]'
    matches = re.finditer(prompt_pattern, command_str)
    
    for match in matches:
        prompt_text = match.group(1)
        user_input = questionary.text(f"{prompt_text}: ").ask()
        if user_input is None:
            raise typer.Abort()
        command_str = command_str.replace(f"[{prompt_text}]", user_input)
    
    # Show the command that will be run
    if command_str:
        console.print(f"\n[bold blue]Running command:[/bold blue] [cyan]{command_str}[/cyan]\n")
    
    return command_str

def display_available_commands():
    """Display available commands in a user-friendly way using Rich."""
    try:
        commands = parse_prompt_index()
        
        console.print("\n[bold green]G'day! Here are the available FlowAI commands:[/bold green]\n")
        
        table = Table(show_header=True, header_style="bold blue", show_lines=True)
        # Set column widths: command (25%), description (35%), context (40%)
        table.add_column("Command", style="yellow", ratio=1)
        table.add_column("Description", style="white", ratio=2)
        table.add_column("Context Source", style="cyan", ratio=3)
        
        for cmd, info in commands.items():
            context_source = info['context_command']
            if '[' in context_source:
                # Use Rich's markup for highlighting
                context_source = re.sub(r'\[(.*?)\]', r'[yellow]\[\1][/yellow]', context_source)
            
            table.add_row(cmd, info['description'], context_source)
        
        console.print(table)
        console.print("\n[bold green]To use a command:[/bold green]")
        console.print("  flowai --command [purple]<command-name>[/purple]")
        console.print("\n[bold green]Example:[/bold green]")
        console.print("  flowai --command pull-request")
        console.print("\n[italic]Note: [yellow]Yellow[/yellow] highlights in Context Source indicate where you'll be prompted for input[/italic]\n")
        
    except Exception as e:
        if "Prompt index file not found" in str(e):
            console.print("[bold yellow]No commands available. Run 'flowai --init' to set up command templates.[/bold yellow]")
        else:
            raise e

def list_commands_callback(ctx: typer.Context, param: typer.CallbackParam, value: str) -> Optional[str]:
    """Callback to handle --command with no value"""
    if value is None:
        display_available_commands()
        raise typer.Exit()
    return value

@app.command()
def main(
    model: Optional[str] = typer.Option(None, help="Specify the LLM model to use"),
    list_models: bool = typer.Option(False, "--list-models", help="List available models for all providers"),
    init: bool = typer.Option(False, "--init", help="Initialize FlowAI configuration"),
    status: bool = typer.Option(False, "--status", help="Show current model and settings"),
    stream: Optional[bool] = typer.Option(None, "--stream/--no-stream", "-s/-S", help="Stream the output directly without waiting for full response"),
    context_file: Optional[str] = typer.Option(None, "--context-file", "-c", help="Path to a context file for global context"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode to display prompts"),
    version: bool = typer.Option(False, "--version", help="Show the version of FlowAI"),
    prompt_file: Optional[str] = typer.Option(None, "--prompt-file", "-p", help="Path to a file containing a detailed prompt"),
    select_prompt_file: bool = typer.Option(False, "--select-prompt-file", help="Select a prompt file from the flowai-prompts directory"),
    context_shell_command: Optional[str] = typer.Option(None, "--context-shell-command", help="Shell command to generate context"),
    context_from_clipboard: bool = typer.Option(False, "--context-from-clipboard", help="Set context from the system clipboard"),
    no_markdown: bool = typer.Option(False, "--no-markdown", help="Return the response without Markdown formatting"),
    command: Optional[str] = typer.Option(None, "--command", help="Command to run (use '--command list' to see available commands)"),
    prompt: Optional[str] = typer.Argument(None, help="The prompt to send to the LLM (optional if --prompt-file or --select-prompt-file is used)")
):
    try:
        config_manager = ConfigManager()

        if not config_manager.config_exists():
            print("It looks like this is your first time running FlowAI. Let's set it up!", file=sys.stderr)
            init_config()
            return

        if init:
            init_config()
            return

        if version:
            print(f"FlowAI version: {__version__}")
            return

        if not config_manager.config_exists():
            raise ValueError("No configuration file found. Please run 'flowai --init' to set up FlowAI.")

        config = config_manager.load_config()
        system_prompt = config_manager.get_system_prompt()

        if status:
            current_model = config.get('DEFAULT', 'default_model', fallback='Not set')
            current_stream_mode = config.getboolean('DEFAULT', 'stream_mode', fallback=True)
            print(f"Current FlowAI Status\n\nModel: {current_model}\nStream mode: {'On' if current_stream_mode else 'Off'}")
            return

        if list_models:
            print("Available models:")
            models = get_available_models(config)
            for provider, provider_models in models.items():
                print(f"\n{provider.capitalize()}:")
                if provider_models and provider_models[0] not in ["No API key set", "Error fetching models"]:
                    for model in provider_models:
                        print(f"  {model}")
            
            print("\nProviders with missing API keys or errors:")
            for provider, url in provider_urls.items():
                if provider not in models or models[provider][0] in [f"{provider}:No API key set", "Error fetching models"]:
                    print(f"{provider.capitalize()}: {url}")
            return

        # Show available commands if no input is provided
        if not any([prompt, prompt_file, select_prompt_file, command, list_models, init, status, version]):
            display_available_commands()
            return

        # Handle command listing and execution
        if command == "list":
            display_available_commands()
            return
        elif command:
            commands = parse_prompt_index()
            if command not in commands:
                console.print(f"\n[bold red]Unknown command: {command}[/bold red]\n")
                display_available_commands()
                raise typer.Exit(code=1)
            
            cmd_info = commands[command]
            
            # Handle any user prompts in the context command
            context_shell_command = handle_user_prompts(cmd_info['context_command'])
            prompt_file = cmd_info['prompt_file']
            
            # Override any existing prompt file or context command
            if prompt_file:
                prompt_file = prompt_file
            if context_shell_command:
                context_shell_command = context_shell_command

        # Check for prompt or prompt file first
        if not (prompt or prompt_file or select_prompt_file or command):
            raise ValueError("No prompt provided. Please provide a prompt, use --prompt-file, --select-prompt-file, or --command.")

        # Only validate configuration if we're not listing models or showing version/status
        if not (list_models or version or status):
            is_valid, error_message = config_manager.validate_config()
            if not is_valid:
                raise ValueError(f"Configuration error: {error_message}\nPlease run 'flowai --init' to reconfigure FlowAI.")

        model = model or config.get('DEFAULT', 'default_model')
        if not model or ':' not in model:
            raise ValueError("No valid model set. Please run 'flowai --init' or use --model to set a model.")

        provider, model_name = model.split(':', 1)
        llm_connector = LLMConnector(config, model=model, system_prompt=system_prompt)
        
        # Handle prompt file and command-line prompt
        file_prompt = ""
        if prompt_file:
            try:
                with open(prompt_file, 'r') as f:
                    file_prompt = f.read().strip()
            except FileNotFoundError:
                console.print(f"[bold red]Error: Prompt file '{prompt_file}' not found.[/bold red]")
                raise typer.Exit(code=1)
            except IOError:
                console.print(f"[bold red]Error: Unable to read prompt file '{prompt_file}'.[/bold red]")
                raise typer.Exit(code=1)
        elif select_prompt_file:
            if os.isatty(sys.stdin.fileno()):
                prompts_dir = Path.home() / "flowai-prompts"
                prompt_files = list(prompts_dir.glob("*.txt"))
                if not prompt_files:
                    console.print(f"[bold red]No prompt files found in {prompts_dir}.[/bold red]")
                    raise typer.Exit(code=1)
                prompt_file_choices = [Choice(str(file.name), value=str(file)) for file in prompt_files]
                selected_prompt_file = questionary.select(
                    "Select a prompt file:",
                    choices=prompt_file_choices
                ).ask()
                if not selected_prompt_file:
                    console.print("[bold red]No prompt file selected. Exiting.[/bold red]")
                    raise typer.Exit(code=1)
                with open(selected_prompt_file, 'r') as f:
                    file_prompt = f.read().strip()
            else:
                console.print("[bold red]Error: --select-prompt-file requires an interactive terminal.[/bold red]")
                raise typer.Exit(code=1)

        # Combine file prompt and command-line prompt
        full_prompt = file_prompt
        if prompt:
            full_prompt += f"\n\n{prompt}" if file_prompt else prompt
        
        # Check if context is required
        context_required = "{{CONTEXT}}" in full_prompt or any(keyword in full_prompt.lower() for keyword in [
            "git diff",
            "code changes",
            "analyze the changes",
            "review the code",
            "context will be provided",
            "__START_CONTEXT__"
        ])

        # Initialize context
        context = ""
        
        # Handle context_file and stdin
        if context_file:
            try:
                with open(context_file, 'r') as f:
                    context = f.read().strip()
            except FileNotFoundError:
                console.print(f"[bold red]Error: Context file '{context_file}' not found.[/bold red]")
                raise typer.Exit(code=1)
            except IOError:
                console.print(f"[bold red]Error: Unable to read context file '{context_file}'.[/bold red]")
                raise typer.Exit(code=1)

            # Check if stdin is also present
            if is_input_available():
                console.print("[bold red]Error: Cannot use both --context-file and stdin for context. Please choose one method.[/bold red]")
                raise typer.Exit(code=1)
        elif is_input_available():
            context = sys.stdin.read().strip()

        # Run the shell command and capture its output
        if context_shell_command:
            try:
                context = subprocess.check_output(f"{os.environ['SHELL']} -i -c '{context_shell_command}'", shell=True, text=True).strip()
                if context:
                    print("\n[#555555]Command output:[/#555555]", file=sys.stderr)
                    print(f"[#555555]{context}[/#555555]", file=sys.stderr)
            except subprocess.CalledProcessError as e:
                console.print(f"[bold red]Error: Failed to run shell command '{context_shell_command}'.[/bold red]")
                console.print(f"[bold red]{e}[/bold red]")
                raise typer.Exit(code=1)

        # Set context from clipboard if --context-from-clipboard is provided
        if context_from_clipboard:
            context = pyperclip.paste()

        # Check if context is required but missing
        if context_required and not context:
            console.print(Panel.fit(
                "[bold red]Error: This prompt requires context, but no context was provided![/bold red]\n\n"
                "You can provide context in several ways:\n\n"
                "[bold blue]1. Pipe content directly:[/bold blue]\n"
                "   git diff -w | flowai --prompt-file ~/flowai-prompts/prompt-commit-message.txt\n\n"
                "[bold blue]2. Use a context file:[/bold blue]\n"
                "   flowai --context-file changes.diff --prompt-file ~/flowai-prompts/prompt-commit-message.txt\n\n"
                "[bold blue]3. Use a shell command:[/bold blue]\n"
                "   flowai --context-shell-command \"git diff -w\" --prompt-file ~/flowai-prompts/prompt-commit-message.txt\n\n"
                "[bold blue]4. Use clipboard content:[/bold blue]\n"
                "   flowai --context-from-clipboard --prompt-file ~/flowai-prompts/prompt-commit-message.txt\n",
                title="Context Required",
                border_style="red"
            ))
            raise typer.Exit(code=1)

        # Initialize wrapped_context
        wrapped_context = ""

        # Check if the prompt contains the {{CONTEXT}} tag
        if "{{CONTEXT}}" in full_prompt:
            full_prompt = full_prompt.replace("{{CONTEXT}}", context)
        else:
            # If no {{CONTEXT}} tag is found, use the traditional wrapping method
            wrapped_context = f"\n\n__START_CONTEXT__\n{context}\n__END_CONTEXT__" if context else ""
            full_prompt = f"{full_prompt}{wrapped_context}"

        if debug:
            print(f"[bold blue]Using provider:[/bold blue] {provider}")
            print(f"[bold blue]Using model:[/bold blue] {model}")
            print(f"[bold blue]System Prompt:[/bold blue] {system_prompt}")
            console.print("[bold blue]Debug: Prompt sent to LLM:[/bold blue]")
            console.print(full_prompt)
            console.print("---")

        start_time = time.time()
        full_response = ""

        if stream:
            for chunk in llm_connector.send_prompt(prompt=full_prompt, debug=debug):
                sys.stdout.write(chunk)
                sys.stdout.flush()
            sys.stdout.write("\n")
            sys.stdout.flush()
        else:
            with Live(generate_status_table(0), refresh_per_second=10, transient=not debug) as live:
                for chunk in llm_connector.send_prompt(prompt=full_prompt, debug=debug):
                    full_response += chunk
                    elapsed_time = time.time() - start_time
                    live.update(generate_status_table(elapsed_time))
        
        elapsed_time = time.time() - start_time
        if debug:
            print(f"[bold blue]Total response time:[/bold blue] {elapsed_time:.3f}s", file=sys.stderr)
            print("[bold green]Response:[/bold green]\n", file=sys.stderr)
        if no_markdown:
            console.print(full_response, file=sys.stderr)
            sys.stdout.write(full_response)
            sys.stdout.flush()
        else:
            md = Markdown(full_response)
            sys.stdout.write(full_response)
            sys.stdout.flush()

        # Print model and token usage to stderr
        print(f"\n\n[#555555]Model used: {llm_connector.model} | Input tokens: {llm_connector.input_tokens} | Output tokens: {llm_connector.output_tokens} | Elapsed time: {elapsed_time:.3f}s[/#555555]", file=sys.stderr)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        if debug:
            traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    app()