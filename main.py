import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI


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
        {
            "role":"user",
            "content":args.user_prompt
        }
    ]
    chat_comp_obj = client.chat.completions.create(messages=messages,model="openrouter/free")
    response_tkn = chat_comp_obj.usage.completion_tokens
    if response_tkn == 0:
        raise ValueError("faliled prompt")
    prompt_tkn = chat_comp_obj.usage.prompt_tokens  
    response = chat_comp_obj.choices[0].message.content
    metadata = f"User prompt: {messages[0].get("content")}\n Prompt tokens: {prompt_tkn}\n Response tokens: {response_tkn}\n "
    if args.verbose:
        print(metadata)
    print(f"Response: {response}")

if __name__ == "__main__":
    main()
