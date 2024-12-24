from typing import Callable, Any, List, Union, Dict
from types import ModuleType
from inspect import iscoroutinefunction, isfunction, getmembers, isgeneratorfunction, isasyncgenfunction, signature, Parameter
from at_common_workflow.types.meta import MetaFunc, Schema
from at_common_workflow.core.context import Context
import asyncio, functools, importlib

class Func:
    def __init__(self, func: Callable[..., Any]) -> None:
        if isgeneratorfunction(func) or isasyncgenfunction(func):
            raise TypeError("Generator functions are not supported")
        self.func = func

    def _check_recursive_dict(self, obj: Any, seen=None) -> None:
        """Check if a dictionary contains recursive references."""
        if seen is None:
            seen = set()

        obj_id = id(obj)
        if obj_id in seen:
            raise RecursionError("Recursive dictionary structure detected")

        if isinstance(obj, dict):
            seen.add(obj_id)
            for value in obj.values():
                self._check_recursive_dict(value, seen)
            seen.remove(obj_id)
        elif isinstance(obj, (list, tuple, set)):
            seen.add(obj_id)
            for item in obj:
                self._check_recursive_dict(item, seen)
            seen.remove(obj_id)

    async def __call__(self, **kwargs: Any) -> Any:
        """Execute the function with keyword arguments only."""
        if iscoroutinefunction(self.func):
            result = await self.func(**kwargs)
        else:
            result = await asyncio.get_event_loop().run_in_executor(
                None, 
                functools.partial(self.func, **kwargs)
            )
        
        # Check for recursive structures in the result
        self._check_recursive_dict(result)
        return result

    def to_meta(self) -> MetaFunc:
        annotations = self.func.__annotations__
        return_type = annotations.get('return', Any)
        
        # Handle None or no return case
        if return_type is None or return_type == type(None):
            rets = {}
        else:
            rets = ({f'ret_{i}': t for i, t in enumerate(return_type.__args__)} 
                    if hasattr(return_type, '__origin__') and return_type.__origin__ is tuple
                    else {'ret': return_type})

        # Get kwargs parameter if it exists
        params = signature(self.func).parameters
        has_kwargs = any(p.kind == Parameter.VAR_KEYWORD for p in params.values())
        
        # Create args schema (excluding kwargs and return)
        args_schema = {k: v for k, v in annotations.items() 
                      if k != 'return' and k != 'kwargs'}

        return MetaFunc(
            module=self.func.__module__,
            name=getattr(self.func, '__qualname__', self.func.__name__),
            args=Schema(args_schema),
            rets=Schema(rets),
            has_kwargs=has_kwargs
        )

    @classmethod
    def from_meta(cls, meta: MetaFunc) -> 'Func':
        """Create a function from metadata that only accepts kwargs."""
        module = importlib.import_module(meta.module)
        obj = module

        for part in meta.name.split('.'):
            obj = getattr(obj, part)
        
        # Validate function signature matches meta and only accepts kwargs
        cls._validate_function(obj, meta)
        
        return cls(obj)

    @classmethod
    def _validate_function(cls, func: Callable, meta: MetaFunc) -> None:
        """Validate that a function matches the meta specification and only accepts kwargs."""
        sig = signature(func)
        params = sig.parameters

        # Check that all parameters (except 'self') are keyword-only
        for name, param in params.items():
            if name == 'self':  # Skip self parameter check
                continue
            if param.kind not in (Parameter.KEYWORD_ONLY, Parameter.VAR_KEYWORD):
                raise ValueError(f"Function {meta.name} must only accept keyword arguments. "
                               f"Parameter '{name}' allows positional arguments.")

        actual_annotations = func.__annotations__
        has_kwargs = any(p.kind == Parameter.VAR_KEYWORD for p in params.values())
        
        # Check if kwargs support matches
        if meta.has_kwargs and not has_kwargs:
            raise ValueError(f"Function {meta.name} does not accept arbitrary kwargs")
        
        # Check arguments (excluding **kwargs)
        for arg_name, arg_type in meta.args.items():
            if arg_name == '**kwargs':
                continue
            if arg_name not in actual_annotations:
                raise ValueError(f"Argument '{arg_name}' not found in function {meta.name}")
            if actual_annotations[arg_name] != arg_type:
                raise ValueError(f"Argument '{arg_name}' type mismatch in {meta.name}. "
                               f"Expected {arg_type}, got {actual_annotations[arg_name]}")

        # Check return type
        actual_return = actual_annotations.get('return', Any)
        if not meta.rets:
            if actual_return not in (None, type(None), Any):
                raise ValueError(f"Return type mismatch in {meta.name}. "
                               f"Expected None or no return, got {actual_return}")
        elif len(meta.rets) == 1:
            if meta.rets['ret'] != actual_return:
                raise ValueError(f"Return type mismatch in {meta.name}. "
                               f"Expected {meta.rets['ret']}, got {actual_return}")
        else:
            if not (hasattr(actual_return, '__origin__') and actual_return.__origin__ is tuple):
                raise ValueError(f"Expected tuple return type in {meta.name}, got {actual_return}")
            if len(actual_return.__args__) != len(meta.rets):
                raise ValueError(f"Return tuple length mismatch in {meta.name}. "
                               f"Expected {len(meta.rets)}, got {len(actual_return.__args__)}")
            for i, (expected_type, actual_type) in enumerate(zip(meta.rets.values(), actual_return.__args__)):
                if expected_type != actual_type:
                    raise ValueError(f"Return type mismatch at index {i} in {meta.name}. "
                                   f"Expected {expected_type}, got {actual_type}")

    @staticmethod
    def scan(modules: Union[List[ModuleType], ModuleType]) -> List['Func']:
        funcs = []
        modules = [modules] if isinstance(modules, ModuleType) else modules
        
        def scan_object(obj, module, prefix: str = '') -> None:
            for name, member in getmembers(obj):
                if name.startswith('_'):
                    continue
                
                if (isfunction(member) and 
                    getattr(member, '__module__', None) == module.__name__):
                    funcs.append(Func(member))
                elif (isinstance(member, type) and 
                      getattr(member, '__module__', None) == module.__name__):
                    scan_object(member, module, f"{prefix}{name}.")
        
        for module in modules:
            scan_object(module, module)
        
        return funcs