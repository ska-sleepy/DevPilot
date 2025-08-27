import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from functions.get_files_info import schema_get_files_info

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if len(sys.argv) < 2:
    print("Enter your prompt with the run script")
    sys.exit(1)

args = sys.argv[1:]
verbose_flag = False

if "--verbose" in args:
    verbose_flag = True
    args.remove("--verbose")

prompt = " ".join(args)

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents= messages,  config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt)
)


if verbose_flag:
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: + {response.usage_metadata.candidates_token_count}")

for function_call in response.function_calls:
    print(f"Calling function: {function_call.name}({function_call.args})")