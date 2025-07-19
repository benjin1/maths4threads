import random
import json
from sympy import symbols, expand, Mul, Add
from sympy.abc import x


def generate_advanced_algebra_questions(n):
    # Format factorized expressions like x*(x - 1)*(x + 2) as x(x-1)(x+2)
    def format_factorized_expr(expr):
        if isinstance(expr, Mul):
            parts = []
            for arg in expr.args:
                if arg == x:
                    parts.append("x")
                elif isinstance(arg, Add):
                    parts.append(f"({str(arg).replace('**', '^')})")
                else:
                    parts.append(str(arg).replace("**", "^"))
            return "".join(parts)
        else:
            return str(expr).replace("**", "^")

    # Generate a random factorized expression
    def generate_factorized_expression():
        expr = 1
        num_factors = random.randint(2, 4)
        used_roots = set()
        
        while len(used_roots) < num_factors:
            root = random.randint(-5, 5)
            if root != 0 and root not in used_roots:
                used_roots.add(root)
                expr *= (x - root)
        
        return expr

    # Generate n "Expand and simplify" questions
    questions = []

    for _ in range(n):
        num_terms = random.randint(2, 4)
        terms = []

        for _ in range(num_terms):
            coeff = random.choice([1, x])
            term = coeff * generate_factorized_expression()
            terms.append(term)

        full_expr = sum(terms)
        question_expr = " + ".join([format_factorized_expr(term) for term in terms])
        expanded_expr = expand(full_expr)  # Fully expand without simplify()

        questions.append({
            "question": f"Expand and simplify {question_expr}",
            "answer": str(expanded_expr).replace("**", "^")
        })

    # Save to JSON
    output_path = "250_fully_expanded_questions.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
