#!/usr/bin/env python3
"""
Interactive Terminal Chatbot
============================
A lightweight, continuous conversation loop in your terminal that streams
responses from LLMs with conversational memory, command handling, and
free cloud AI support out of the box (no account or API key required!).
"""

import sys
import os

# Ensure UTF-8 output encoding for Windows command line / PowerShell
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stdin, "reconfigure"):
            sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Gracefully import python-dotenv if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Gracefully import colorama for cross-platform terminal colors
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR_CYAN = Fore.CYAN
    COLOR_GREEN = Fore.GREEN
    COLOR_YELLOW = Fore.YELLOW
    COLOR_RED = Fore.RED
    COLOR_MAGENTA = Fore.MAGENTA
    COLOR_RESET = Style.RESET_ALL
    STYLE_BRIGHT = Style.BRIGHT
except ImportError:
    COLOR_CYAN = ""
    COLOR_GREEN = ""
    COLOR_YELLOW = ""
    COLOR_RED = ""
    COLOR_MAGENTA = ""
    COLOR_RESET = ""
    STYLE_BRIGHT = ""

# Check for OpenAI package
try:
    from openai import OpenAI, OpenAIError, AuthenticationError, RateLimitError, APIConnectionError
except ImportError:
    print(f"\n{COLOR_RED}[Error]{COLOR_RESET} The 'openai' library is not installed.")
    print("Please install dependencies by running:")
    print(f"    {COLOR_CYAN}pip install -r requirements.txt{COLOR_RESET}\n")
    sys.exit(1)


def print_banner(display_name: str) -> None:
    """Displays the welcome banner and quick commands."""
    divider = "=" * 60
    print(f"{COLOR_CYAN}{divider}{COLOR_RESET}")
    print(f"{STYLE_BRIGHT}{COLOR_CYAN}           🤖 Python AI Terminal Chatbot{COLOR_RESET}")
    print(f"{COLOR_CYAN}{divider}{COLOR_RESET}")
    print(f" AI Engine: {COLOR_GREEN}{display_name}{COLOR_RESET}")
    print(f" Commands:  Type {COLOR_YELLOW}/help{COLOR_RESET} for commands or {COLOR_YELLOW}exit{COLOR_RESET} to quit.")
    print(f"{COLOR_CYAN}{'-' * 60}{COLOR_RESET}\n")


def print_help() -> None:
    """Displays available in-chat commands."""
    print(f"\n{COLOR_MAGENTA}{STYLE_BRIGHT}Available Commands:{COLOR_RESET}")
    print(f"  {COLOR_YELLOW}/help{COLOR_RESET}             - Show this help menu")
    print(f"  {COLOR_YELLOW}/clear{COLOR_RESET} or {COLOR_YELLOW}/reset{COLOR_RESET}  - Clear conversation history and start fresh")
    print(f"  {COLOR_YELLOW}/model <name>{COLOR_RESET}     - Change current model (e.g., /model gpt-4o)")
    print(f"  {COLOR_YELLOW}/system <prompt>{COLOR_RESET}  - Update system persona / instructions")
    print(f"  {COLOR_YELLOW}/history{COLOR_RESET}          - Show current conversation message count")
    print(f"  {COLOR_YELLOW}exit{COLOR_RESET} or {COLOR_YELLOW}quit{COLOR_RESET}      - Exit the chatbot\n")


def get_client_and_config():
    """Initializes the OpenAI client and determines the appropriate AI model and backend."""
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    base_url = os.environ.get("OPENAI_BASE_URL", "").strip()

    is_placeholder = (
        not api_key or
        api_key in ("your_openai_api_key_here", "none", "free", "demo", "null")
    )

    if is_placeholder and not base_url:
        # Free AI Mode: Works without any OpenAI account or API key!
        client = OpenAI(
            base_url="https://text.pollinations.ai/openai",
            api_key="none"
        )
        raw_model = os.environ.get("OPENAI_MODEL", "openai").strip()
        model_name = "openai" if raw_model in ("gpt-4o-mini", "openai") else raw_model
        display_name = f"Free AI Cloud ({model_name}) [No Account Required]"
    else:
        # Official OpenAI API Mode
        client = OpenAI(
            api_key=api_key,
            base_url=base_url if base_url else None
        )
        model_name = os.environ.get("OPENAI_MODEL", "gpt-4o-mini").strip()
        display_name = f"OpenAI ({model_name})"

    return client, model_name, display_name


def main() -> None:
    """Main execution loop for the chatbot."""
    client, model_name, display_name = get_client_and_config()

    default_system_prompt = os.environ.get(
        "SYSTEM_PROMPT",
        "You are a helpful, friendly, and intelligent AI assistant."
    ).strip()

    # Maintain conversation history
    conversation_history = [
        {"role": "system", "content": default_system_prompt}
    ]

    print_banner(display_name)

    while True:
        try:
            # User input prompt
            user_input = input(f"{COLOR_GREEN}{STYLE_BRIGHT}You > {COLOR_RESET}").strip()

            # Skip empty inputs
            if not user_input:
                continue

            # Check exit commands
            if user_input.lower() in ("exit", "quit", "q", "/exit", "/quit"):
                print(f"\n{COLOR_CYAN}👋 Goodbye! Have a wonderful day.{COLOR_RESET}\n")
                break

            # Handle commands
            if user_input.startswith("/"):
                parts = user_input.split(maxsplit=1)
                cmd = parts[0].lower()
                arg = parts[1].strip() if len(parts) > 1 else ""

                if cmd == "/help":
                    print_help()
                    continue

                elif cmd in ("/clear", "/reset"):
                    system_msg = conversation_history[0] if conversation_history else {"role": "system", "content": default_system_prompt}
                    conversation_history = [system_msg]
                    print(f"{COLOR_YELLOW}✨ Conversation history cleared.{COLOR_RESET}\n")
                    continue

                elif cmd == "/model":
                    if not arg:
                        print(f"{COLOR_YELLOW}Current model: {model_name}. Usage: /model <model_name>{COLOR_RESET}\n")
                    else:
                        model_name = arg
                        print(f"{COLOR_YELLOW}Switched model to: {model_name}{COLOR_RESET}\n")
                    continue

                elif cmd == "/system":
                    if not arg:
                        print(f"{COLOR_YELLOW}Current system prompt:{COLOR_RESET} {conversation_history[0]['content']}\n")
                    else:
                        conversation_history[0] = {"role": "system", "content": arg}
                        print(f"{COLOR_YELLOW}System prompt updated and set as active.{COLOR_RESET}\n")
                    continue

                elif cmd == "/history":
                    turns = (len(conversation_history) - 1) // 2
                    print(f"{COLOR_CYAN}Total messages: {len(conversation_history)} ({turns} user turns){COLOR_RESET}\n")
                    continue

                else:
                    print(f"{COLOR_RED}Unknown command '{cmd}'. Type /help for available commands.{COLOR_RESET}\n")
                    continue

            # Append user message to history
            conversation_history.append({"role": "user", "content": user_input})

            # Stream the AI response
            print(f"{COLOR_CYAN}{STYLE_BRIGHT}AI > {COLOR_RESET}", end="", flush=True)

            try:
                # Try streaming first for responsive UX
                response_stream = client.chat.completions.create(
                    model=model_name,
                    messages=conversation_history,
                    stream=True
                )

                full_response = ""
                for chunk in response_stream:
                    if chunk.choices and len(chunk.choices) > 0:
                        choice = chunk.choices[0]
                        if hasattr(choice, "delta") and choice.delta and choice.delta.content:
                            delta = choice.delta.content
                            full_response += delta
                            print(delta, end="", flush=True)

                if not full_response:
                    # Fallback to non-streaming if stream yielded no chunks
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=conversation_history,
                        stream=False
                    )
                    full_response = response.choices[0].message.content or ""
                    print(full_response, end="", flush=True)

                print("\n")
                conversation_history.append({"role": "assistant", "content": full_response})

            except AuthenticationError:
                print(f"\n\n{COLOR_RED}[Authentication Error]{COLOR_RESET} Your API key appears to be invalid.")
                print("Please check your OPENAI_API_KEY setting in .env or terminal.\n")
                conversation_history.pop()

            except RateLimitError:
                print(f"\n\n{COLOR_RED}[Rate Limit / Quota Error]{COLOR_RESET} Rate limit or quota exceeded.")
                print("Please check your API plan or wait a moment.\n")
                conversation_history.pop()

            except APIConnectionError:
                print(f"\n\n{COLOR_RED}[Connection Error]{COLOR_RESET} Could not connect to AI servers.")
                print("Please check your internet connection.\n")
                conversation_history.pop()

            except OpenAIError as oe:
                print(f"\n\n{COLOR_RED}[AI API Error]{COLOR_RESET} {oe}\n")
                conversation_history.pop()

            except Exception as ex:
                print(f"\n\n{COLOR_RED}[Error]{COLOR_RESET} {ex}\n")
                conversation_history.pop()

        except KeyboardInterrupt:
            print(f"\n\n{COLOR_CYAN}Session interrupted. Type 'exit' to quit or continue chatting.{COLOR_RESET}\n")
            continue
        except EOFError:
            print(f"\n{COLOR_CYAN}👋 Goodbye!{COLOR_RESET}\n")
            break


if __name__ == "__main__":
    main()
