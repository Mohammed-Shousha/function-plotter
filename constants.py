import re

# list of allowed words to be entered by the user
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

PATTERN = r'^(\s*([0-9]+(?:\.[0-9]+)?|{})\s*)+$'.format(
    '|'.join(map(re.escape, ALLOWED)))


# dictionary of replacements for string to mathematical expression conversion
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

FUNCTION_ERROR_MSG = f"Invalid function.\nOnly functions of 'x' are allowed. e.g., 5*x^3 + 2/x - 1.\nAllowed symbols: {', '.join(ALLOWED)}"
RANGE_ERROR_MSG = "Invalid range. Minimum x value must be less than maximum x value."
