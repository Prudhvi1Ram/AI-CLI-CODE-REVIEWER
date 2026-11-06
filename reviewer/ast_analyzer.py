import ast

import ast

def analyze_structure(code: str):

    tree = ast.parse(code)

    analysis = {
        "functions": [],
        "classes": [],
        "variables": [],
        "imports": [],
        "conditions": [],
        "loops": [],
        "operations": [],
        "comparisons": [],
        "function_calls": [],
        "returns": []
    }

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):
            analysis["functions"].append({
            "name": node.name,
            "line": node.lineno
    })

        elif isinstance(node, ast.ClassDef):
            analysis["classes"].append((node.name))

        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target,ast.Name):
                    analysis["variables"].append((target.id))

        elif isinstance(node, (ast.Import, ast.ImportFrom)):
             for alias in node.names:
                analysis["imports"].append({
            "name": alias.name,
            "line": node.lineno
        })

        elif isinstance(node, ast.ImportFrom):
                     analysis["imports"].append({
            "name": node.module,
            "line": node.lineno
    })

        elif isinstance(node, ast.If):
            analysis["conditions"].append({
            "condition": ast.unparse(node.test),
            "line": node.lineno
        })

        elif isinstance(node,ast.For):
            analysis["loops"].append({
            "type": "For",
            "target": ast.unparse(node.target),
            "iterable": ast.unparse(node.iter),
            "line": node.lineno
    })
        elif isinstance(node,ast.While):
              analysis["loops"].append({
            "type": "While",
            "condition": ast.unparse(node.test),
            "line": node.lineno
    })
             

        elif isinstance(node, ast.BinOp):
            analysis["operations"].append(type(node.op).__name__)

        elif isinstance(node, ast.Compare):
            for op in node.ops:
                 analysis["comparisons"].append(type(op).__name__)

            
        elif isinstance(node, ast.Call):
             analysis["function_calls"].append({
            "name": ast.unparse(node.func),
            "line": node.lineno
    })

        elif isinstance(node, ast.Return):
            value=ast.unparse(node.value) if node.value else None
            analysis["returns"].append({
            "value": ast.unparse(node.value) if node.value else None,
            "line": node.lineno
    })
        elif isinstance(node,ast.AnnAssign):
             if isinstance(node.target, ast.Name):
                analysis["variables"].append(node.target.id)
        elif isinstance(node,ast.AugAssign):
             if isinstance(node.target, ast.Name):
                analysis["variables"].append(node.target.id)
             

    return analysis


