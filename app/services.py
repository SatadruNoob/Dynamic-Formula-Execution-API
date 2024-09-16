import ast
import re
from datetime import datetime
from fastapi import HTTPException
from app.models import FormulaPayload
from app.utils import parse_value


# Formula validation function
def validate_formula(formula, context):
    """
    Validates the mathematical expression in the formula.
    - Checks if all variables are defined.
    - Checks if there are any syntax errors.
    """
    # Validate that all variables used in the expression exist in the context
    for node in ast.walk(ast.parse(formula.expression)):
        if isinstance(node, ast.Name) and node.id not in context:
            raise HTTPException(status_code=400, detail=f"Variable '{node.id}' is not defined in the inputs or data.")

    # Perform a basic syntax check for division by zero
    try:
        # Compile the expression to check for syntax errors
        compiled_expr = compile(ast.parse(formula.expression, mode='eval'), '', 'eval')
    except SyntaxError:
        raise HTTPException(status_code=400, detail="Syntax error in the formula.")

def evaluate_expression(expression, context):
    # Log the context before parsing
    print(f"Context before parsing: {context}")

    # Ensure all values in the context are properly parsed
    for key, value in context.items():
        if isinstance(value, str):  # Parse strings into appropriate types
            context[key] = parse_value(value)

    # Log the context after parsing
    print(f"Context after parsing: {context}")

    # Safe evaluation of the expression
    try:
        compiled_expr = compile(ast.parse(expression, mode='eval'), '', 'eval')
        result = eval(compiled_expr, {}, context)
        return result
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Division by zero error in the formula.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error evaluating expression: {e}")

def execute_formulas(payload: FormulaPayload):
    data_rows = payload.data
    formulas = payload.formulas
    
    results = {formula.outputVar: [] for formula in formulas}
    
    # Iterate over each row of data
    for row in data_rows:
        row_context = row.dict()  # Convert Pydantic model to dictionary
        
        # Iterate over each formula
        for formula in formulas:
            try:
                # Prepare the formula's expression context
                formula_context = {input.varName: row_context.get(input.varName) for input in formula.inputs}

                # Parse the values in the context to ensure correct types
                for var, val in formula_context.items():
                    if isinstance(val, str):
                        formula_context[var] = parse_value(val)
                
                # Validate the formula before evaluating it
                validate_formula(formula, formula_context)
                
                # Safely evaluate the expression
                result = evaluate_expression(formula.expression, formula_context)

                # Store the result in the row context for formula chaining
                row_context[formula.outputVar] = result
                results[formula.outputVar].append(result)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error evaluating formula {formula.outputVar}: {e}")
    
    return {
        "results": results,
        "status": "success",
        "message": "The formulas were executed successfully."
    }
