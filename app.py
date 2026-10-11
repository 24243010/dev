from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import ast
import operator


class CalculatorHandler(SimpleHTTPRequestHandler):

    def do_POST(self):
        if self.path != "/calculate":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(length).decode("utf-8"))
        expression = data.get("expression", "")

        try:
            result = calculate(expression)
            response = {"result": result}
        except Exception:
            response = {"error": "Invalid calculation"}

        output = json.dumps(response).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(output)))
        self.end_headers()
        self.wfile.write(output)


def calculate(expression):
    operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
    }

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.UnaryOp) and isinstance(
            node.op, (ast.UAdd, ast.USub)
        ):
            value = evaluate(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value

        if isinstance(node, ast.BinOp) and type(node.op) in operations:
            left = evaluate(node.left)
            right = evaluate(node.right)
            return operations[type(node.op)](left, right)

        raise ValueError("Invalid expression")

    tree = ast.parse(expression, mode="eval")
    result = evaluate(tree)

    if isinstance(result, float) and not __import__("math").isfinite(result):
        raise ValueError("Invalid result")

    return result


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), CalculatorHandler)
    print("Calculator server started!")
    print("Open http://localhost:8000")
    server.serve_forever()
