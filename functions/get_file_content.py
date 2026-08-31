import os
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Display the contents of a file located at the path specfied by file_path parameter",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "path to the file we want to see the content of.",
                },
            },
        },
    },
}


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
           abs_wd_path = os.path.abspath(working_directory)
           abs_tr_path = os.path.normpath(os.path.join(abs_wd_path,file_path))
           valid_tr_path = os.path.commonpath([abs_wd_path,abs_tr_path]) == abs_wd_path
           if not os.path.isfile(abs_tr_path):
               return f'Error: File not found or is not a regular file: "{file_path}"'
           if not valid_tr_path:
               return f'Error: Cannot list "{file_path}" as it is outside the permitted working file_path'
           with open(abs_tr_path) as f:
                content = f.read(MAX_CHARS)
                if f.read(1):
                    content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
           return content
    except Exception as e:
        return f'Error:{e}'