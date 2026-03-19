from abc import ABC, abstractmethod
from typing import Any
from ..schemas.execution_plan import ExecutionPlan

class BaseAdapter(ABC):
    """Abstract base class for all Axiom execution adapters."""
    
    def __init__(self):
        self._plan: ExecutionPlan = None
        
    def ingest(self, plan: ExecutionPlan) -> None:
        """Stores the completely isolated static ExecutionPlan for lateral compilation."""
        if not isinstance(plan, ExecutionPlan):
            raise TypeError("Expected an ExecutionPlan object.")
        self._plan = plan
        
    @abstractmethod
    def execute(self) -> Any:
        """Translates the plan into the framework's native execution format and runs it."""
        pass
