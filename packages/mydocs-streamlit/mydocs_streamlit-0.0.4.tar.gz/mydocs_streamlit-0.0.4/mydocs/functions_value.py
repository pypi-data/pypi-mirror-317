project_dict = {
    "project_name": "Batch Computation",
    "files": {},
    "folder": {
        "project": {
            "display_name": "Folder One",
            "files": {
                "file.py": {
                    "code": '\'import sys\\n\\ndef testing(a:int, b:int):\\n    """\\n    Return the testing function\\n\\n    # Params\\n        a (int): variable a stores the integer value\\n        b (int): variable a stores the integer value\\n\\n    # Response:\\n        return a+b\\n\\n    """\\n    try:\\n        a = 10\\n        b = 10\\n        return a+b\\n    except Exception as error:\\n        print("The testing error is ", error,"line no is ", sys.exc_info()[-1].tb_lineno)\\n\\ndef testing01(a:int, b:int):\\n    """\\n    Return the testing function\\n\\n    # Params\\n        a (int): variable a stores the integer value\\n        b (int): variable a stores the integer value\\n\\n    # Response:\\n        return a+b\\n\\n    """\\n    try:\\n        a = 10\\n        b = 10\\n        return a+b\\n    except Exception as error:\\n        print("The testing01 error is ", error,"line no is ", sys.exc_info()[-1].tb_lineno)\\n\\n\\ndef testing02(a:int, b:int):\\n    """\\n    Return the testing function\\n\\n    # Params\\n        a (int): variable a stores the integer value\\n        b (int): variable a stores the integer value\\n\\n    # Response:\\n        return a+b\\n\\n    """\\n    try:\\n        a = 10\\n        b = 10\\n        return a+b\\n    except Exception as error:\\n        print("The testing02 error is ", error,"line no is ", sys.exc_info()[-1].tb_lineno)\\n\'',
                    "display_name": "First File",
                    "result": [
                        {
                            "function_name": "testing",
                            "doc_string": "Return the testing function\n\n# Params\n    a (int): variable a stores the integer value\n    b (int): variable a stores the integer value\n\n# Response:\n    return a+b",
                        },
                        {
                            "function_name": "testing01",
                            "doc_string": "Return the testing function\n\n# Params\n    a (int): variable a stores the integer value\n    b (int): variable a stores the integer value\n\n# Response:\n    return a+b",
                        },
                        {
                            "function_name": "testing02",
                            "doc_string": "Return the testing function\n\n# Params\n    a (int): variable a stores the integer value\n    b (int): variable a stores the integer value\n\n# Response:\n    return a+b",
                        },
                    ],
                },
                "file2.py": {
                    "code": '\'import sys\\n\\ndef testingfile(a:int, b:int):\\n    """\\n    Return the testingfile function\\n\\n    # Params\\n        a (int): variable a stores the integer value\\n        b (int): variable a stores the integer value\\n\\n    # Response:\\n        return a+b\\n\\n    """\\n    try:\\n        a = 10\\n        b = 10\\n        return a+b\\n    except Exception as error:\\n        print("The testingfile error is ", error,"line no is ", sys.exc_info()[-1].tb_lineno)\\n\\ndef testingfile01(a:int, b:int):\\n    """\\n    Return the testingfile function\\n\\n    # Params\\n        a (int): variable a stores the integer value\\n        b (int): variable a stores the integer value\\n\\n    # Response:\\n        return a+b\\n\\n    """\\n    try:\\n        a = 10\\n        b = 10\\n        return a+b\\n    except Exception as error:\\n        print("The testingfile01 error is ", error,"line no is ", sys.exc_info()[-1].tb_lineno)\\n\\n\\ndef testingfile02(a:int, b:int):\\n    """\\n    Return the testingfile function\\n\\n    # Params\\n        a (int): variable a stores the integer value\\n        b (int): variable a stores the integer value\\n\\n    # Response:\\n        return a+b\\n\\n    """\\n    try:\\n        a = 10\\n        b = 10\\n        return a+b\\n    except Exception as error:\\n        print("The testingfile02 error is ", error,"line no is ", sys.exc_info()[-1].tb_lineno)\\n\'',
                    "display_name": "Second File",
                    "result": [
                        {
                            "function_name": "testingfile",
                            "doc_string": "Return the testingfile function\n\n# Params\n    a (int): variable a stores the integer value\n    b (int): variable a stores the integer value\n\n# Response:\n    return a+b",
                        },
                        {
                            "function_name": "testingfile01",
                            "doc_string": "Return the testingfile function\n\n# Params\n    a (int): variable a stores the integer value\n    b (int): variable a stores the integer value\n\n# Response:\n    return a+b",
                        },
                        {
                            "function_name": "testingfile02",
                            "doc_string": "Return the testingfile function\n\n# Params\n    a (int): variable a stores the integer value\n    b (int): variable a stores the integer value\n\n# Response:\n    return a+b",
                        },
                    ],
                },
            },
            "folder": {
                "project1": {
                    "display_name": "Folder Two",
                    "files": {
                        "file3.py": {
                            "code": '\'import sys\\n\\ndef testingfile04(a:int, b:int):\\n    """\\n    Return the testingfile function\\n\\n    # Params\\n        a (int): variable a stores the integer value\\n        b (int): variable a stores the integer value\\n\\n    # Response:\\n        return a+b\\n\\n    """\\n    try:\\n        a = 10\\n        b = 10\\n        return a+b\\n    except Exception as error:\\n        print("The testingfile error is ", error,"line no is ", sys.exc_info()[-1].tb_lineno)\\n\\ndef testingfile041(a:int, b:int):\\n    """\\n    Return the testingfile function\\n\\n    # Params\\n        a (int): variable a stores the integer value\\n        b (int): variable a stores the integer value\\n\\n    # Response:\\n        return a+b\\n\\n    """\\n    try:\\n        a = 10\\n        b = 10\\n        return a+b\\n    except Exception as error:\\n        print("The testingfile01 error is ", error,"line no is ", sys.exc_info()[-1].tb_lineno)\\n\\n\\ndef testingfile042(a:int, b:int):\\n    """\\n    Return the testingfile function\\n\\n    # Params\\n        a (int): variable a stores the integer value\\n        b (int): variable a stores the integer value\\n\\n    # Response:\\n        return a+b\\n\\n    """\\n    try:\\n        a = 10\\n        b = 10\\n        return a+b\\n    except Exception as error:\\n        print("The testingfile02 error is ", error,"line no is ", sys.exc_info()[-1].tb_lineno)\\n\'',
                            "display_name": "Third File",
                            "result": [
                                {
                                    "function_name": "testingfile04",
                                    "doc_string": "Return the testingfile function\n\n# Params\n    a (int): variable a stores the integer value\n    b (int): variable a stores the integer value\n\n# Response:\n    return a+b",
                                },
                                {
                                    "function_name": "testingfile041",
                                    "doc_string": "Return the testingfile function\n\n# Params\n    a (int): variable a stores the integer value\n    b (int): variable a stores the integer value\n\n# Response:\n    return a+b",
                                },
                                {
                                    "function_name": "testingfile042",
                                    "doc_string": "Return the testingfile function\n\n# Params\n    a (int): variable a stores the integer value\n    b (int): variable a stores the integer value\n\n# Response:\n    return a+b",
                                },
                            ],
                        }
                    },
                    "folder": {},
                }
            },
        }
    },
}
