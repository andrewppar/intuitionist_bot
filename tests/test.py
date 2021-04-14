import unittest
from intuitionistic_bot import FormulaParser, Atomic, Negation, Implication
from intuitionistic_bot import Disjunction, Conjunction, BiImplication


class TestFormulaParser(unittest.TestCase):

    A = Atomic("a")
    NOTA = Negation(A)
    NOTNOTA = Negation(NOTA)

    def internal_formula_test(self, formula_string, expected_result):
        parser = FormulaParser()
        formula = formula_string
        result = parser.parse(formula)
        self.assertEqual(result, expected_result)

    def test_parse_one(self):
        self.internal_formula_test("¬¬((¬¬¬a⇾a)∨¬a)",
                                   Negation
                                   (Negation
                                    (Disjunction
                                     (Implication(Negation(self.NOTNOTA),
                                                  self.A),
                                      self.NOTA))))

    def test_parse_two(self):
        self.internal_formula_test("¬¬((¬¬¬a⇿¬a)∨a)",
                                   Negation
                                   (Negation
                                    (Disjunction
                                     (BiImplication
                                      (Negation(self.NOTNOTA),
                                       self.NOTA),
                                      self.A))))

    def test_parse_three(self):
        self.internal_formula_test("¬¬((¬¬¬a∧¬a)∨a)",
                                   Negation
                                   (Negation
                                    (Disjunction
                                     (Conjunction
                                      (Negation(self.NOTNOTA),
                                       self.NOTA),
                                      self.A))))
