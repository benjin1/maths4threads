import json
import random
from sympy import symbols, integrate
from sympy.printing.str import StrPrinter

# Define the integration variable
x = symbols('x')

# Custom printer to remove 1x and format x^2 instead of x**2
class CleanPrinter(StrPrinter):
    def _print_Pow(self, expr):
        base, exp = expr.as_base_exp()
        return f"{self._print(base)}^{self._print(exp)}"

    def _print_Mul(self, expr):
        coeff, rest = expr.as_coeff_Mul()
        rest_str = self._print(rest)
        if coeff == 1:
            return f"{rest_str}"
        elif coeff == -1:
            return f"-{rest_str}"
        else:
            return f"{self._print(coeff)}{rest_str}"

    def doprint(self, expr):
        return self._print(expr)

printer = CleanPrinter()

# Function to generate a random polynomial term (degree 1–4)
def generate_polynomial_term(max_degree=4):
    degree = random.randint(1, max_degree)
    coeff = random.randint(-10, 10)
    while coeff == 0:
        coeff = random.randint(-10, 10)
    return coeff * x**degree

# Generate 4000 questions
questions = []
for _ in range(4000):
    num_terms = random.randint(1, 3)
    expr = sum(generate_polynomial_term() for _ in range(num_terms))
    integral_expr = integrate(expr, x).expand()

    question_expr = printer.doprint(expr)
    answer_expr = printer.doprint(integral_expr)

    question = f"\u222B {question_expr} dx"
    answer = answer_expr

    questions.append({"question": question, "answer": answer})

# Save to a JSON file
with open("4000_integral_questions.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)
