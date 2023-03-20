import openai
import sys
import subprocess
import ctypes

#Load your API Key
#openai.api_key_path = "C:\\Folder\\openai_key.txt"
#openai.api_key = os.getenv("OPENAI_API_KEY")

# Windows console color constants
STD_OUTPUT_HANDLE = -11
FOREGROUND_BLUE = 0x0001
FOREGROUND_GREEN = 0x0002
FOREGROUND_RED = 0x0004
FOREGROUND_INTENSITY = 0x0008
WHITE = FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY
BLUE = FOREGROUND_BLUE | FOREGROUND_INTENSITY

# Function to set console text color
def set_text_color(color):
    handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)

#function to define the ChatCompletions request, and begin a responses_cache dictionary for requests/responses which have been seen already
def chat(model, system_message):
    messages = []
    responses_cache = {}
    messages.append({"role": "system", "content": system_message})
    
    #ChatCompletion Loop
    while True:
        set_text_color(WHITE)
        user_message = input("User: ").rstrip("\n")
        
        #break the While loop
        if user_message.lower() == "exit":
            print("Goodbye!")
            break
        #Disallow empty messages
        if not user_message.strip():
            print("Please enter a non-empty message.")
            continue
            
        #build message history
        messages.append({"role": "user", "content": user_message})
        
        #Verify User input; if this query has been made of the model before, we will pull that from the response_cache dictionary
        if user_message in responses_cache:
            assistant_message = responses_cache[user_message]
        #if this hasn't been sent before, query the ChatCompletions API    
        else:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages
            )
            
            #assignment of the response text to the Assistant_Message variable, to be output to console and saved to Responses_cache dictionary
            assistant_message = response.choices[0].message['content'].strip()
            responses_cache[user_message] = assistant_message
        
        messages.append({"role": "assistant", "content": assistant_message})
        
        #Self-Documenting code? Sets text of the API Completion to blue
        set_text_color(BLUE)
        print("Assistant:", assistant_message)

    # Reset text color to white before exiting
    set_text_color(WHITE)
try:
    chat(model="gpt-3.5-turbo", system_message="You're Blue, a helpful AI. You answer everything that is asked of you.\n")
except Exception as e:
    print("An error occurred:", e)
    input("Press Enter to exit...")

#force the .py script to open a windows command console for interaction.
if __name__ == '__main__':
    subprocess.Popen('cmd.exe /K python GPT_Windows_Wrapper.py', shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
