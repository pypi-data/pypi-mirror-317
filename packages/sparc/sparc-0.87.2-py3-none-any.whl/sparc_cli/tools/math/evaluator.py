from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import logging
from typing import Any, Dict, List, Optional, Literal
from langchain.tools import BaseTool
from langchain.llms.base import BaseLLM
from .models import BenchmarkRequest, BenchmarkResponse
from .validator import MathValidator
from pydantic import Field

class SparcBaseTool(BaseTool):
    """Base class for SPARC tools with proper type annotations."""
    name: str = Field(description="The name of the tool")
    description: str = Field(description="The description of the tool")

logger = logging.getLogger(__name__)

class MathBenchmarkEvaluator(ABC):
    """Base class for math benchmark evaluation."""
    
    def __init__(self, llm: BaseLLM, tools: Optional[List[BaseTool]] = None):
        """Initialize the evaluator.
        
        Args:
            llm: Language model to use for evaluation
            tools: Optional list of tools to use
        """
        self.llm = llm
        self.tools = tools or []
        self.validator = MathValidator()
        self.setup_tools()
        
    @abstractmethod
    def setup_tools(self) -> None:
        """Configure tools needed for evaluation."""
        pass
        
    @abstractmethod
    def evaluate_problem(self, request: BenchmarkRequest) -> BenchmarkResponse:
        """Evaluate a math benchmark problem.
        
        Args:
            request: The benchmark problem to evaluate
            
        Returns:
            Response containing the answer and validation results
        """
        pass
    
    def process_results(self, problem_id: str, answer: Any, 
                       validation_result: Dict[str, Any]) -> BenchmarkResponse:
        """Process evaluation results into a response.
        
        Args:
            problem_id: ID of the problem
            answer: Computed answer
            validation_result: Validation details
            
        Returns:
            Formatted benchmark response
        """
        return BenchmarkResponse(
            problem_id=problem_id,
            answer=answer,
            validation_result=validation_result,
            metadata={'evaluator': self.__class__.__name__}
        )
    
    def validate_solution(self, answer: Any, expected: Any, 
                         answer_type: str) -> Dict[str, Any]:
        """Validate a solution against expected answer.
        
        Args:
            answer: Computed answer to validate
            expected: Expected correct answer
            answer_type: Type of answer (numerical/symbolic/matrix)
            
        Returns:
            Dictionary with validation results
        """
        if answer_type == 'numerical':
            valid, message = self.validator.validate_numerical(answer, expected)
        elif answer_type == 'symbolic':
            valid, message = self.validator.validate_symbolic(answer, expected)
        elif answer_type == 'matrix':
            valid, message = self.validator.validate_matrix(answer, expected)
        else:
            valid, message = False, f"Unknown answer type: {answer_type}"
            
        return {
            'valid': valid,
            'message': message,
            'type': answer_type
        }

class NuminaMathEvaluator(MathBenchmarkEvaluator):
    """Direct calculation-based math evaluator."""
    
    def setup_tools(self) -> None:
        """Configure calculation tools."""
        # Initialize calculator and basic math tools
        self.calculator = CalculatorTool()
        self.tools.extend([self.calculator])
        
    def evaluate_problem(self, request: BenchmarkRequest) -> BenchmarkResponse:
        """Evaluate problem using direct calculation.
        
        Args:
            request: The benchmark problem to evaluate
            
        Returns:
            Response with calculated answer
        """
        try:
            # Direct calculation using calculator tool
            answer = self.calculator.run(request.problem_text)
            
            # Validate against expected answer if provided
            expected = request.metadata.get('expected_answer')
            if expected:
                validation = self.validate_solution(
                    answer, expected, request.expected_type
                )
            else:
                validation = {'valid': None, 'message': 'No expected answer provided'}
                
            return self.process_results(request.problem_id, answer, validation)
            
        except Exception as e:
            logger.error(f"Evaluation failed: {str(e)}")
            return self.process_results(
                request.problem_id,
                None,
                {'valid': False, 'message': f"Evaluation error: {str(e)}"}
            )

class MathOdysseyEvaluator(MathBenchmarkEvaluator):
    """Step-by-step reasoning math evaluator."""
    
    def setup_tools(self) -> None:
        """Configure symbolic and advanced math tools."""
        self.symbolic_solver = SymbolicSolverTool()
        self.calculator = CalculatorTool()
        self.tools.extend([self.symbolic_solver, self.calculator])
        
    def evaluate_problem(self, request: BenchmarkRequest) -> BenchmarkResponse:
        """Evaluate problem using step-by-step reasoning.
        
        Args:
            request: The benchmark problem to evaluate
            
        Returns:
            Response with reasoned answer
        """
        try:
            # First attempt symbolic solution
            symbolic_result = self.symbolic_solver.run(request.problem_text)
            
            # Fall back to numerical if needed
            if not symbolic_result:
                answer = self.calculator.run(request.problem_text)
            else:
                answer = symbolic_result
                
            # Validate result
            expected = request.metadata.get('expected_answer')
            if expected:
                validation = self.validate_solution(
                    answer, expected, request.expected_type
                )
            else:
                validation = {'valid': None, 'message': 'No expected answer provided'}
                
            return self.process_results(request.problem_id, answer, validation)
            
        except Exception as e:
            logger.error(f"Evaluation failed: {str(e)}")
            return self.process_results(
                request.problem_id,
                None,
                {'valid': False, 'message': f"Evaluation error: {str(e)}"}
            )

class CalculatorTool(SparcBaseTool):
    """Tool for basic mathematical calculations."""
    
    name: str = Field(default="calculator")
    description: str = Field(default="Performs basic mathematical calculations")
    
    def _run(self, expression: str) -> str:
        """Execute the calculation.
        
        Args:
            expression: Mathematical expression to evaluate
            
        Returns:
            Calculated result as a string
        """
        try:
            # Create a safe dictionary with basic math operations
            safe_dict = {
                'abs': abs,
                'float': float,
                'int': int,
                'pow': pow,
                'round': round,
                '+': lambda x, y: x + y,
                '-': lambda x, y: x - y,
                '*': lambda x, y: x * y,
                '/': lambda x, y: x / y,
                '**': pow
            }
            
            # Parse the expression to handle quadratic equations
            if "=" in expression and ("x^2" in expression or "x²" in expression):
                # For equations like "x^2 + 5x + 6 = 0"
                left_side = expression.split('=')[0].strip()
                # Extract coefficients
                left_side = left_side.replace("²", "^2")  # normalize notation
                terms = left_side.replace(" ", "").replace("-", "+-").split("+")
                
                a = b = c = 0
                for term in terms:
                    if not term: continue
                    if "x^2" in term:
                        a = -1 if term.startswith("-") else 1
                        if term.replace("-", "").replace("x^2", ""):
                            a *= float(term.replace("-", "").replace("x^2", ""))
                    elif "x" in term:
                        b = -1 if term.startswith("-") else 1
                        if term.replace("-", "").replace("x", ""):
                            b *= float(term.replace("-", "").replace("x", ""))
                    else:
                        c = float(term)
                
                # Use quadratic formula: (-b ± √(b² - 4ac)) / (2a)
                discriminant = b**2 - 4*a*c
                if discriminant < 0:
                    return "No real solutions"
                
                x1 = (-b + (discriminant ** 0.5)) / (2*a)
                x2 = (-b - (discriminant ** 0.5)) / (2*a)
                
                # Format the solutions nicely
                solutions = []
                for x in sorted([x1, x2]):
                    if x == int(x):
                        solutions.append(str(int(x)))
                    else:
                        solutions.append(f"{x:.2f}")
                
                return f"x = {' or x = '.join(solutions)}"
            else:
                # For regular calculations
                result = eval(expression, {"__builtins__": None}, safe_dict)
                if isinstance(result, (int, float)):
                    return str(result if result == int(result) else f"{result:.2f}")
                return str(result)
        except Exception as e:
            raise ValueError(f"Calculation failed: {str(e)}")

class SymbolicSolverTool(SparcBaseTool):
    """Tool for symbolic mathematical manipulation."""
    
    name: str = Field(default="symbolic_solver")
    description: str = Field(default="Performs symbolic mathematical operations")
    
    def _run(self, expression: str) -> str:
        """Execute symbolic manipulation.
        
        Args:
            expression: Mathematical expression to manipulate
            
        Returns:
            Simplified symbolic expression
        """
        try:
            # Placeholder for symbolic manipulation logic
            return expression
        except Exception as e:
            raise ValueError(f"Symbolic solving failed: {str(e)}")
