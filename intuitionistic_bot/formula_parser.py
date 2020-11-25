from enum import Enum

# Utilities


debug_mode = False


def debug(func):
    def function_wrapper(*args):
        if debug_mode:
            print(f"{func.__name__} {args}")
        func(*args)
    return function_wrapper


# Formula


class Connective(Enum):

    Negation = "Not"
    Implication = "Implies"
    Conjunction = "And"
    Disjunction = "Or"
    BiImplication = "Equiv"


class Formula:

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        pass

    def __eq__(self, formula) -> bool:
        pass


class Atomic(Formula):

    def __init__(self, repr: str) -> None:
        super().__init__()
        self.repr = repr

    def __str__(self) -> str:
        return f'(AtomicFormula "{self.repr}")'

    def __eq__(self, formula) -> bool:
        if not isinstance(formula, Atomic):
            return False
        else:
            return self.repr == formula.repr


class Negation(Formula):

    def __init__(self, negatum: Formula) -> None:
        super().__init__()
        self.connective = Connective.Negation
        self.negatum = negatum

    def __str__(self) -> str:
        return f"({self.connective.value} {self.negatum.__str__()})"

    def __eq__(self, formula) -> bool:
        if not isinstance(formula, Negation):
            return False
        else:
            return self.negatum == formula.negatum


class BinaryFormula(Formula):

    def __init__(self, left: Formula, right: Formula) -> None:
        super().__init__()
        self.left = left
        self.right = right

    def _str_helper(self, connective: str) -> str:
        left_string = self.left.__str__()
        right_string = self.right.__str__()
        return f"({connective} [{left_string}, {right_string}])"

    def __str__(self) -> str:
        pass

    def _eq_helper(self, formula):
        first_formulas = [self.left, self.right]
        second_formulas = [formula.left, formula.right]
        for formula in first_formulas:
            if formula not in second_formulas:
                return False
        for formula in second_formulas:
            if formula not in first_formulas:
                return False
        return True

    def __eq__(self, formula) -> bool:
        pass


class Implication(BinaryFormula):

    def __init__(self, antecedent: Formula, consequent: Formula) -> None:
        super().__init__(antecedent, consequent)
        self.connective = Connective.Implication

    def __str__(self) -> str:
        return f"(Implies {self.left} {self.right})"

    def __eq__(self, formula) -> bool:
        if not isinstance(formula, Implication):
            return False
        else:
            first_antecedent = self.left
            second_antecedent = formula.left
            first_consequent = self.right
            second_consequent = formula.right
            ant_equal = first_antecedent == second_antecedent
            con_equal = first_consequent == second_consequent
            return ant_equal and con_equal


class BiImplication(BinaryFormula):

    def __init__(self, left: Formula, right: Formula) -> None:
        super().__init__(left, right)
        self.connective = Connective.BiImplication

    def __str__(self) -> str:
        return f"(Equiv {self.left} {self.right})"

    def __eq__(self, formula) -> bool:
        if not isinstance(formula, BiImplication):
            return False
        else:
            return self._eq_helper(formula)


class Disjunction(BinaryFormula):

    def __init__(self, left: Formula, right: Formula) -> None:
        super().__init__(left, right)
        self.connective = Connective.Disjunction

    def __str__(self) -> str:
        return self._str_helper(self.connective.value)

    def __eq__(self, formula) -> bool:
        if not isinstance(formula, Disjunction):
            return False
        else:
            return self._eq_helper(formula)


class Conjunction(BinaryFormula):

    def __init__(self, left: Formula, right: Formula) -> None:
        super().__init__(left, right)
        self.connective = Connective.Conjunction

    def __str__(self) -> str:
        return self._str_helper(self.connective.value)

    def __eq__(self, formula) -> bool:
        if not isinstance(formula, Conjunction):
            return False
        else:
            return self._eq_helper(formula)


class FormulaParser:

    def __init__(self) -> None:
        self.binary_connective_chars = ['∨', '⇾', '∧', '⇿']
        self.logical_operator_chars = self.binary_connective_chars + ['¬']
        self.special_parse_chars = self.logical_operator_chars + ['(',
                                                                  ')']

    def _is_atomic_formula(self, formula_string):
        result = True
        for char in formula_string:
            if char in self.special_parse_chars:
                return False
        return result

    def parse(self, string):
        # print(f"Parse: {string}")
        if string[0] == '(' and string[-1] == ')':
            string = string[1:-1]
        # print(f"Parse: {string}")
        if self._is_atomic_formula(string):
            return Atomic(string)
        else:
            main_idx = self.get_main_connective_index(string)
        if main_idx == 0:
            subformula = self.parse(string[1:])
            return Negation(subformula)
        else:
            connective = string[main_idx]
            left_string = string[:main_idx]
            right_string = string[(main_idx + 1):]
            left_formula = self.parse(left_string)
            right_formula = self.parse(right_string)
            if connective == '∨':
                return Disjunction(left_formula, right_formula)
            elif connective == '⇾':
                return Implication(left_formula, right_formula)
            elif connective == '∧':
                return Conjunction(left_formula, right_formula)
            elif connective == '⇿':
                return BiImplication(left_formula, right_formula)
            else:
                error = f"{connective} is not a supported connective"
                raise RuntimeError(error)

    def get_main_connective_index(self, formula_string) -> int:
        # print(f"get_main_connective_index: {formula_string}")
        paren_depth = 0
        connective_index = 0
        for idx, char in enumerate(formula_string):
            if char in self.binary_connective_chars and paren_depth == 0:
                if connective_index != 0:
                    raise RuntimeError(f"{formula_string} is ambiguous")
                else:
                    connective_index = idx
            elif char == '(':
                paren_depth += 1
            elif char == ')':
                paren_depth -= 1
            else:
                continue
        # print(f"get_main_connective_index_result: {connective_index}")
        return connective_index


# formulas = ["¬¬((¬¬¬a⇾a)∨¬a)",
#             "¬¬((¬¬¬a⇿¬a)∨a)",
#             "¬¬((¬¬¬a∧¬a)∨a)",
#             "(¬¬¬a∧¬a)∨a",
#             "¬¬¬a∧¬a",
#             ]
#
# parser = FormulaParser()
# for formula in formulas:
#     print(formula)
#     print(parser.parse(formula))
