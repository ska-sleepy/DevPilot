import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if len(sys.argv) < 2:
    print("Enter your prompt with the run script")
    sys.exit(1)

prompt = " ".join(sys.argv[1])
verbose_flag = False
if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
    verbose_flag = True

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]


response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents= messages
)


if verbose_flag:
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: + {response.usage_metadata.candidates_token_count}")

print(response.text)