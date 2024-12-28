# Math Evaluation in SPARC

SPARC includes a powerful math evaluation system that can handle various mathematical operations, with a particular focus on solving quadratic equations.

## Features

### Quadratic Equation Solver
- Solves equations in the form ax² + bx + c = 0
- Handles coefficients with or without explicit values (e.g., x² is treated as 1x²)
- Supports both positive and negative terms
- Provides solutions with appropriate precision (integers when possible, decimals when needed)

### Input Format
The solver accepts equations in several formats:
- Standard form: x² + 5x + 6 = 0
- With coefficients: 2x² - 3x + 1 = 0
- Using different notations: x^2 or x² are both accepted

### Output Format
Solutions are presented in a clear format:
- For integer solutions: "x = -2 or x = -3"
- For decimal solutions: "x = -1.50 or x = -2.50"
- For no real solutions: "No real solutions"

## Usage Examples

1. Basic quadratic equation:
```
> solve the quadratic equation x² + 5x + 6 = 0
Solutions: x = -2 or x = -3
```

2. With coefficients:
```
> solve 2x² - 3x + 1 = 0
Solutions: x = 1 or x = 0.50
```

3. Using alternate notation:
```
> solve x^2 - 4 = 0
Solutions: x = 2 or x = -2
```

## Implementation Details

The math evaluation system uses a robust parsing algorithm that:
1. Normalizes the equation format
2. Identifies coefficients for each term
3. Applies the quadratic formula: x = (-b ± √(b² - 4ac)) / (2a)
4. Formats results based on solution type (integer vs decimal)

### Error Handling
The system includes comprehensive error handling for:
- Invalid equation formats
- Non-quadratic equations
- Complex solutions
- Parsing errors

## Future Enhancements
Planned features include:
- Support for higher-degree polynomials
- Symbolic mathematics
- Step-by-step solution explanations
- Graph visualization

## Integration
The math evaluation system is fully integrated with SPARC's chat mode, allowing for:
- Interactive problem solving
- Follow-up questions
- Solution verification
- Multiple equation solving in sequence
