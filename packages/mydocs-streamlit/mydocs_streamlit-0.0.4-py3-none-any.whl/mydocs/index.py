import ast
import json
import os


def listen_files(structure: list, document: list, current_path: any):
    for record in structure:
        display_name = record["display_name"]
        folder_name = record["folder_name"]
        files = record["files"]
        structure = record["structure"]

        now_path = os.path.join(current_path,folder_name)

        # print("now path is ", now_path)

        if folder_name not in document:
            document[folder_name] = {
                "display_name": display_name,
                "files":{},
                "folder":{}
            }

        # current_path = os.getcwd()

        for file in files:
            file_name = file["file_name"]
            display_name = file["display_name"]

            file_path = os.path.join(now_path,file_name)

            print("file path is ", file_path)

            with open(file_path, "r") as read_current_file:
                source_code = read_current_file.read()
                tree = ast.parse(source_code)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    function_name = node.name
                    docstring = ast.get_docstring(node)

                    if file_name not in document[folder_name]["files"]:
                        document[folder_name]["files"][file_name] = {
                            "code": repr(source_code),
                            "display_name":display_name,
                            "result":[]
                        }

                    document[folder_name]["files"][file_name]["result"].append(
                        {
                            "function_name":function_name,
                            "doc_string":docstring
                        }
                    )

        # for folder in structure:
        document[folder_name]["folder"] = listen_files(structure,document[folder_name]["folder"], now_path)
    return document


def index_start():
    functions = {"project_name": "", "data": {}}
    current_path = os.getcwd()

    print("current path ", current_path)

    FILE_OBJECT = {}
    with open(os.path.join(current_path, "document.py"), "r") as read_current_file:
        value = read_current_file.read()
        FILE_OBJECT = json.loads(value)

    print("current path ", FILE_OBJECT, current_path)

    functions["project_name"] = FILE_OBJECT["project_name"]
    files = {
        "project_name": FILE_OBJECT["project_name"],
        "files":{},
        "folder":{}
    }

    for record in FILE_OBJECT["files"]:
        file_name = record["file_name"]
        display_name = record["display_name"]

        print("final name is ", file_name, display_name)

        with open(f"{current_path}/{file_name}", "r") as file:
            source_code = file.read()
            tree = ast.parse(source_code) # design like the tree like structure.

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_name = node.name
                docstring = ast.get_docstring(node)

                if file_name not in files["files"]:
                    files["files"][file_name] = {
                        "code": repr(source_code),
                        "display_name":display_name,
                        "result":[]
                    }

                files["files"][file_name]["result"].append(
                    {
                        "function_name":function_name,
                        "doc_string":docstring
                    }
                )

    files["folder"] = listen_files(FILE_OBJECT["structure"],files["folder"],current_path)


    print("files is ", files, f"{os.path.dirname(__file__)}/functions_value.py")
    with open(f"{os.path.dirname(__file__)}/functions_value.py", "w") as wb:
        wb.write("project_dict = " + repr(files) + "\n")


if __name__ == "__main__":
    index_start()
