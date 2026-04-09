import google.generativeai as genai
import os
from tools import get_time,create_file,read_file,edit_file,delete_file
# Replace with your API key
genai.configure(api_key=os.environ['GEMINI_API_KEY'])
try:
    tools_map={
        "get_time":get_time,
        "create_file":create_file,
        "edit_file": edit_file,
        "read_file": read_file,
        "delete_file": delete_file
    }
    tools = [{
        "function_declarations": [
            {
                "name": "get_time",
                "description": "Get the current time for a city",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "The name of the city"
                        }
                    },
                    "required": ["city"]
                }
            },
            {
                "name": "create_file",
                "description": "Create a file that has is created containing the text new file You can only create files that hold text",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_name": {
                            "type": "string",
                            "description": "The name of the file"
                        },
                        "file_type":{
                            "type": "string",
                            "description": "The type of file it is"
                        }
                    },
                    "required": ["file_name","file_type"]
                }
            },
            {
                "name": "read_file",
                "description": "Read the content of a file the user has given you access to.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_name": {
                            "type": "string",
                            "description": "The name of the file"
                        },
                        "file_type":{
                            "type": "string",
                            "description": "The type of file it is"
                        }
                    },
                    "required": ["file_name","file_type"]
                }
            },
            {
                "name": "edit_file",
                "description": "Edit the content of a file, Always run read_file once before editing a file. You will need to send the ENTIRE content of the file along with the edits, Meaning the file will be overwritten by your change.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_name": {
                            "type": "string",
                            "description": "The name of the file"
                        },
                        "file_type":{
                            "type": "string",
                            "description": "The type of file it is"
                        },
                        "content":
                        {
                            "type": "string",
                            "description":"The content that you will enter into the file This content will overwrite whats currently in the file so you need to send ALL of the content that needs to be added to the file."
                        }
                    },
                    "required": ["file_name","file_type","content"]
                }
            },
            {
                "name": "delete_file",
                "description": "Delete a file and all its contents",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_name": {
                            "type": "string",
                            "description": "The name of the file"
                        },
                        "file_type":{
                            "type": "string",
                            "description": "The type of file it is"
                        }
                    },
                    "required": ["file_name","file_type"]
                }
            }
        ]
    }]
    with open("transcription.txt","r", encoding="utf-8") as f:
        text=f.read()
        print(text)
    model = genai.GenerativeModel("models/gemini-2.5-flash",tools=tools,system_instruction=
                                                            """When you call a tool and receive the result:
                                                            - Use the result to answer the question
                                                            - Do NOT call the same tool again unless absolutely necessary""")
    chat= model.start_chat()
    response=chat.send_message(text)
    last_func=None
    for _ in range(5):
        has_function_call = any(hasattr(part, "function_call") for part in response.candidates[0].content.parts)
        print('test')
        # print(has_function_call)
        # print(response.candidates[0].content.parts[0])
        # print(hasattr(response.candidates[0].content.parts[0],"text"))
        # print(type(response.candidates[0].content.parts))
        # if not response.candidates[0].content.parts or not response.candidates[0].content or not hasattr(response.candidates[0].content.parts,"function_call"):
        #     print("No parts")
        #     print(response.text)
        #     break
        if response.candidates[0].content.parts[0].text:
            print(response.text)
            break
        for part in response.candidates[0].content.parts:
            if hasattr(part, "function_call"):
                has_function_call = True
                func_name = part.function_call.name
                func = tools_map.get(func_name)
                args = dict(part.function_call.args)

                print("Function call:", func_name, args)
                if last_func == func_name:
                    print("Repeated function call detected")

                    response = chat.send_message(
                        "You already have the file content. Do not call the tool again. "
                        "Explain what is in the file."
                    )

                    has_function_call = False
                    break
                if func:
                    result = func(**args)
                    response = chat.send_message(
                        {
                            "function_response": {
                                "name": func_name,
                                "response": {"content": result}
                            }
                        }
                    )
                    last_func= func_name
                    break 
except Exception as e:
    print("Error:", e)

input("Press Enter to exit...")
