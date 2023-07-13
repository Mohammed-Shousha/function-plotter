import re

# list of allowed symbols to be entered by the user
ALLOWED = [
    'x',
    'sin',
    'cos',
    'sqrt',
    'exp',
    'tan',
    'log',
    'pi',
    'e',
    '/',
    '+',
    '*',
    '^',
    '-',
    '(',
    ')',
]

# regex pattern to check if the input is valid
PATTERN = r'^(\s*([0-9]+(?:\.[0-9]+)?|{})\s*)+$'.format(
    '|'.join(map(re.escape, ALLOWED)))


# dictionary of replacements from string to mathematical expression
REPLACEMENTS = {
    'sin': 'np.sin',
    'cos': 'np.cos',
    'sqrt': 'np.sqrt',
    'exp': 'np.exp',
    'tan': 'np.tan',
    'log': 'np.log',
    '^': '**',
    'pi': 'np.pi',
    'e': 'np.e',
}

# range of x values to be plotted
RANGE = (-1000, 1000)

# error messages
FUNCTION_ERROR_MSG = f"Only functions of 'x' are allowed. e.g., 5*x^3 + 2/x - 1.\nAllowed symbols: {', '.join(ALLOWED)}"
RANGE_ERROR_MSG = "Minimum x value must be less than maximum x value."
