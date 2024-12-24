from typing import Dict, Any, Callable, Union
from .context import Context
from .func import Func
from ..types.meta import MetaTask, Schema, Mappings, Arguments

class Task:
    """A task that executes a function with context-based input/output handling."""
    
    def __init__(
        self,
        name: str,
        description: str,
        func: Union[Callable[..., Any], Func],
        fixed_args: Union[Dict[str, Any], Arguments],
        inputs: Union[Dict[str, type], Schema],
        outputs: Union[Dict[str, type], Schema],
        input_mappings: Union[Dict[str, str], Mappings],
        output_mappings: Union[Dict[str, str], Mappings]
    ):
        """Initialize a task with its core components.
        
        Args:
            name: The unique identifier for the task
            description: A human-readable description of what the task does
            func: The function to execute (can be sync or async)
            fixed_args: Optional fixed arguments to pass to the function
            inputs: Schema of required context inputs {context_key: type}
            outputs: Schema of provided context outputs {context_key: type}
            input_mappings: Mapping of context keys to function arguments
            output_mappings: Mapping of function results to context keys
        """
        if not name:
            raise ValueError("Task name cannot be empty")
        if not description:
            raise ValueError("Task description cannot be empty")
        if not callable(func):
            raise TypeError("Function must be callable")
        
        self.name = name
        self.description = description
        self.func = func if isinstance(func, Func) else Func(func)
        self.fixed_args = fixed_args if isinstance(fixed_args, Arguments) else Arguments(fixed_args)
        self.inputs = inputs if isinstance(inputs, Schema) else Schema(inputs)
        self.outputs = outputs if isinstance(outputs, Schema) else Schema(outputs)
        self.input_mappings = input_mappings if isinstance(input_mappings, Mappings) else Mappings(input_mappings)
        self.output_mappings = output_mappings if isinstance(output_mappings, Mappings) else Mappings(output_mappings)
        
        # Add validation for mapping types
        for k, v in input_mappings.items():
            if not isinstance(k, str) or not isinstance(v, str):
                raise TypeError("Mapping keys and values must be strings")
        for k, v in output_mappings.items():
            if not isinstance(k, str) or not isinstance(v, str):
                raise TypeError("Mapping keys and values must be strings")
            
        # Check for circular dependencies
        common_keys = set(inputs.keys()) & set(outputs.keys())
        if common_keys:
            raise ValueError(f"Circular dependency detected for key '{common_keys.pop()}'")
        
        # Check for duplicate output mappings
        result_keys = list(output_mappings.values())
        if len(result_keys) != len(set(result_keys)):
            for key in result_keys:
                if result_keys.count(key) > 1:
                    raise ValueError(f"Multiple output mappings to the same result key '{key}'")
        
        self._validate_mappings()
    
    def _validate_mappings(self) -> None:
        """Validate that input and output mappings match the schemas."""
        # Validate input mappings
        for mapping_key in self.input_mappings:
            if mapping_key not in self.inputs:
                raise ValueError(f"Input mapping '{mapping_key}' not in inputs schema")

        # Validate output mappings
        for context_key in self.outputs.keys():
            if context_key not in self.output_mappings:
                raise ValueError(f"Provided output '{context_key}' has no mapping")
        
        for mapping_key in self.output_mappings:
            if mapping_key not in self.outputs:
                raise ValueError(f"Output mapping '{mapping_key}' not in outputs schema")

    def _prepare_inputs(self, context: Context) -> Dict[str, Any]:
        """Prepare function inputs from context and arguments.
        
        Args:
            context: The context containing input data
            
        Returns:
            Dictionary of function arguments
        """
        inputs = {}
        
        # Validate all required inputs exist and match types
        for context_key, expected_type in self.inputs.items():
            if context_key not in context:
                raise ValueError(f"Required input '{context_key}' not found in context")
            value = context[context_key]
            if not isinstance(value, expected_type):
                raise TypeError(f"Input '{context_key}' expected type {expected_type}, got {type(value)}")
            
            func_arg = self.input_mappings.get(context_key, context_key)
            inputs[func_arg] = value
        
        inputs.update(self.fixed_args)
        return inputs

    def _store_outputs(self, context: Context, result: Any) -> None:
        """Store function results in the context using standardized naming.
        
        Convention:
        - All returns are stored as "ret_0", "ret_1", etc.
        - Single return value (including dict) is stored as "ret"
        
        Args:
            context: The context to store results in
            result: The function execution results
        """
        if result is None:
            if self.outputs:
                raise ValueError("Function returned None but outputs were promised")
            return

        # Handle tuple returns
        if isinstance(result, tuple):
            result_dict = {f"ret_{i}": value for i, value in enumerate(result)}
        else:
            # Handle single return value (including dicts)
            result_dict = {"ret": result}

        # Map the standardized names to context using output_mappings
        for context_key, expected_type in self.outputs.items():
            result_key = self.output_mappings.get(context_key)
            if result_key not in result_dict:
                raise ValueError(f"Output mapping '{result_key}' not found in function result")

            value = result_dict[result_key]
            if isinstance(value, dict) and not value:  # Check if dict is empty
                raise ValueError(f"Output mapping '{result_key}' is empty")
            
            if not isinstance(value, expected_type):
                raise TypeError(f"Output '{context_key}' expected type {expected_type}, got {type(value)}")
            
            context[context_key] = value

    async def execute(self, context: Context) -> None:
        """Execute the task using the provided context.
        
        Args:
            context: The context containing input data and storing output data
        """
        # Prepare inputs from context
        inputs = self._prepare_inputs(context)
        
        # Execute function
        result = await self.func(**inputs)
        
        # Store results in context
        self._store_outputs(context, result)

    def to_meta(self) -> MetaTask:
        """Convert task to metadata representation.
        
        Returns:
            MetaTask object representing this task
        """
        return MetaTask(
            name=self.name,
            description=self.description,
            func=self.func.to_meta(),
            fixed_args=self.fixed_args,
            inputs=self.inputs,
            outputs=self.outputs,
            input_mappings=self.input_mappings,
            output_mappings=self.output_mappings
        )

    @classmethod
    def from_meta(cls, meta: MetaTask) -> 'Task':
        """Create a task from metadata.
        
        Args:
            meta: The task metadata
            
        Returns:
            New Task instance
        """
        return cls(
            name=meta.name,
            description=meta.description,
            func=Func.from_meta(meta.func),
            fixed_args=meta.fixed_args,
            inputs=meta.inputs,
            outputs=meta.outputs,
            input_mappings=meta.input_mappings,
            output_mappings=meta.output_mappings
        )
