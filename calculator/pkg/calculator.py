# calculator/pkg/calculator.py

from collections.abc import Callable


class Calculator:
    def __init__(self) -> None:
        self.operators: dict[str, Callable[[float, float], float]] = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
            "%": lambda a, b: a % b,
        }
        self.precedence: dict[str, int] = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "%": 2,
        }
        # Postfix (unary) operators take only one operand from the stack.
        # "pct" means "divide by 100" (e.g. 20pct -> 0.2)
        self.postfix_operators: dict[str, Callable[[float], float]] = {
            "pct": lambda a: a / 100,
        }

    def evaluate(self, expression: str) -> float | None:
        if not expression or expression.isspace():
            return None
        tokens = self._tokenize(expression)
        return self._evaluate_infix(tokens)

    def _tokenize(self, expression: str) -> list[str]:
        """
        Splits an infix expression into tokens, recognizing:
        - Binary operators: +, -, *, /, %
        - Postfix percentage: 20pct (converts to [20, pct])
        - Numbers (int/float)
        """
        tokens: list[str] = []
        i = 0
        n = len(expression)

        while i < n:
            # Skip whitespace
            if expression[i].isspace():
                i += 1
                continue

            c = expression[i]

            # Binary operators
            if c in "+-*/%":
                tokens.append(c)
                i += 1
                continue

            # Handle 'pct' as a postfix percentage (e.g., "20pct" -> 0.2)
            if i + 3 <= n and expression[i:i+3] == "pct":
                if tokens and self._is_number(tokens[-1]):
                    # Convert the previous number token to a separate pct token
                    tokens.append("pct")
                else:
                    raise ValueError(
                        "unexpected 'pct' operator, expected a number before it"
                    )
                i += 3
                continue

            # Read a number (including decimal points and leading signs)
            if c.isdigit() or c in "+-.":
                j = i
                # Handle sign only if it starts a number (not subtraction)
                if c in "+-" and (i == 0 or expression[i-1] in " \t\n\r"):
                    pass  # Include sign in number
                elif c in "+-":
                    # This is subtraction, push the sign as its own token
                    tokens.append(c)
                    i += 1
                    continue

                # Parse the rest of the number
                while j < n and (expression[j].isdigit() or expression[j] == "."):
                    j += 1
                tokens.append(expression[i:j])
                i = j
                continue

            # Any other character is an invalid token
            raise ValueError(f"invalid character: '{c}'")

        return tokens

    @staticmethod
    def _is_number(token: str) -> bool:
        try:
            float(token)
            return True
        except ValueError:
            return False

    def _evaluate_infix(self, tokens: list[str]) -> float:
        values: list[float] = []
        operators: list[str] = []

        for token in tokens:
            if token in self.postfix_operators:
                if not values:
                    raise ValueError(
                        f"not enough operands for operator {token}"
                    )
                a = values.pop()
                values.append(self.postfix_operators[token](a))
            elif token in self.operators:
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            else:
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"invalid token: {token}")

        while operators:
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("invalid expression")

        return values[0]

    def _apply_operator(self, operators: list[str], values: list[float]) -> None:
        if not operators:
            return

        operator = operators.pop()
        if len(values) < 2:
            raise ValueError(f"not enough operands for operator {operator}")

        b = values.pop()
        a = values.pop()
        values.append(self.operators[operator](a, b))
