import json
import os
import sys

from .index import index_start

FILE_OBJECT = {
    "project_name": "",
    "files":[
        {
            "display_name":"",
            "file_name":""
        }
    ],
    "structure":[
        {
            "display_name":"",
            "folder_name":"",
            "files":[],
            "structure":[]
        }
    ]
}


def start_command():
    file_name = "document.py"
    file_path = os.path.join(os.getcwd(), file_name)
    if os.path.exists(file_name):
        print(f"'{file_name}' already exists, The content in the file overridden.")
    else:
        print(f"Created '{file_name}' with default content.")

    with open(file_path, "w") as wb:
        wb.write(json.dumps(FILE_OBJECT))


def run_doc():
    file_path = os.path.join(os.getcwd(), "document.py")
    if os.path.exists(file_path):
        file_path = "mydocs/index.py"
        index_start()
    else:
        print("'document.py' does not exist. Please create it with 'mypackage start'.")


def execute():
    file_name = "document.py"
    if os.path.exists(file_name):
        os.system(f"streamlit run {os.path.dirname(__file__)}/main.py")


def main():
    if len(sys.argv) < 2:
        print("Usage: mypackage <start|run|execute>")
        sys.exit(1)

    command = sys.argv[1]
    if command == "start":
        start_command()
    elif command == "run":
        run_doc()
    elif command == "execute":
        execute()
    else:
        print(f"Unknown command: {command}")
        print("Usage: mypackage <start|run>")
