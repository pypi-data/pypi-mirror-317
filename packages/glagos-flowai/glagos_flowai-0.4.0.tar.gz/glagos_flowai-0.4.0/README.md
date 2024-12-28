# FlowAI

A CLI tool for multi-agent LLM tasks.

## Installation

Run `pipx install glagos-flowai`

## Upgrading
Run `pipx upgrade glagos-flowai`

## Usage

### Initialization

First, initialize FlowAI:

```sh
flowai --init
```

This will guide you through an interactive setup process, allowing you to choose your default model, stream mode, and other options using arrow keys for selection. The current settings will be displayed before the onboarding process starts, and you can preselect these values in the prompts.

### Check Current Status

To check the current status, including the model and stream mode:

```sh
flowai --status
```

### Basic Usage

To run FlowAI with a simple prompt:

```sh
flowai "Your prompt here"
```

### Model Selection

To specify a model:

```sh
flowai --model openai:gpt-4 "Your prompt here"
```

To list available models for all providers:

```sh
flowai --list-models
```

### Streaming

To stream the output directly without waiting for the full response:

```sh
flowai --stream "Your prompt here"
```

### Prompt Files

FlowAI comes pre-packaged with several prompt files designed to assist with git commit messages and pull requests.
During initial setup, these files are copied to the `~/flowai-prompts` folder. Feel free to add your own custom prompts
to this directory as well. However, avoid modifying the included template files, as they will be overwritten
during future program updates.

To select a prompt file from the `flowai-prompts` directory:

```sh
flowai --select-prompt-file
```

### Context Options

To use a context file for global context:

```sh
flowai --context-file path/to/context "Your prompt here"
```

To run a shell command to generate context:

```sh
flowai --context-shell-command "your-command" "Your prompt here"
```

To set context from the system clipboard:

```sh
flowai --context-from-clipboard "Your prompt here"
```

## Features

- **Model Selection**: Support for multiple LLM providers with dynamic model selection.
- **Interactive Setup**: User-friendly configuration process.
- **Stream Mode**: Real-time response streaming.
- **Prompt Files**: Pre-packaged and custom prompt file support.
- **Context Management**: Multiple options for providing context (file, shell command, clipboard).
- **Error Reporting**: Detailed error reporting and graceful error handling.
- **Configuration Validation**: Configuration validation to ensure correct provider-model pairing.
- **Stream Mode Override**: Ability to override and update default settings for stream mode.
- **Context Options**: Multiple options for setting context (file, shell command, clipboard).

## Supported Providers

- **OpenAI**: Dynamically fetches available models.
- **Anthropic**: Fetches available models from Anthropic API.
- **Groq**: Fetches available models from Groq API.
- **Google**: Fetches available models from Google API.
- **Ollama**: Fetches available models from local Ollama instance.

You can easily extend FlowAI to support additional providers in the future.

## Troubleshooting

If you encounter any issues while fetching models or sending prompts, FlowAI will display detailed error messages. Check your API keys and internet connection if you're having trouble connecting to a provider. If you see a configuration error, try running `flowai --init` to reconfigure FlowAI.

## Contributing

We welcome contributions from the community! If you're familiar with a model that isn't currently supported, we'd love your help in integrating it into the library. The library could also use some unit tests. Here's how you can contribute:

1. **Fork the Repository**: Start by forking the repository.
2. **Clone the Forked Repository**: Clone the forked repository to your local machine and switch into its directory.
3. **Create a New Branch**: Create a new branch for each feature or bug fix you're working on.
4. **Make Your Changes**: Make the necessary changes in the new branch.
5. **Test Your Changes**: Make sure your changes do not break any existing functionality. Add new tests if necessary.
6. **Commit and Push Your Changes**: Once you're happy with your changes, commit them and push the branch to your forked repository on GitHub.
7. **Create a Pull Request**: Navigate to the original repository and create a pull request. Explain the changes you made, why you believe they're necessary, and any other information you think might be helpful.

After you've submitted your pull request, the maintainers will review your changes. You might be asked to make some additional modifications or provide more context about your changes. Once everything is approved, your changes will be merged into the main branch.

We value all our contributors and are grateful for any time you can spare to help improve FlowAI. Happy coding!