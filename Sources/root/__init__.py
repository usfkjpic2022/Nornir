import os
import sys
import traceback
from datetime import datetime

log_name = f"{datetime.now()}".replace(" ", "_").replace(":", "")
if not os.path.isdir("logs"):
    os.mkdir("logs")
log_file = open(f"logs/{log_name}.txt", 'w+')
sys.stdout = log_file
sys.stderr = log_file
print("Python", sys.version)
print("\nPATH {")
for l in sys.path:
    print("    "+l)
print("}\n", flush=True)


def run_python(func_name, *args, **kwargs):
    try:
        namespace = globals()
        if func_name in namespace:
            func = namespace[func_name]
        else:
            return "{\"code\": 0, \"message\": \"[from function run_python] Cannot find requested function in the module.\"}"
        result = func(*args, **kwargs)
        if result is not None:
            if not (isinstance(result, dict) and 'code' in result and 'message' in result):
                result = "{\"code\": 0, \"message\": \"%s\"}" % str(result)
            else:
                result = "{\"code\": %d, \"message\": \"%s\"}" % (result['code'], str(result['message']))
        else:
            result = "{\"code\": 0, \"message\": \"None\"}"
    except:
        message = traceback.format_exc()
        print(message)
        result = "{\"code\": 0, \"message\": \"%s\"}" % str(message)
    return result


def run_static_server(port: int = 8084):
    import static_server
    static_server.run(port)
    return "Server Terminated"
