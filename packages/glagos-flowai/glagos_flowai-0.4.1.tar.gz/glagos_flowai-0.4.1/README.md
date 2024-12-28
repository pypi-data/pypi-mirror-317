# FlowAI

G'day! FlowAI is your mate for automating development tasks using LLMs. It's a ripper CLI tool that helps you write better commit messages, pull requests, and code reviews.

## Quick Start

```bash
# Install FlowAI
pipx install glagos-flowai

# Set up your config (you'll need API keys)
flowai --init

# Generate a commit message
git diff -w --staged | flowai --prompt-file ~/flowai-prompts/prompt-commit-message.txt

# Create a pull request description
git log main..HEAD | flowai --prompt-file ~/flowai-prompts/prompt-pull-request.txt

# Get a code review
git diff -w main..HEAD | flowai --prompt-file ~/flowai-prompts/prompt-code-review.txt
```

## Required API Keys

You'll need at least one of these environment variables set:
- OpenAI: `OPENAI_API_KEY` (get it from https://platform.openai.com/api-keys)
- Anthropic: `ANTHROPIC_API_KEY` (get it from https://console.anthropic.com/settings/keys)
- Groq: `GROQ_API_KEY` (get it from https://console.groq.com/keys)
- Google: `GOOGLE_API_KEY` (get it from https://makersuite.google.com/app/apikey)
- Ollama: No key needed, but install from https://ollama.com

## Common Commands

### Git Workflow

```bash
# Generate commit message for staged changes
git diff -w --staged | flowai --prompt-file ~/flowai-prompts/prompt-commit-message.txt

# Review code changes
git diff -w main..HEAD | flowai --prompt-file ~/flowai-prompts/prompt-code-review.txt

# Create pull request description
git log main..HEAD | flowai --prompt-file ~/flowai-prompts/prompt-pull-request.txt
```

### Model Selection

```bash
# List available models
flowai --list-models

# Use a specific model
flowai --model openai:gpt-4 "Your prompt here"
flowai --model anthropic:claude-3-opus-20240229 "Your prompt here"
flowai --model groq:mixtral-8x7b-32768 "Your prompt here"
flowai --model google:gemini-pro "Your prompt here"
flowai --model ollama:codellama "Your prompt here"
```

### Context Options

```bash
# Use a file as context
flowai --context-file error.log "Analyze this error"

# Use command output as context
flowai --context-shell-command "git diff" "Review these changes"

# Use clipboard content as context
flowai --context-from-clipboard "Summarize this"
```

## Advanced Features

### Custom Prompts

Create your own prompt templates in `~/flowai-prompts/`. See [Creating Custom Prompts](docs/creating-prompts.md) for details.

```bash
# Select a prompt file interactively
flowai --select-prompt-file

# Use a custom prompt file
flowai --prompt-file ~/flowai-prompts/my-custom-prompt.txt
```

### Configuration

```bash
# Check current settings
flowai --status

# Reconfigure FlowAI
flowai --init

# Toggle streaming output
flowai --stream "Watch the response in real-time"
flowai --no-stream "Wait for complete response"
```

### Output Formatting

```bash
# Default markdown output
flowai "Format this nicely"

# Plain text output
flowai --no-markdown "Keep it simple"
```

## Troubleshooting

1. **Missing API Keys**
   - Run `flowai --init` to see which providers need API keys
   - Check the provider URLs above to get your keys
   - Add keys to your environment variables

2. **Model Issues**
   - Run `flowai --list-models` to see available models
   - Check if your chosen provider is properly configured
   - Verify your API key has access to the model

3. **Command Not Found**
   - Make sure `pipx` is installed
   - Try reinstalling: `pipx reinstall glagos-flowai`
   - Check your PATH environment variable

## Contributing

We'd love your help! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

We especially need help with:
- Adding new LLM providers
- Creating useful prompt templates
- Writing unit tests
- Improving documentation

## License

MIT License - See LICENSE file for details