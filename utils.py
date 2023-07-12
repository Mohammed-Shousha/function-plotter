import re
import numpy as np
from constants import REPLACEMENTS, PATTERN


def validate_input(user_input):
    return re.match(PATTERN, user_input)


def create_expression_function(user_input):

    for word, replacement in REPLACEMENTS.items():
        user_input = user_input.replace(word, replacement)

    # dealing with constant expressions
    if 'x' not in user_input:
        user_input += '+0*x'

    def expr(x):
        return eval(user_input)

    return expr
