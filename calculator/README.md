# calculator

A simple CLI calculator that supports basic arithmetic operations plus percentage calculations.

## Features

- Basic arithmetic: `+`, `-`, `*`, `/`
- Modulo: `%` (e.g., `10 % 3` = 1)
- **Percentage**: `pct` postfix operator (e.g., `20pct` = 0.2)

## Usage

```bash
python main.py "<expression>"
```

## Examples

```bash
python main.py "3 + 5"
# Output: {"expression": "3 + 5", "result": 8}

python main.py "200 * 20pct"
# Output: {"expression": "200 * 20pct", "result": 40}  # 20% of 200

python main.py "50 + 50pct"
# Output: {"expression": "50 + 50pct", "result": 50.5}  # 50 + 5%

python main.py "10 % 3"
# Output: {"expression": "10 % 3", "result": 1}  # modulo still works
```

## Operator Precedence

- `*`, `/`, `pct` (postfix) have higher precedence (level 2)
- `+`, `-`, `%` (modulo) have lower precedence (level 1)

## Notes

- The `%` operator remains as modulo (binary operator between two numbers)
- Use `pct` as a postfix operator for percentage calculations (e.g., `20pct` means 20%)
- Numbers can have decimal points
- Expressions are evaluated using standard infix notation with proper precedence