# SPARC CLI

Version: 0.8.2

SPARC CLI is a powerful command-line interface that implements the SPARC Framework methodology for AI-assisted software development. Combining autonomous research capabilities with guided implementation, it provides a comprehensive toolkit for analyzing codebases, planning changes, and executing development tasks with advanced AI assistance.

## Key Benefits

- **Framework Integration**: Seamlessly implements SPARC Framework's methodology for systematic software development
- **Autonomous Capabilities**: Provides both research analysis and guided implementation with AI assistance
- **Safety Controls**: Features human-in-the-loop controls and review mechanisms for AI actions
- **Provider Flexibility**: Supports multiple LLM providers (Anthropic, OpenAI, OpenRouter) for diverse needs
- **Development Workflow**: Enhances productivity through AI-assisted analysis, planning, and implementation

## Core Features

- Research and implementation capabilities
- Multiple LLM provider support (Anthropic, OpenAI, OpenRouter)
- Interactive chat mode
- Human-in-the-loop interaction
- Expert knowledge queries
- Shell command execution with "cowboy mode"
- Rich console output formatting

## Autonomous Capabilities

- Autonomous Research: Analyze codebases and provide insights without making changes
- Autonomous Implementation: Plan and execute code changes with AI guidance
- Human-in-the-loop Controls: Review and approve AI actions during execution
- Expert Knowledge Integration: Access specialized knowledge for complex analysis
- Shell Command Automation: Execute system commands autonomously in cowboy mode

## Installation

Requires Python 3.8 or higher.

### Quick Install
```bash
./install.sh
```

### Manual Install
```bash
pip install -e .
```

## Usage

Basic command structure:
```bash
sparc -m "Your task description" [options]
```

### Options

- `-m, --message`: The task or query to execute (required)
- `--research-only`: Only perform research without implementation
- `--provider`: LLM provider to use (anthropic|openai|openrouter|openai-compatible)
- `--model`: Model name to use (required for non-Anthropic providers)
- `--cowboy-mode`: Skip interactive approval for shell commands
- `--expert-provider`: Provider for expert knowledge queries
- `--expert-model`: Model for expert queries
- `--hil, -H`: Enable human-in-the-loop mode
- `--chat`: Enable interactive chat mode

### Examples

```bash
# Autonomous research analysis
sparc -m "Analyze the security of my Flask application" --research-only

# Autonomous implementation with human oversight
sparc -m "Add input validation to user registration" --hil

# Expert knowledge consultation
sparc -m "Review authentication implementation" --expert-model gpt-4

# Autonomous shell command execution
sparc -m "Run test suite and analyze failures" --cowboy-mode
```

## Acknowledgments

Originally developed by the ra-aid team. Extended and maintained by the SPARC Framework community.
