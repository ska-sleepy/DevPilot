import os
import sys
import traceback
from groq import Groq
from dotenv import load_dotenv
from config import system_prompt, working_directory
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function


def main():
    load_dotenv()

    api_key = os.environ.get("Groq_API_KEY")
    client = Groq(api_key=api_key)

    verbose_flag = "--verbose" in sys.argv

    available_tools = [
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]

    messages = [
        {"role": "system", "content": system_prompt},
    ]

    print(f"DevPilot (working dir: {working_directory}) — type 'exit' to quit")

    while True:
        try:
            prompt = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not prompt:
            continue
        if prompt.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        messages.append({"role": "user", "content": prompt})

        for i in range(20):
            try:
                response = client.chat.completions.create(
                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                    messages=messages,
                    tools=available_tools,
                )

                message = response.choices[0].message
                messages.append(message)

                if message.tool_calls:
                    for tool_call in message.tool_calls:
                        result = call_function(tool_call, verbose_flag)
                        if verbose_flag:
                            print(f"-> {result}")
                        else:
                            print("...", end="", flush=True)
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": str(result),
                        })
                    continue

                elif message.content:
                    print(f"\nDevPilot: {message.content}")
                    break

            except Exception as e:
                print(f"Error: {e}")
                if verbose_flag:
                    traceback.print_exc()
                break


if __name__ == "__main__":
    main()
