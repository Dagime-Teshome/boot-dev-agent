import os



schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "writes the content(a string passed to the function) paramteter passed to a file located specfied by the file_path parameter  (writes to a path given as a function parameter)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file path to a file we want to write to",
                },
                "content":{
                      "type":"string",
                      "description":"content we want to write on the file"
                }
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
        try:
                abs_wd_path = os.path.abspath(working_directory)
                abs_tr_path = os.path.normpath(os.path.join(abs_wd_path,file_path))
                valid_tr_path = os.path.commonpath([abs_wd_path,abs_tr_path]) == abs_wd_path
                
                if not valid_tr_path:
                   return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
                if os.path.isdir(abs_tr_path):
                    return f'Error: Cannot write to "{file_path}" as it is a directory'
                os.makedirs(os.path.dirname(abs_tr_path),exist_ok=True)
                with open(abs_tr_path,"w") as f:
                    f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception as e:
            return f'Error:{e}'