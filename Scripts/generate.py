import random
import json
from sympy import symbols, expand, Mul, Add
from sympy.abc import x
import mathgenerator
from collections import defaultdict
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

    # Format the expanded expression without * and with ^ instead of **
    def clean_expression(expr):
        expr_str = str(expr).replace("**", "^")
        expr_str = expr_str.replace("*", "")
        return expr_str

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
        expanded_expr = expand(full_expr)

        questions.append({
            "question": f"Expand and simplify {question_expr}",
            "answer": clean_expression(expanded_expr)
        })

    # Save to JSON
    output_path = "250_clean_expanded_questions.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

# Split into categories
genlist = mathgenerator.getGenList()
listofallsubjects = defaultdict(list)
for topic in genlist:
    
    subject = topic[4]
    if subject not in listofallsubjects:
        listofallsubjects[subject] = []
    else:
        listofallsubjects[subject].append(topic[0])



def generate_math_problems(num_problems,  output_file, randlist):
    data = []
    output_file = output_file + '.json'
    for _ in range(num_problems):
        try:
            problem_id = random.choice(randlist)
            problem, solution = mathgenerator.genById(problem_id)
            data.append({
                "problem": problem,
                "solution": solution
            })
        except Exception as e:
            # Handle any invalid IDs or generation errors 
            print(f"Error with ID {problem_id}: {e}")
            continue

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Saved {len(data)} problems to {output_file}")

# Make multiple files for every category
for key in listofallsubjects.keys():
    
    generate_math_problems(500,key,listofallsubjects[key]) # Use [0,1,2,...125] list if you want all categories
