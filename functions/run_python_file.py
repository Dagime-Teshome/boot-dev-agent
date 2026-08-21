import os
import subprocess
def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
        try:
                abs_wd_path = os.path.abspath(working_directory)
                abs_tr_path = os.path.normpath(os.path.join(abs_wd_path,file_path))
                valid_tr_path = os.path.commonpath([abs_wd_path,abs_tr_path]) == abs_wd_path
                
                if not valid_tr_path:
                    return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
                if not os.path.isfile(abs_tr_path):
                    return f'Error: "{file_path}" does not exist or is not a regular file'
                if not ".py" in file_path:
                     return f'Error: "{file_path}" is not a Python file'
                command = ["python", abs_tr_path]
                if args != None:
                      command.extend(args)
                completed_process = subprocess.run(command,text=True,timeout=30);
                ret_code = completed_process.returncode
                std_err = completed_process.stderr
                std_out = completed_process.stdout
                content = ""
                if ret_code != 0:
                      content += f'Process exited with code {ret_code}\n'
                if std_err == "" and std_out == "":
                      content += f'No output produced\n'
                content += f"STDOUT:{std_out}"
                content += f"STDERR:{std_err}"
                return content
        except Exception as e:
            return f'Error:{e}'