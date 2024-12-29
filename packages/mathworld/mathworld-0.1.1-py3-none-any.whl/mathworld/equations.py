from __future__ import annotations

__author__ = 'Tobia Petrolini'
__file__ = 'equations.py'

import re
import sympy as sp


def sympy_value(value, name: str = 'value') -> sp.Expr:
    """
    Convert a value into a sympy expression.

    Args:
        value (int | float | str | sp.Expr): The value to convert.
        name (str): A name used in error messages.

    Returns:
        sp.Expr: The converted value as a sympy expression.

    Raises:
        ValueError: If the input value is of an unsupported type.
    """
    if isinstance(value, int):
        value = sp.simplify(sp.Integer(value))
    elif isinstance(value, float):
        value = sp.simplify(sp.Rational(str(value)))
    elif isinstance(value, sp.Expr):
        pass
    elif isinstance(value, str):
        value = read_expression(value)
    else:
        raise ValueError(
            f"{name} must be an integer, float, Rational, Expr or str")

    return value


def format_expression(expression: str, lower: bool = True) -> str:
    """
    Format a mathematical expression into a standard form suitable for sympy.

    Args:
        expression (str): The mathematical expression as a string.
        lower (bool): Whether to convert the result to lowercase.

    Returns:
        str: The formatted expression.
    """
    # Mapping of mathematical functions to placeholders (example uses Chinese Unicode as placeholders)
    function_mapping = {
        'cos': chr(21455),
        'sin': chr(21456),
        'tan': chr(21457),
        'acos': chr(21458),
        'asin': chr(21459),
        'atan': chr(21460),
        'cosh': chr(21461),
        'sinh': chr(21462),
        'tanh': chr(21463),
        'acosh': chr(21464),
        'asinh': chr(21465),
        'atanh': chr(21466),
        'exp': chr(21467),
        'log': chr(21468),
        'sqrt': chr(21469),
        'Abs': chr(21470)
    }

    # Replace functions with placeholders
    for func, char in function_mapping.items():
        expression = expression.replace(f'{func}(', char)

    # Standardize brackets and operators
    expression = expression.replace(
        '[', '(').replace(']', ')').replace('{', '(').replace('}', ')')
    expression = expression.replace('^', '**').replace(')(', ')*(')

    # Add explicit multiplication symbols where necessary
    expression = re.sub(r'(\d+)([a-zA-Z(])', r'\1*\2', expression)
    expression = re.sub(r'([a-zA-Z])\(', r'\1*(', expression)
    expression = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', expression)

    # Reverse the placeholders to function names if needed
    if lower:
        expression = expression.lower()
    for func, char in function_mapping.items():
        expression = expression.replace(char, f'{func}(')

    return expression


def find_variables(expression: str) -> tuple:
    """
    Identify all variables present in a mathematical expression.

    Args:
        expression (str): The mathematical expression as a string.

    Returns:
        tuple: A tuple of all variable names found in the expression.
    """
    variables = set(re.findall(r'[a-zA-Z]', expression))
    return tuple(variables)


def isexpression(expression: str) -> bool:
    """
    Check if a string is a valid mathematical expression.

    Args:
        expression (str): The expression to check.

    Returns:
        bool: True if the expression is valid, False otherwise.
    """
    try:
        sp.sympify(expression)
        return True
    except:
        return False


def is_sympy_expression(expression) -> bool:
    """
    Determine if an object is a sympy expression.

    Args:
        expression: The object to check.

    Returns:
        bool: True if the object is a sympy expression, False otherwise.
    """
    return isinstance(expression, sp.Expr)


def isequation(equation: str) -> bool:
    """
    Check if a string represents a valid mathematical equation.

    Args:
        equation (str): The equation to check.

    Returns:
        bool: True if the equation is valid, False otherwise.
    """
    try:
        lhs, rhs = equation.split("=")
        sp.sympify(lhs)
        sp.sympify(rhs)
        return True
    except:
        return False


def is_sympy_equation(equation) -> bool:
    """
    Determine if an object is a sympy equation.

    Args:
        equation: The object to check.

    Returns:
        bool: True if the object is a sympy equation, False otherwise.
    """
    return isinstance(equation, sp.Equality)


def expression(expression: str) -> sp.Expr:
    """
    Convert a string representation of an expression into a sympy expression.

    Args:
        expression (str): The expression as a string.

    Returns:
        sp.Expr: The sympy representation of the expression.
    """
    symbols = find_variables(expression)
    for symbol in symbols:
        exec(f"{symbol} = sp.symbols('{symbol}')")
    return sp.sympify(expression)


def equation(equation: str) -> sp.Equality:
    """
    Convert a string representation of an equation into a sympy equation.

    Args:
        equation (str): The equation as a string in the form "lhs=rhs".

    Returns:
        sp.Equality: The sympy representation of the equation.
    """
    lhs, rhs = equation.split("=")
    symbols = find_variables(equation)
    for symbol in symbols:
        exec(f"{symbol} = sp.symbols('{symbol}')")
    return sp.Eq(sp.sympify(lhs), sp.sympify(rhs))


def read_expression(_expression: str) -> sp.Expr:
    """
    Parse and convert a mathematical expression from a string.

    Args:
        _expression (str): The mathematical expression as a string.

    Returns:
        sp.Expr: The sympy representation of the expression.

    Raises:
        ValueError: If the string is not a valid mathematical expression.
    """
    _expression = format_expression(_expression)
    if not isexpression(_expression):
        raise ValueError("Invalid expression")
    return expression(_expression)


def read_equation(_equation: str) -> sp.Equality:
    """
    Parse and convert a mathematical equation from a string.

    Args:
        _equation (str): The mathematical equation as a string.

    Returns:
        sp.Equality: The sympy representation of the equation.

    Raises:
        ValueError: If the string is not a valid mathematical equation.
    """
    _equation = format_expression(_equation)
    if not isequation(_equation):
        raise ValueError("Invalid equation")
    return equation(_equation)


def read(input: str) -> sp.Expr:
    """
    Parse and convert a string into a sympy expression or equation.

    Args:
        input (str): The input string representing an expression or equation.

    Returns:
        sp.Expr or sp.Equality: The sympy representation of the input.
    """
    if "=" in input:
        return read_equation(input)
    else:
        return read_expression(input)
