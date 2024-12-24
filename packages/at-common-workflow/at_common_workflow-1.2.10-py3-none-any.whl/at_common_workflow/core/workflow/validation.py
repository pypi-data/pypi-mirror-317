from typing import Dict, Any, Set
from ..task import Task
from ...types.meta import Schema

class WorkflowValidator:
    @staticmethod
    def validate_workflow(name: str, description: str, tasks: list[Task], 
                         inputs: Schema, outputs: Schema, dependency_graph: Dict) -> None:
        """Perform comprehensive workflow validation."""
        WorkflowValidator._validate_basics(name, description, tasks)
        WorkflowValidator._validate_task_names(tasks)
        WorkflowValidator._check_for_cycles(tasks, dependency_graph)
        WorkflowValidator._validate_schema(inputs, outputs)
        WorkflowValidator._validate_task_connections(tasks, inputs)
        WorkflowValidator._validate_type_compatibility(tasks)

    @staticmethod
    def _validate_basics(name: str, description: str, tasks: list[Task]) -> None:
        if not name:
            raise ValueError("Workflow name cannot be empty")
        if not description:
            raise ValueError("Workflow description cannot be empty")
        if not tasks:
            raise ValueError("Workflow must contain at least one task")

    @staticmethod
    def _validate_task_names(tasks: list[Task]) -> None:
        task_names = [task.name for task in tasks]
        if len(task_names) != len(set(task_names)):
            duplicates = [name for name in task_names if task_names.count(name) > 1]
            raise ValueError(f"Duplicate task names found: {duplicates}")

    @staticmethod
    def _validate_schema(inputs: Schema, outputs: Schema) -> None:
        if not isinstance(inputs, Schema):
            raise TypeError("Workflow inputs must be a Schema instance")
        if not isinstance(outputs, Schema):
            raise TypeError("Workflow outputs must be a Schema instance")

    @staticmethod
    def _validate_task_connections(tasks: list[Task], inputs: Schema) -> None:
        for task in tasks:
            for required_key in task.inputs:
                if required_key in inputs:
                    continue
                
                satisfied = False
                for provider in tasks:
                    if required_key in provider.outputs:
                        satisfied = True
                        break
                    
                if not satisfied:
                    raise ValueError(
                        f"Task '{task.name}' requires '{required_key}' but no provider found"
                    )

    @staticmethod
    def _check_for_cycles(tasks: list[Task], dependency_graph: Dict[Task, Set[Task]]) -> None:
        visited = set()
        path = set()

        def dfs(task: Task) -> None:
            visited.add(task)
            path.add(task)
            
            for dependent in dependency_graph[task]:
                if dependent in path:
                    raise ValueError(f"Circular dependency detected involving task '{task.name}'")
                if dependent not in visited:
                    dfs(dependent)
                    
            path.remove(task)

        for task in tasks:
            if task not in visited:
                dfs(task)

    @staticmethod
    def _validate_type_compatibility(tasks: list[Task]) -> None:
        for task in tasks:
            for req_key, req_type in task.inputs.items():
                if not isinstance(req_type, type):
                    raise TypeError(f"Invalid type specification for {req_key} in {task.name}")

    @staticmethod
    def validate_input_data(input_data: Dict[str, Any], inputs: Schema) -> None:
        missing_inputs = set(inputs.keys()) - set(input_data.keys())
        if missing_inputs:
            raise ValueError(f"Missing required input(s): {missing_inputs}")

        for key, value in input_data.items():
            if key in inputs:
                expected_type = inputs[key]
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"Invalid type for input '{key}': expected {expected_type}, got {type(value)}"
                    )