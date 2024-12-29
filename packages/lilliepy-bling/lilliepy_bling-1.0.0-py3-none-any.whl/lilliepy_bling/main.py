from flask import Flask
from requests import get
import threading
import logging
import ctypes


def _server(name, func, *args):
    """
    A server utility function that runs a Flask app to execute a provided function.

    Args:
        name (str): Pass `__name__` to differentiate direct execution and imports.
        func (callable): A function that returns the result to be served.
        *args: Variable-length argument list to be passed to the function.

    Returns:
        The result of the provided function after the server processes the request.
    """
    app = Flask(__name__)
    module_name = name
    res = None
    
    logging.getLogger('werkzeug').setLevel(logging.ERROR)

    @app.route("/func")
    def index():
        nonlocal res
        res = func(*args)  
        return ""  

    @app.route("/kill")
    def kill():
        ctypes.windll.kernel32.GenerateConsoleCtrlEvent(0, 0)  
        return ""

    def req():
        get(url="http://127.0.0.1:5000/func")
        get(url="http://127.0.0.1:5000/kill")

    if module_name == "__main__":
        threading.Thread(target=req).start()
        app.run()

    return res
