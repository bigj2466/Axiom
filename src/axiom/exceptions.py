class AxiomError(Exception):
    """Base exception for all Axiom related errors."""
    pass

class AxiomSchemaError(AxiomError):
    """Raised when an Axiom definition fails schema validation."""
    pass

class AxiomDependencyError(AxiomError):
    """Raised when an Axiom entity cannot resolve its dependencies."""
    pass

class AxiomNotFoundError(AxiomError):
    """Raised when an Axiom entity id is not found in the registry."""
    pass
