

import os


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:

    try:
        abs_wd_path = os.path.abspath(working_directory)
        abs_tr_path = os.path.normpath(os.path.join(abs_wd_path,directory))
        valid_tr_path = os.path.commonpath([abs_wd_path,abs_tr_path]) == abs_wd_path
        if not os.path.isdir(abs_tr_path):
            return f'Error: "{directory}" is not a directory'
        if not valid_tr_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        dir_contents = os.listdir(abs_tr_path)
        return_txt = ""
        dir = directory

        return_txt += f'Result for {'current' if dir == "." else "'" + dir +"'"} directory:\n'
        for dir in dir_contents:
            return_txt += f'- {dir}: file_size={os.path.getsize(os.path.join(abs_tr_path,dir))} bytes, is_dir={os.path.isdir(os.path.join(abs_tr_path,dir))}\n'
        return return_txt
        # return f'Success: "{directory}" is within the working directory'
    except Exception as e:
        return f'Error:{e}'