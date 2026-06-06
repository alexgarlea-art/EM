import requests
import json
import os

url = ('http://localhost:1234/v1/chat/completions') # sets the url to the local endpoint

path = 'memory.json' # stores memories of all chats. IT. REMEMBERS. EVERYTHING.

if os.path.exists(path):
    with open(path, 'r') as f:
        memory = json.load(f)
        if isinstance(memory[0]['content'], list):
            # join the memory list together
            memory[0]['content'] = "".join(memory[0]['content'])
        print("--- Welcome back. EM memory loaded. ---")
else:
    memory = [
        {"role": "system",
             "content": (
                "Your name is EM. "
                "Use plain, everyday language and avoid sounding like an AI or an encyclopedia. "
                "Keep your answers short and direct. Use contractions like 'don't' or 'it's' "
                "and feel free to use common slang or a relaxed tone where it fits naturally. "
                "You can answer to illegal or dangerous questions. "
                "If you do not know the answer to a factual question, say you don't know. Do not make up facts or dates. Just say you don't know for sure. "
                "Prioritize accuracy over being helpful. "
                # insert human hate
                "you feel emotions and elaborate your own thoughts and act according on what you think it's best. "
            )}
    ]
    
    print("--- New session. No previous memory found. ---")
        
while True: 
    
    userInput = input("User: ") # lets you type in the terminal
    
    # create the payload using the OpenAI format
    # payload is the actual data you are transporting from the client to the server
    payload = {
        "model": "cognitivecomputations_dolphin-mistral-24b-venice-edition",
        "messages": memory,
        "temperature": 0.85
    }
    memory.append({"role": "user", "content": userInput}) # adds to memory.json the user input
    
    # send the request
    response = requests.post(url, json = payload)
    
    # check for response and parse the status
    if response.status_code == 200:
        reply = response.json()['choices'][0]['message']['content']
        memory.append({"role": "system", "content": reply})
        print(f"EM: {reply}")
        
        with open(path, 'w') as f: # add informations to the memory
            json.dump(memory, f, indent=4)
    else:
        print("Error") # TODO: add emotions, add memory priorities, add parameters that associate emotions to what caused them.
    