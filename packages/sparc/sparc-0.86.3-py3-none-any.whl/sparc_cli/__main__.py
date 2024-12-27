import argparse
import sys
import uuid
from rich.panel import Panel
from rich.console import Console
from sparc_cli.console.formatting import print_interrupt
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from sparc_cli.env import validate_environment
from sparc_cli.tools.memory import _global_memory, get_related_files, get_memory_value
from sparc_cli.tools.human import ask_human
from sparc_cli.console.formatting import print_stage_header, print_error
from sparc_cli.agent_utils import (
    run_agent_with_retry,
    run_research_agent,
    run_planning_agent
)
from sparc_cli.prompts import (
    PLANNING_PROMPT,
    CHAT_PROMPT,
    EXPERT_PROMPT_SECTION_PLANNING,
    HUMAN_PROMPT_SECTION_PLANNING,
)
from sparc_cli.llm import initialize_llm

from sparc_cli.tool_configs import (
    get_planning_tools,
    get_chat_tools
)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='SPARC CLI - AI Agent for executing programming and research tasks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
    sparc -m "Add error handling to the database module"
    sparc -m "Explain the authentication flow" --research-only
        '''
    )
    parser.add_argument(
        '-m', '--message',
        type=str,
        help='The task or query to be executed by the agent'
    )
    parser.add_argument(
        '--research-only',
        action='store_true',
        help='Only perform research without implementation'
    )
    parser.add_argument(
        '--provider',
        type=str,
        default='anthropic',
        choices=['anthropic', 'openai', 'openrouter', 'openai-compatible'],
        help='The LLM provider to use'
    )
    parser.add_argument(
        '--model',
        type=str,
        help='The model name to use (required for non-Anthropic providers)'
    )
    parser.add_argument(
        '--cowboy-mode',
        action='store_true',
        help='Skip interactive approval for shell commands'
    )
    parser.add_argument(
        '--expert-provider',
        type=str,
        default='openai',
        choices=['anthropic', 'openai', 'openrouter', 'openai-compatible'],
        help='The LLM provider to use for expert knowledge queries (default: openai)'
    )
    parser.add_argument(
        '--expert-model',
        type=str,
        help='The model name to use for expert knowledge queries (required for non-OpenAI providers)'
    )
    parser.add_argument(
        '--hil', '-H',
        action='store_true',
        help='Enable human-in-the-loop mode, where the agent can prompt the user for additional information.'
    )
    parser.add_argument(
        '--chat',
        action='store_true',
        help='Enable chat mode with direct human interaction (implies --hil)'
    )
    
    args = parser.parse_args()
    
    # Set hil=True when chat mode is enabled
    if args.chat:
        args.hil = True
    
    # Set default model for Anthropic, require model for other providers
    if args.provider == 'anthropic':
        if not args.model:
            args.model = 'claude-3-5-sonnet-20241022'
    elif not args.model:
        parser.error(f"--model is required when using provider '{args.provider}'")
    
    # Validate expert model requirement
    if args.expert_provider != 'openai' and not args.expert_model:
        parser.error(f"--expert-model is required when using expert provider '{args.expert_provider}'")
    
    return args

# Create console instance
console = Console()

# Create individual memory objects for each agent
research_memory = MemorySaver()
planning_memory = MemorySaver()
implementation_memory = MemorySaver()


def is_informational_query() -> bool:
    """Determine if the current query is informational based on implementation_requested state."""
    return _global_memory.get('config', {}).get('research_only', False) or not is_stage_requested('implementation')

def is_stage_requested(stage: str) -> bool:
    """Check if a stage has been requested to proceed."""
    if stage == 'implementation':
        return _global_memory.get('implementation_requested', False)
    return False

def main():
    """Main entry point for the sparc command line tool."""
    try:
        args = parse_arguments()
        expert_enabled, expert_missing = validate_environment(args)  # Will exit if main env vars missing
        
        if expert_missing:
            console.print(Panel(
                f"[yellow]Expert tools disabled due to missing configuration:[/yellow]\n" + 
                "\n".join(f"- {m}" for m in expert_missing) +
                "\nSet the required environment variables or args to enable expert mode.",
                title="Expert Tools Disabled",
                style="yellow"
            ))
        
        # Create the base model after validation
        model = initialize_llm(args.provider, args.model)

        # If no message is provided, default to chat mode
        if not args.message:
            args.chat = True
            args.hil = True  # Chat mode implies hil

        # Handle chat mode
        if args.chat:
            print_stage_header("Chat Mode")
            
            # Get initial request from user
            initial_request = ask_human.invoke({"question": "What would you like help with?"})

            # Create chat agent with appropriate tools
            chat_agent = create_react_agent(
                model,
                get_chat_tools(expert_enabled=expert_enabled),
                checkpointer=MemorySaver()
            )
            
            # Run chat agent with CHAT_PROMPT
            config = {
                "configurable": {"thread_id": uuid.uuid4()},
                "recursion_limit": 100,
                "chat_mode": True,
                "cowboy_mode": args.cowboy_mode,
                "hil": True,  # Always true in chat mode
                "initial_request": initial_request
            }
            
            # Store config in global memory
            _global_memory['config'] = config
            _global_memory['config']['expert_provider'] = args.expert_provider
            _global_memory['config']['expert_model'] = args.expert_model
            
            # Run chat agent and exit
            run_agent_with_retry(chat_agent, CHAT_PROMPT.format(initial_request=initial_request), config)
            return
            
        base_task = args.message
        config = {
            "configurable": {"thread_id": uuid.uuid4()},
            "recursion_limit": 100,
            "research_only": args.research_only,
            "cowboy_mode": args.cowboy_mode
        }
    
        # Store config in global memory for access by is_informational_query
        _global_memory['config'] = config
        
        # Store model configuration
        _global_memory['config']['provider'] = args.provider
        _global_memory['config']['model'] = args.model
        
        # Store expert provider and model in config
        _global_memory['config']['expert_provider'] = args.expert_provider
        _global_memory['config']['expert_model'] = args.expert_model
        
        # Run research stage
        print_stage_header("Research Stage")
        
        run_research_agent(
            base_task,
            model,
            expert_enabled=expert_enabled,
            research_only=args.research_only,
            hil=args.hil,
            memory=research_memory,
            config=config
        )
        
        # Proceed with planning and implementation if not an informational query
        if not is_informational_query():
            # Run planning agent
            run_planning_agent(
                base_task,
                model,
                expert_enabled=expert_enabled,
                hil=args.hil,
                memory=planning_memory,
                config=config
            )

    except KeyboardInterrupt:
        print_interrupt("Operation cancelled by user")
        sys.exit(1)

if __name__ == "__main__":
    main()
