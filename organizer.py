from groq import Groq
from tools import list_folder, make_folder, rename_move_file, delete_file_or_folder, get_file_info, copy_file_or_folder, get_folder_info, empty_folder
from dotenv import load_dotenv
import os
import json

# Loading environment variables from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)



tools = [
    {
    "type": "function",
    "function": {
        "name": "list_folder",
        "description": "A function to list the files in a directory(folder)",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the folder we are checking"
                }
            },
            "required": ["path"]
        }
    }
},

{
    "type": "function",
    "function": {
        "name": "make_folder",
        "description": """Function to make a folder. 
        If the folder does not exist it creates the parents and the folder. 
        If it does then it does nothin""",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path of the new directory we are creating"
                }
            },
            "required": ["path"]
        }
    }
},

{
    "type": "function",
    "function": {
        "name": "rename_move_file",
        "description": """A function to move a file from one folder or path to another.
        If the parent path does not exist for the destination, it creates it""",
        "parameters": {
            "type": "object",
            "properties": {
                "source_path": {
                    "type": "string",
                    "description": """The original path of the file we sre trying to move or rename
                    (It contains the full path and the file extension)"""
                },
                "destination": {
                    "type": "string",
                    "description": """The path of the renamed or moved file."""
                }
            },
            "required": ["source_path", "destination"]
        }
    }
},

{
    "type": "function",
    "function": {
        "name": "delete_file_or_folder",
        "description": "A function to delete a file or a folder",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path of the file or folder(directory) to be deleted"
                }
            },
            "required": ["path"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "get_file_info",
        "description": """A function that returns the stats of a file, given the path. 
        It returns {file name, file size, date modified and date created}""",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the file we are checking"
                }
            },
            "required": ["path"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "copy_file_or_folder",
        "description": "A function to copy a file or directory(folder) from a source to a destination path",
        "parameters": {
            "type": "object",
            "properties": {
                "source_path": {
                    "type": "string",
                    "description": "The path to the folder we are copying"
                },
                "destination": {
                    "type": "string",
                    "description": "The path we are copying the folder to"
                }
            },
            "required": ["source_path", "destination"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "empty_folder",
        "description": "A function to empty and remove all files and folders from a directory",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the folder we are emptying."
                }
            },
            "required": ["path"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "get_folder_info",
        "description": "A function to get information/stats of a folder like size, number of items, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the folder whose info we are trying to access."
                }
            },
            "required": ["path"]
        }
    }
}
]

def run_agent(path: str, instruction: str):
    # Set Up the messages
    messages = [
        {"role": "system", "content": "You are a file organizing agent. Organize files into appropriate subfolders. Use only valid Windows folder names — no special characters like < > : \" / \\ | ? *"},
        {"role":"user", "content": f"Instruction: {instruction}. Path: {path}"}
    ]

    # The list of available tools
    available_tools = {
        "list_folder": list_folder,
        "make_folder": make_folder,
        "rename_move_file":rename_move_file,
        "delete_file_or_folder": delete_file_or_folder,
        "get_file_info": get_file_info,
        "copy_file_or_folder": copy_file_or_folder,
        "get_folder_info": get_folder_info,
        "empty_folder": empty_folder
    }

    # The loop to run the agent
    while True:
        # Get a response from the model
        response = client.chat.completions.create(
            messages=messages,
            model="moonshotai/kimi-k2-instruct-0905",
            tools=tools
        )


        # Check if groq is done responnding or has more to do
        if response.choices[0].finish_reason == "tool_calls": # Groq's response to this is usually "tool_calls or stop"
            # Add groq's response to messages so it remembers what it was meant to do
            messages.append(response.choices[0].message)

            # Loop through each function the LLM called and call it
            for tool_call in response.choices[0].message.tool_calls:
                name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)


                # Calling the function based on the tool_call
                result = available_tools[name](**arguments)

                # Append to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": name,
                    "content": str(result)
                })
             
        else:
            print(response.choices[0].message.content)
            break