import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

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
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
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

function_responses = []
for function_call in response.function_calls:
    function_call_result = call_function(function_call, verbose_flag)
    if (
        not function_call_result.parts
        or not function_call_result.parts[0].function_response
    ):
        raise Exception("empty function call result")
    if verbose_flag:
        print(f"-> {function_call_result.parts[0].function_response.response}")
    function_responses.append(function_call_result.parts[0])

if not function_responses:
    raise Exception("no function responses generated, exiting.")