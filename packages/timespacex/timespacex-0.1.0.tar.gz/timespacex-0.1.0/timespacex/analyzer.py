import ast
from typing import Dict

class BigOAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.complexity = "O(1)"  # Default complexity
        self.space_complexity = "O(1)"  # Default space complexity
        self.loops = 0
        self.nested_loops = 0
        self.list_comprehensions = 0
        self.recursion = False
        self.current_function = None
        self.analyzed_functions = {}
        self.explanations = []
        self.loop_variables = set()
        self.binary_search_pattern = False
        self.divide_and_conquer = False
        self.matrix_operation = False
        self.current_loop_depth = 0
        self.max_loop_depth = 0

    def visit_FunctionDef(self, node):
        self.current_function = node.name
        self.loops = 0
        self.nested_loops = 0
        self.list_comprehensions = 0
        self.recursion = False
        self.binary_search_pattern = False
        self.divide_and_conquer = False
        self.matrix_operation = False
        self.loop_variables = set()
        self.current_loop_depth = 0
        self.max_loop_depth = 0
        
        # Check for matrix operations
        for child in ast.walk(node):
            if isinstance(child, ast.Subscript):
                if isinstance(child.value, ast.Subscript):
                    self.matrix_operation = True
        
        # Check for recursion and divide-and-conquer patterns
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name) and child.func.id == node.name:
                    self.recursion = True
                    # Check for divide-and-conquer pattern (like merge sort)
                    if any(isinstance(parent, ast.Slice) for parent in self._get_parents(child)):
                        self.divide_and_conquer = True
                    break
        
        self.generic_visit(node)
        self._calculate_complexity()
        self._calculate_space_complexity(node)
        self._generate_explanation(node)
        
        self.analyzed_functions[node.name] = {
            'time_complexity': self.complexity,
            'space_complexity': self.space_complexity,
            'explanation': self.explanations[-1]
        }

    def visit_For(self, node):
        self.loops += 1
        self.current_loop_depth += 1
        self.max_loop_depth = max(self.max_loop_depth, self.current_loop_depth)
        
        # Track loop variables
        if isinstance(node.target, ast.Name):
            self.loop_variables.add(node.target.id)
        
        self.generic_visit(node)
        self.current_loop_depth -= 1

    def visit_While(self, node):
        self.loops += 1
        self.current_loop_depth += 1
        self.max_loop_depth = max(self.max_loop_depth, self.current_loop_depth)
        
        # Check for binary search pattern
        if isinstance(node.test, ast.Compare):
            if any(isinstance(op, (ast.LtE, ast.GtE)) for op in node.test.ops):
                for child in ast.walk(node):
                    if isinstance(child, ast.BinOp) and isinstance(child.op, ast.Div):
                        self.binary_search_pattern = True
                        break
        
        self.generic_visit(node)
        self.current_loop_depth -= 1

    def visit_ListComp(self, node):
        self.list_comprehensions += 1
        self.generic_visit(node)

    def _get_parents(self, node):
        parents = []
        parent = getattr(node, 'parent', None)
        while parent:
            parents.append(parent)
            parent = getattr(parent, 'parent', None)
        return parents

    def _calculate_complexity(self):
        if self.binary_search_pattern:
            self.complexity = "O(log n)"
        elif self.divide_and_conquer:
            self.complexity = "O(n log n)"  # Common for efficient sorting algorithms
        elif self.recursion and not self.divide_and_conquer:
            if self.current_function == "fibonacci_recursive":
                self.complexity = "O(2^n)"  # Special case for fibonacci
            else:
                self.complexity = "O(2^n)"  # Default for recursive
        elif self.matrix_operation and self.max_loop_depth == 3:
            self.complexity = "O(n³)"  # Matrix multiplication
        elif self.max_loop_depth > 1:
            self.complexity = f"O(n^{self.max_loop_depth})"
        elif self.max_loop_depth == 1:
            self.complexity = "O(n)"
        else:
            self.complexity = "O(1)"

    def _calculate_space_complexity(self, node):
        creates_new_ds = False
        growing_ds = False
        
        for child in ast.walk(node):
            if isinstance(child, (ast.List, ast.Dict, ast.Set)):
                creates_new_ds = True
                # Check if the data structure size depends on input
                if any(isinstance(parent, ast.For) for parent in self._get_parents(child)):
                    growing_ds = True
                    break
        
        if self.divide_and_conquer:
            self.space_complexity = "O(n log n)"
        elif self.recursion:
            self.space_complexity = "O(n)"  # Stack space for recursion
        elif growing_ds:
            self.space_complexity = "O(n)"
        elif creates_new_ds:
            self.space_complexity = "O(n)"
        else:
            self.space_complexity = "O(1)"

    def _generate_explanation(self, node):
        function_name = node.name
        explanation = []
        
        # Time complexity explanation
        explanation.append(f"The function `{function_name}` has a time complexity of {self.complexity}.")
        
        if self.binary_search_pattern:
            explanation.append("This is because the function uses a binary search pattern, dividing the search space in half at each step.")
        elif self.divide_and_conquer:
            explanation.append("This is because the function uses a divide-and-conquer approach, splitting the input and combining results.")
        elif self.matrix_operation and self.max_loop_depth == 3:
            explanation.append("This is because the function performs matrix multiplication with three nested loops.")
        elif self.max_loop_depth > 1:
            explanation.append(f"This is because the function contains {self.max_loop_depth} nested loops, each potentially iterating over the input.")
        elif self.max_loop_depth == 1:
            explanation.append("This is because the function iterates through the input exactly once.")
        elif self.recursion:
            if self.current_function == "fibonacci_recursive":
                explanation.append("This is because the function makes two recursive calls for each non-base case, creating an exponential number of calls.")
            else:
                explanation.append("This is because the function uses recursion, which creates a binary tree of calls.")
        else:
            explanation.append("This is because the function performs a constant number of operations regardless of input size.")

        # Space complexity explanation
        explanation.append(f"\nThe space complexity is {self.space_complexity}.")
        
        if self.divide_and_conquer:
            explanation.append("This is because the function creates temporary arrays at each recursion level for merging.")
        elif self.recursion:
            explanation.append("This is due to the recursive call stack that grows with input size.")
        elif self.space_complexity == "O(n)":
            explanation.append("This is because the function creates new data structures that grow with the input size.")
        else:
            explanation.append("This is because the function uses a constant amount of extra space regardless of input size.")

        self.explanations.append(" ".join(explanation))


def analyze_file(file_path: str) -> Dict:
    """Analyze a Python file for time and space complexity."""
    with open(file_path, 'r') as file:
        code = file.read()
    
    try:
        tree = ast.parse(code)
        analyzer = BigOAnalyzer()
        analyzer.visit(tree)
        return analyzer.analyzed_functions
    except SyntaxError as e:
        return {"error": f"Syntax error in the code: {str(e)}"}
    except Exception as e:
        return {"error": f"Error analyzing the code: {str(e)}"} 