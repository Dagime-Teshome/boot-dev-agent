import argparse
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions,call_function
from generate import generate_content


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt",type=str,help="type you command for the AI")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role":"user",
            "content":args.user_prompt
        }
    ]
    final_answer_found = False
    for _ in range(20):
        chat_comp_obj = generate_content(client,messages,available_functions)
        response_tkn = chat_comp_obj.usage.completion_tokens # pyright: ignore[reportOptionalMemberAccess]
        if response_tkn == 0:
            raise ValueError("faliled prompt")
        prompt_tkn = chat_comp_obj.usage.prompt_tokens   # pyright: ignore[reportOptionalMemberAccess]
        response = chat_comp_obj.choices[0].message.content
        message = chat_comp_obj.choices[0].message;
        metadata = f"User prompt: {messages[0].get("content")}\n Prompt tokens: {prompt_tkn}\n Response tokens: {response_tkn}\n "
        messages.append(message)
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call,args.verbose)
                if result_message['content'] == "":
                    raise ValueError("content can not be empty")
                messages.append(result_message)
        else:
            final_answer_found = True
            break
        
    if not final_answer_found:
        print("agent run of iterations");
        sys.exit(1)
    if args.verbose:
            print(metadata) # type: ignore
            print(f"-> {result_message['content']}") # type: ignore 
    print(f"Response: {response}") # type: ignore

if __name__ == "__main__":
    main()
