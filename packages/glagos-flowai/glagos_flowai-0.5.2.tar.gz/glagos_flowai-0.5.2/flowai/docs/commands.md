# Using and Creating Commands in FlowAI

G'day! This guide will help you understand and create custom commands in FlowAI. Commands are a ripper way to automate your common workflows without having to remember complex pipe operations and prompt file combinations.

## What Are Commands?

Commands are pre-configured combinations of:
- A context-gathering shell command
- A prompt template file
- An optional user input prompt

Instead of typing something like:
```bash
git diff -w --staged | flowai --prompt-file ~/flowai-prompts/code-review.txt "Review these changes"
```

You can simply use:
```bash
flowai --command staged-code-review
```

## Command Configuration

Commands are defined in `~/flowai-prompts/prompt-index.txt` using a CSV format:
```csv
label,description,context_command,prompt_file
"staged-code-review","Review staged changes","git diff -w --staged","~/flowai-prompts/prompt-code-review.txt"
```

Each field serves a specific purpose:
- `label`: The command name used with `--command`
- `description`: A brief explanation shown in the command list
- `context_command`: The shell command that generates the context
- `prompt_file`: The prompt template to use

## Platform-Specific Commands

FlowAI automatically handles platform compatibility by allowing commands to be prefixed with the target platform:
- `win:` for Windows-specific commands
- `unix:` for Unix-based systems (Mac/Linux)

For example:
```csv
"unix:help","Get help with using FlowAI","cat ~/.config/flowai/docs/*.md","~/flowai-prompts/prompt-help.txt"
"win:help","Get help with using FlowAI","type %USERPROFILE%\\.config\\flowai\\docs\\*.md","~/flowai-prompts/prompt-help.txt"
```

When you run a command (e.g., `flowai --command help`), FlowAI automatically selects the appropriate version for your platform. Commands without a platform prefix work on all platforms.

## Interactive Input

Commands can prompt for user input using square brackets in the `context_command`:
```csv
"blame-lines","Find who changed specific lines","git blame -L [Enter line range (e.g. 10,20)] [Enter file path]","~/flowai-prompts/blame-analysis.txt"
```

When running this command, FlowAI will:
1. Ask for the line range
2. Ask for the file path
3. Replace the bracketed text with user input
4. Run the resulting command

## Command Ideas

Here are some ripper ideas for custom commands:

### 1. Git Workflows
- `branch-summary`: Show what's been done in the current branch
  ```csv
  "branch-summary","Summarize branch changes","git log main..HEAD","~/flowai-prompts/branch-summary.txt"
  ```

- `commit-suggest`: Suggest commit message for staged changes
  ```csv
  "commit-suggest","Generate commit message","git diff --staged","~/flowai-prompts/commit-message.txt"
  ```

### 2. Code Analysis
- `complexity-check`: Analyze function complexity
  ```csv
  "complexity-check","Check code complexity","cat [Enter file path]","~/flowai-prompts/complexity-analysis.txt"
  ```

- `docstring-gen`: Generate Python docstrings
  ```csv
  "docstring-gen","Generate docstrings","cat [Enter Python file]","~/flowai-prompts/docstring-generator.txt"
  ```

### 3. Project Management
- `issue-template`: Create issue templates
  ```csv
  "issue-template","Generate issue description","echo [Describe the issue]","~/flowai-prompts/issue-template.txt"
  ```

- `sprint-summary`: Summarize sprint commits
  ```csv
  "sprint-summary","Create sprint summary","git log --since='[Days ago (e.g. 14)]' --oneline","~/flowai-prompts/sprint-summary.txt"
  ```

### 4. Documentation
- `api-docs`: Generate API documentation
  ```csv
  "api-docs","Create API docs","cat [Enter API file path]","~/flowai-prompts/api-documentation.txt"
  ```

- `changelog`: Generate changelog from commits
  ```csv
  "changelog","Create changelog","git log [Enter version range (e.g. v1.0.0..v1.1.0)]","~/flowai-prompts/changelog.txt"
  ```

### 5. Code Review
- `security-review`: Check for security issues
  ```csv
  "security-review","Review security","git diff [Enter branch/commit]","~/flowai-prompts/security-review.txt"
  ```

- `performance-check`: Analyze performance implications
  ```csv
  "performance-check","Check performance","git diff [Enter branch/commit]","~/flowai-prompts/performance-analysis.txt"
  ```

### 6. Testing
- `test-generator`: Generate unit tests
  ```csv
  "test-generator","Create unit tests","cat [Enter source file]","~/flowai-prompts/test-generator.txt"
  ```

- `test-coverage`: Analyze test coverage gaps
  ```csv
  "test-coverage","Find coverage gaps","coverage report","~/flowai-prompts/coverage-analysis.txt"
  ```

## Tips for Creating Commands

1. **Keep It Simple**
   - Start with common tasks you do frequently
   - Use descriptive command names
   - Keep descriptions clear and concise

2. **Smart Prompting**
   - Use brackets for required user input
   - Make prompt text descriptive
   - Include examples in the prompt text

3. **Context is Key**
   - Ensure context commands provide enough information
   - Consider using multiple commands with pipes
   - Test commands with different inputs

4. **Reusability**
   - Make commands generic enough to reuse
   - Use parameters for flexibility
   - Document any requirements

## Example Usage

Here's how to use some of the commands above:

```bash
# Generate docstrings for a Python file
flowai --command docstring-gen
# When prompted: Enter Python file: src/main.py

# Create a sprint summary
flowai --command sprint-summary
# When prompted: Days ago (e.g. 14): 7

# Analyze security implications of changes
flowai --command security-review
# When prompted: Enter branch/commit: feature/new-auth
```

Remember, you can always list available commands with:
```bash
flowai --command list
```

Or get details about a specific command with:
```bash
flowai --command help [command-name]
``` 