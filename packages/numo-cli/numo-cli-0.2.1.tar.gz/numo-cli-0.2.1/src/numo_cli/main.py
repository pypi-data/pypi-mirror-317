from typing import List, Optional
import asyncio
import argparse
from numo import Numo
import os


class NumoCLI:
    def __init__(self):
        self.numo = Numo()

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system("cls" if os.name == "nt" else "clear")

    async def process_expression(self, expression: str) -> Optional[str]:
        """Process a single expression."""
        results = await self.numo.calculate([expression])
        return results[0] if results else None

    async def process_expressions(self, expressions: List[str]) -> None:
        """Process multiple expressions."""
        results = await self.numo.calculate(expressions)
        for expr, result in zip(expressions, results):
            if result:
                print(f"{expr:30} = {result}")

    async def interactive_mode(self) -> None:
        """Run in interactive mode."""
        print("Numo CLI Interactive Shell (Press Ctrl+C to exit)")
        print("Examples:")
        print(" 2 + 2")
        print(" 1 km to m")
        print(" hello in spanish")
        print(" 100 usd to eur")
        print(" list functions - Show available functions")
        print(" list variables - Show available variables")
        print(" clear - Clear the screen")
        print("-" * 40)

        while True:
            try:
                expression = input(">>> ")
                if not expression:
                    continue

                if expression.strip().lower() == "clear":
                    self.clear_screen()
                    continue

                if expression.strip().lower() == "list functions":
                    functions = self.numo.get_available_functions()
                    print("\nAvailable Functions:")
                    print("-" * 20)
                    for func in functions:
                        print(f"- {func}")
                    continue

                if expression.strip().lower() == "list variables":
                    variables = self.numo.get_available_variables()
                    print("\nAvailable Variables:")
                    print("-" * 20)
                    for var in variables:
                        print(f"- {var}")
                    continue

                result = await self.process_expression(expression)
                if result:
                    print(f"{result}")
                else:
                    print("Could not process expression")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {str(e)}")


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Numo CLI - A powerful calculator, converter, and translator"
    )
    parser.add_argument(
        "expressions",
        nargs="*",
        help="Expressions to evaluate (e.g. '2 + 2', '1 km to m', 'hello in spanish')",
    )
    args = parser.parse_args()

    cli = NumoCLI()

    try:
        if args.expressions:
            asyncio.run(cli.process_expressions(args.expressions))
        else:
            asyncio.run(cli.interactive_mode())
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    return 0


if __name__ == "__main__":
    exit(main())
