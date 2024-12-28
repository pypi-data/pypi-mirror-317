from functions_value import project_dict
import streamlit as st
import os


funciton_name = []
navigation_files = []
PATH_OBJECT = os.path.dirname(__file__)

with open(f"{PATH_OBJECT}/main.py","r") as rb:
    lines = rb.readlines()
    lines = lines[:60]

with open(f"{PATH_OBJECT}/main.py","w") as rb:
    rb.writelines(lines)

st.header("Batch Computation", divider="gray")
for file_name in project_dict:
    codes = []
    func_name = file_name.strip(".py")
    funciton_name.append({"name": func_name,"display_name": project_dict[file_name]["display_name"]})
    function_templates = f"\ndef {func_name}():\n"
    function_templates += """
    with st.expander("Click to view/hide code"):
        st.code(eval(project_dict[file_name]["code"]))
"""
    # function_templates = ""
    for record in project_dict[file_name]["result"]:
        codes.append(f"{record['function_name']}()")
        function_templates += f"""
    def {record["function_name"]}(record = {record}):
        st.title(record["function_name"])
        st.code(record["doc_string"])
"""

    for func in codes:
        function_templates += "    " + func + "\n"

    with open(f"{PATH_OBJECT}/main.py", "a") as f:
        f.write(function_templates)

with open(f"{PATH_OBJECT}/main.py", "a") as f:
    function_templates = """
for pages in funciton_name:
    print(pages)
    func_obj = globals()[pages["name"]]
    navigation_files.append(st.Page(func_obj, title=pages["display_name"]))
pages = st.navigation(navigation_files)
pages.run()
"""
    f.write(function_templates)

# if __name__ == "__main__":
#    execute_code()
   
### DYNAMIC CODE




def index():

    with st.expander("Click to view/hide code"):
        st.code(eval(project_dict[file_name]["code"]))

    def testing(record = {'file_path': 'project/index.py', 'function_name': 'testing', 'doc_string': '@Parameters\n    a (int) : the parameter a\n    b (int) : the parameter b\n\nThis document is used for testing'}):
        st.title(record["function_name"])
        st.code(record["doc_string"])

    def testing01(record = {'file_path': 'project/index.py', 'function_name': 'testing01', 'doc_string': '@Parameters\n    a (int) : the parameter a\n    b (int) : the parameter b\n\nThis document is used for testing'}):
        st.title(record["function_name"])
        st.code(record["doc_string"])

    def testing02(record = {'file_path': 'project/index.py', 'function_name': 'testing02', 'doc_string': '@Parameters\n    a (int) : the parameter a\n    b (int) : the parameter b\n\nThis document is used for testing'}):
        st.title(record["function_name"])
        st.code(record["doc_string"])
    testing()
    testing01()
    testing02()

for pages in funciton_name:
    print(pages)
    func_obj = globals()[pages["name"]]
    navigation_files.append(st.Page(func_obj, title=pages["display_name"]))
pages = st.navigation(navigation_files)
pages.run()
