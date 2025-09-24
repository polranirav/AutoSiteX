import argparse
import sys
import traceback
from dotenv import load_dotenv

from agent.graph import agent

load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="Run engineering project planner")
    parser.add_argument("--recursion-limit", "-r", type=int, default=100,
                        help="Recursion limit for processing (default: 100)")

    args = parser.parse_args()

    try:
        # Check if stdin is available for interactive input
        import sys
        if sys.stdin.isatty():
            user_prompt = input("Enter your project prompt: ")
        else:
            # If not interactive, use a default prompt or read from stdin
            user_prompt = "Build a colourful modern todo app in html css and js"
            print(f"Using default prompt: {user_prompt}")
        
        result = agent.invoke(
            {"user_prompt": user_prompt},
            {"recursion_limit": args.recursion_limit}
        )
        print("Final State:", result)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        traceback.print_exc()
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()