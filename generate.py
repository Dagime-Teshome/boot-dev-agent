

def generate_content(client,messages,partools,model="openrouter/free"):
    return client.chat.completions.create(messages=messages,model=model,tools=partools) # type: ignore