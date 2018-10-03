"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
from functools import reduce

DEFAULT = "No value set"


def index():
    """ Home page for the calculator """
    return ("<h1>Welcome to the WSGI-Calculator</h1>"
            "This calculator supports the following operations:"
            "<pre>    Add</pre>"
            "<pre>    Subtract</pre>"
            "<pre>    Multiply</pre>"
            "<pre>    Divide<BR></pre>"
            "Each operation can be used by navigating to that location from this home page."
            "The operands for each operation must be supplied as additional fields in the uri.<BR>"
            "For example:<BR>"
            "<pre>    [this page]/multiply/3/5 => 15</pre>"
            "<pre>    [this page]/add/23/42 => 65</pre>")


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    return str(sum(map(int, args)))


def divide(*args):
    """ Returns a STRING with the quotient of the arguments """
    return str(reduce(lambda a, b: a / b, map(int, args)))


def multiply(*args):
    """ Returns a STRING with the product of the arguments """
    return str(reduce(lambda a, b: a * b, map(int, args)))


def subtract(*args):
    """ Returns a STRING with the difference of the arguments """
    return str(reduce(lambda a, b: a - b, map(int, args)))


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    operations = {
        "": index,
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide
    }

    path = path.strip("/").split("/")
    oper = path[0]
    args = path[1:]

    try:
        func = operations[oper]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    """ WSGI-Calculator main application """
    try:
        func, args = resolve_path(environ.get("PATH_INFO", DEFAULT))
        body = func(*args)
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except (TypeError, ValueError):
        status = "400 Bad Request"
        body = "<h1>Bad Request: Invalid operand</h1>"
    except ZeroDivisionError:
        status = "400 Bad Request"
        body = "<h1>Bad Request: Cannot divide by zero!</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    else:
        status = "200 OK"
    finally:
        headers = [("Content-type", "text/html")]
        start_response(status, headers)

    return [f"<h1>{body}</h1>".encode("utf-8")]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('localhost', 8080, application)
    server.serve_forever()
