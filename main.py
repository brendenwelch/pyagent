import os, sys
from google import genai
from google.genai import types
from dotenv import load_dotenv

from call_function import call_function, available_functions
from prompts import system_prompt


def main():
    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    if not args:
        print("AI Code Assistant")
        print("Usage: python main.py \"prompt\" [--verbose]")
        sys.exit(1)

    load_dotenv()
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    user_prompt = " ".join(args)
    if verbose:
        print(f"User prompt: {user_prompt}")
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    for i in range(20 + 1):
        if i >= 20:
            print(f"Maximum iterations (20) reached.")
            sys.exit(1)
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    function_responses = []
    for call in response.function_calls:
        call_result = call_function(call, verbose)
        if (
            not call_result.parts
            or not call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {call_result.parts[0].function_response.response}")
        function_responses.append(call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated")

    messages.append(types.Content(role="tool", parts=function_responses))


if __name__ == "__main__":
    main()
