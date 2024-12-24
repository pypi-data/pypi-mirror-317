from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Type, TypeVar, Generic
from enum import Enum
from typing import get_origin

def type_to_string(t: type) -> str:
    """Convert a type to its string representation."""
    origin = get_origin(t)
    if origin is None:
        return t.__name__
    args = t.__args__
    args_str = ', '.join(arg.__name__ for arg in args)
    return f"{origin.__name__}[{args_str}]"

class AllowedTypes(Enum):
    """Enumeration of allowed data types in the workflow system."""
    STRING = str
    INTEGER = int
    FLOAT = float
    BOOLEAN = bool
    DICT = dict
    LIST = list
    ANY = Any

    @classmethod
    def get_types(cls) -> tuple:
        return (str, int, float, bool, dict, list, Dict, List, Any)
    
    @classmethod
    def get_type_map(cls) -> Dict[str, Type]:
        """Get mapping of type names to type objects, including generic types."""
        base_types = {member.value.__name__: member.value for member in cls}
        # Add Dict, List and Any types
        base_types.update({
            'dict': dict,
            'Dict': Dict,
            'list': list,
            'List': List,
            'Any': Any
        })
        return base_types

class WorkflowValidationError(Exception):
    """Base exception for workflow validation errors."""
    pass

T = TypeVar('T')
class ValidatedDict(Dict[str, T], ABC, Generic[T]):
    """Abstract base class for validated dictionaries."""
    
    def __init__(self, data: Dict[str, T]):
        if type(self) is ValidatedDict:
            raise TypeError("Can't instantiate abstract class ValidatedDict")
        self._validate(data)
        super().__init__(data)
    
    @abstractmethod
    def _validate(self, data: Dict[str, T]) -> None:
        """Validate dictionary data."""
        pass

    def to_dict(self) -> Dict[str, T]:
        """Convert to regular dictionary."""
        return dict(self)

class Schema(ValidatedDict[type]):
    """Schema validator with improved type checking."""
    
    ALLOWED_TYPES = AllowedTypes.get_types()
    
    def _validate(self, schema: Dict[str, type]) -> None:
        if not isinstance(schema, dict):
            raise TypeError("Schema must be a dictionary")
            
        for key, value in schema.items():
            if not isinstance(key, str):
                raise TypeError("Schema keys must be strings")
            # Check if it's a type or a generic type (like Dict, List etc)
            if not (isinstance(value, type) or hasattr(value, '__origin__')):
                raise TypeError(f"Schema value for '{key}' must be a type or generic type")
            
            # If it's a generic type, validate its origin
            if hasattr(value, '__origin__'):
                origin = value.__origin__
                # Convert typing.List/Dict to built-in list/dict for comparison
                if origin == List:
                    origin = list
                elif origin == Dict:
                    origin = dict
                
                if origin not in self.ALLOWED_TYPES:
                    raise ValueError(
                        f"Invalid type '{value.__origin__.__name__}' for key '{key}'. "
                        f"Allowed types are: {[t.__name__ for t in self.ALLOWED_TYPES]}"
                    )
            # If it's a regular type, validate it's in allowed types
            elif isinstance(value, type) and value not in self.ALLOWED_TYPES:
                raise ValueError(
                    f"Invalid type '{value.__name__}' for key '{key}'. "
                    f"Allowed types are: {[t.__name__ for t in self.ALLOWED_TYPES]}"
                )

    def to_dict(self) -> Dict[str, str]:
        """Convert schema to dictionary with type names"""
        return {key: value.__name__ for key, value in self.items()}
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Schema':
        """Create Schema from dictionary of type names"""
        return cls({
            key: AllowedTypes.get_type_map()[type_name]
            for key, type_name in data.items()
        })

class Mappings(ValidatedDict[str]):
    """Mapping validator with reference checking."""
    
    def __init__(self, mappings: Dict[str, str], source_schema: Optional[Schema] = None, 
                 target_schema: Optional[Schema] = None):
        self.source_schema = source_schema
        self.target_schema = target_schema
        super().__init__(mappings)

    def _validate(self, mappings: Dict[str, str]) -> None:
        if not isinstance(mappings, dict):
            raise TypeError("Mappings must be a dictionary")
        
        for key, value in mappings.items():
            if not isinstance(key, str):
                raise TypeError("Mapping keys must be strings")
            if not isinstance(value, str):
                raise TypeError("Mapping values must be strings")
            
            # Validate schema references if schemas are provided
            if self.source_schema and key not in self.source_schema:
                raise KeyError(f"Mapping source '{key}' not found in schema")
            if self.target_schema and value not in self.target_schema:
                raise KeyError(f"Mapping target '{value}' not found in schema")

    def to_dict(self) -> Dict[str, str]:
        """Convert mappings to dictionary"""
        return dict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Mappings':
        """Create Mappings from dictionary"""
        return cls(data)

class Arguments(ValidatedDict[Any]):
    """Argument validator with improved type checking."""
    
    ALLOWED_TYPES = AllowedTypes.get_types()

    def _validate(self, args: Dict[str, Any]) -> None:
        if not isinstance(args, dict):
            raise TypeError("Arguments must be a dictionary")
        
        for key, value in args.items():
            if not isinstance(key, str):
                raise TypeError("Argument keys must be strings")
            if value is None:
                raise ValueError(f"Argument '{key}' cannot be None")
            
            # Check if value's type matches any of the allowed types
            value_type = type(value)
            # Skip type checking if Any is allowed
            if Any in self.ALLOWED_TYPES:
                continue
            
            if value_type not in self.ALLOWED_TYPES and not any(
                isinstance(value, t) for t in self.ALLOWED_TYPES 
                if not hasattr(t, '__origin__')  # Skip generic types
            ):
                raise TypeError(
                    f"Invalid type for argument '{key}': {type(value).__name__}. "
                    f"Allowed types are: {[t.__name__ for t in self.ALLOWED_TYPES]}"
                )

    def to_dict(self) -> Dict[str, Any]:
        """Convert arguments to dictionary"""
        return dict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Arguments':
        """Create Arguments from dictionary"""
        return cls(data)

@dataclass
class TaskExecutionInfo:
    """Contains execution information for a task."""
    status: str
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    error: Optional[Exception] = None
    dependencies_met: bool = False

@dataclass
class MetaFunc:
    """Metadata container for function information with improved validation."""
    module: str
    name: str
    args: Schema = field(default_factory=lambda: Schema({}))
    rets: Schema = field(default_factory=lambda: Schema({}))
    has_kwargs: bool = False  # New field to indicate kwargs support

    def __post_init__(self):
        if not isinstance(self.module, str) or not self.module:
            raise WorkflowValidationError("Module must be a non-empty string")
        if not isinstance(self.name, str) or not self.name:
            raise WorkflowValidationError("Function name must be a non-empty string")

    def to_dict(self) -> Dict[str, Any]:
        """Serialize MetaFunc to dictionary"""
        # Filter out **kwargs from args when serializing
        args_dict = {k: v for k, v in self.args.items() if k != '**kwargs'}
        return {
            'module': self.module,
            'name': self.name,
            'args': Schema(args_dict).to_dict(),
            'rets': self.rets.to_dict(),
            'has_kwargs': self.has_kwargs
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MetaFunc':
        """Create MetaFunc from dictionary"""
        return cls(
            module=data['module'],
            name=data['name'],
            args=Schema.from_dict(data['args']),
            rets=Schema.from_dict(data['rets']),
            has_kwargs=data.get('has_kwargs', False)  # Default to False for backward compatibility
        )

@dataclass
class MetaTask:
    """Metadata container for task information.
    
    Attributes:
        name: Unique identifier for the task
        description: Human-readable description of what the task does
        func: Reference to the function this task wraps
        fixed_args: Arguments for the task
        inputs: Schema defining required input types
        outputs: Schema defining output types
        input_mappings: Mappings between task inputs and function arguments
        output_mappings: Mappings between function returns and task outputs
    """
    name: str
    description: str
    func: MetaFunc
    fixed_args: Arguments = field(default_factory=lambda: Arguments({}))
    inputs: Schema = field(default_factory=lambda: Schema({}))
    outputs: Schema = field(default_factory=lambda: Schema({}))
    input_mappings: Mappings = field(default_factory=lambda: Mappings({}))
    output_mappings: Mappings = field(default_factory=lambda: Mappings({}))

    def to_dict(self) -> Dict[str, Any]:
        """Serialize MetaTask to dictionary"""
        return {
            'name': self.name,
            'description': self.description,
            'func': self.func.to_dict(),
            'fixed_args': dict(self.fixed_args),
            'inputs': self.inputs.to_dict(),
            'outputs': self.outputs.to_dict(),
            'input_mappings': self.input_mappings.to_dict(),
            'output_mappings': self.output_mappings.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MetaTask':
        """Create MetaTask from dictionary"""
        return cls(
            name=data['name'],
            description=data['description'],
            func=MetaFunc.from_dict(data['func']),
            fixed_args=Arguments(data['fixed_args']),
            inputs=Schema.from_dict(data['inputs']),
            outputs=Schema.from_dict(data['outputs']),
            input_mappings=Mappings.from_dict(data['input_mappings']),
            output_mappings=Mappings.from_dict(data['output_mappings'])
        )

@dataclass
class MetaWorkflow:
    """Metadata container for workflow information.

    Attributes:
        name: Unique identifier for the workflow
        description: Human-readable description of what the workflow does
        tasks: List of MetaTask objects that comprise the workflow
        inputs: Schema defining the required input types for the entire workflow
        outputs: Schema defining the output types produced by the workflow
    """
    name: str
    description: str
    tasks: List[MetaTask]
    inputs: Schema = field(default=lambda: Schema({}))
    outputs: Schema = field(default=lambda: Schema({}))

    def to_dict(self) -> Dict[str, Any]:
        """Serialize MetaWorkflow to dictionary"""
        return {
            'name': self.name,
            'description': self.description,
            'tasks': [task.to_dict() for task in self.tasks],
            'inputs': self.inputs.to_dict(),
            'outputs': self.outputs.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MetaWorkflow':
        """Create MetaWorkflow from dictionary"""
        return cls(
            name=data['name'],
            description=data['description'],
            tasks=[MetaTask.from_dict(task_data) for task_data in data['tasks']],
            inputs=Schema.from_dict(data['inputs']),
            outputs=Schema.from_dict(data['outputs'])
        )