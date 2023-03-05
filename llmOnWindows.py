#
# simple LLM tool for the Windows clipboard
# (c) OakMiner RBA 2023
#
# OpenAI API Key is taken from the environment variable OPENAI_API_KEY
# Run on terminal setx OPENAI_API_KEY <your key>

import os
import pyperclip
import openai
import time

class Clipboard:

    def get(self):
        return pyperclip.paste()
        
    def set(self,data):
        pyperclip.waitForNewPaste()

class LLM:
    def __init__(self, model="gpt-3.5-turbo", temperature=0.0):
        self.model = model
        self.temperature = temperature
        
    def generate(self, text):
        c = openai.ChatCompletion.create(
          model=self.model,
          messages = [
            {"role": "user", "content": text},
        ],
        )
        return c.choices[0].message.content
          
# Get API Key from environment variable or from file
openai.api_key = os.getenv("OPENAI_API_KEY")
clipboard = Clipboard()
llm = LLM()
req = 0

# Watch the clipboard for the trigger string "@@" and if you find it run through GPT 
# and write the result back to the clipboard

while True:
    txt = clipboard.get()
    if txt.startswith("@@"):
        req = req+1
        txt = txt[2:]
        out = llm.generate(txt)
        #print(out)
        pyperclip.copy(out)
    # wait 1 second
    time.sleep(1)
