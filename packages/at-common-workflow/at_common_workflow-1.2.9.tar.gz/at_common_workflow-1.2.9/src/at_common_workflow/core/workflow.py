from typing import Union, Dict, List, Set, Any, Optional, TypeVar
from collections import defaultdict
from dataclasses import dataclass
from ..types.meta import Schema, MetaWorkflow
from .task import Task
from .context import Context
import asyncio
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')

@dataclass
class TaskExecutionInfo:
    """Contains execution information for a task."""
    task: Task
    status: str
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    error: Optional[Exception] = None
    dependencies_met: bool = False

class Workflow:
    """A sophisticated workflow implementation that manages task execution in a DAG structure.
    
    Example:
        >>> workflow = Workflow(
        ...     name="example",
        ...     description="Example workflow",
        ...     tasks=[task1, task2],
        ...     inputs=Schema({"input1": str}),
        ...     outputs=Schema({"output1": str})
        ... )
        >>> result = await workflow.run({"input1": "value"})
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        tasks: List[Task],
        inputs: Union[Dict[str, type], Schema],
        outputs: Union[Dict[str, type], Schema]
    ):
        """
        Initialize a new workflow.

        Args:
            name: Unique identifier for the workflow
            description: Human-readable description
            tasks: List of tasks to execute
            inputs: Schema for workflow inputs
            outputs: Schema for workflow outputs
        """
        self.name = name
        self.description = description
        self.tasks = tasks
        self.inputs = inputs if isinstance(inputs, Schema) else Schema(inputs)
        self.outputs = outputs if isinstance(outputs, Schema) else Schema(outputs)
        
        # Internal state
        self._task_execution_info = {
            task: TaskExecutionInfo(task=task, status="PENDING")
            for task in tasks
        }
        self._dependency_graph = self._build_dependency_graph()
        self._reverse_dependency_graph = self._build_reverse_dependency_graph()
        
        # Validate the workflow structure
        self._validate_workflow()

    def _build_dependency_graph(self) -> Dict[Task, Set[Task]]:
        """Build a graph of task dependencies."""
        graph = defaultdict(set)
        for task in self.tasks:
            for other_task in self.tasks:
                if task != other_task:
                    if any(key in other_task.outputs for key in task.inputs.keys()):
                        graph[task].add(other_task)
        return graph

    def _build_reverse_dependency_graph(self) -> Dict[Task, Set[Task]]:
        """Build a reverse graph of task dependencies."""
        graph = defaultdict(set)
        for task, deps in self._dependency_graph.items():
            for dep in deps:
                graph[dep].add(task)
        return graph

    def _validate_workflow(self) -> None:
        """Perform comprehensive workflow validation."""
        # Basic validations
        if not self.name:
            raise ValueError("Workflow name cannot be empty")
        if not self.description:
            raise ValueError("Workflow description cannot be empty")
        if not self.tasks:
            raise ValueError("Workflow must contain at least one task")
        
        # Other validations
        self._validate_task_names()
        self._validate_workflow_inputs()
        self._validate_workflow_outputs()
        self._validate_task_connections()
        self._check_for_cycles()
        self._validate_type_compatibility()

    def _validate_task_names(self) -> None:
        """Ensure task names are unique."""
        task_names = [task.name for task in self.tasks]
        if len(task_names) != len(set(task_names)):
            duplicates = [name for name in task_names if task_names.count(name) > 1]
            raise ValueError(f"Duplicate task names found: {duplicates}")

    def _validate_type_compatibility(self) -> None:
        """Validate type compatibility between connected tasks."""
        for task in self.tasks:
            for req_key, req_type in task.inputs.items():
                # Validate input types
                if not isinstance(req_type, type):
                    raise TypeError(f"Invalid type specification for {req_key} in {task.name}")
                
                # Find provider for this requirement
                provider = None
                for other_task in self.tasks:
                    if req_key in other_task.outputs:
                        provider = other_task
                        break
                
                # If provider found, validate type compatibility
                if provider:
                    provided_type = provider.outputs[req_key]
                    if not issubclass(provided_type, req_type):
                        raise TypeError(
                            f"Type mismatch: task '{provider.name}' provides '{req_key}' "
                            f"as {provided_type}, but '{task.name}' requires {req_type}"
                        )

    def _check_for_cycles(self) -> None:
        """Check for cycles in the dependency graph using DFS."""
        visited = set()
        path = set()

        def dfs(task: Task) -> None:
            visited.add(task)
            path.add(task)
            
            for dependent in self._dependency_graph[task]:
                if dependent in path:
                    raise ValueError(f"Circular dependency detected involving task '{task.name}'")
                if dependent not in visited:
                    dfs(dependent)
                    
            path.remove(task)

        for task in self.tasks:
            if task not in visited:
                dfs(task)

    def _validate_task_connections(self) -> None:
        """Validate that all task dependencies can be satisfied."""
        for task in self.tasks:
            for required_key in task.inputs:
                # Check if requirement is satisfied by workflow inputs
                if required_key in self.inputs:
                    continue
                
                # Check if requirement is satisfied by any task outputs
                satisfied = False
                for provider in self.tasks:
                    if required_key in provider.outputs:
                        satisfied = True
                        break
                    
                if not satisfied:
                    raise ValueError(
                        f"Task '{task.name}' requires '{required_key}' but no provider found"
                    )

    def _validate_workflow_inputs(self) -> None:
        """Validate workflow input schema."""
        if not isinstance(self.inputs, Schema):
            raise TypeError("Workflow inputs must be a Schema instance")
        if not self.inputs:
            raise ValueError("Workflow must define input schema")

    def _validate_workflow_outputs(self) -> None:
        """Validate workflow output schema."""
        if not isinstance(self.outputs, Schema):
            raise TypeError("Workflow outputs must be a Schema instance")
        if not self.outputs:
            raise ValueError("Workflow must define output schema")

    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the workflow with the given input data.

        Args:
            input_data: Dictionary containing the workflow inputs

        Returns:
            Dictionary containing the workflow outputs

        Raises:
            ValueError: If input data is invalid
            RuntimeError: If workflow execution fails
        """
        try:
            # Validate and prepare
            self._validate_input_data(input_data)
            context = Context(input_data)
            
            # Get initial tasks that have no dependencies
            ready_tasks = asyncio.Queue()
            completed_tasks = asyncio.Queue()
            
            # Initialize with tasks that have no dependencies
            initial_tasks = self._get_initial_tasks()
            for task in initial_tasks:
                await ready_tasks.put(task)

            # Execute workflow
            await self._execute_workflow(ready_tasks, completed_tasks, context)

            # Extract and validate outputs
            return self._extract_outputs(context)

        except Exception as e:
            logger.error(f"Workflow '{self.name}' failed: {str(e)}")
            raise

    async def _execute_workflow(
        self,
        ready_tasks: asyncio.Queue,
        completed_tasks: asyncio.Queue,
        context: Context
    ) -> None:
        """Execute the workflow tasks with maximum parallelism."""
        try:
            completed_count = 0
            total_tasks = len(self.tasks)
            running_tasks = set()

            while completed_count < total_tasks:
                # Start all ready tasks immediately
                while not ready_tasks.empty():
                    task = await ready_tasks.get()
                    info = self._task_execution_info[task]
                    info.status = "RUNNING"
                    info.start_time = asyncio.get_event_loop().time()
                    
                    # Create and start task execution
                    task_coro = self._execute_task(task, info, context, completed_tasks)
                    running_tasks.add(asyncio.create_task(task_coro))

                # Wait for any task to complete
                if running_tasks:
                    done, running_tasks = await asyncio.wait(
                        running_tasks, 
                        return_when=asyncio.FIRST_COMPLETED
                    )
                    
                    # Handle completed tasks
                    for task_future in done:
                        completed_task = await completed_tasks.get()
                        completed_count += 1
                        
                        # Find new ready tasks
                        new_ready_tasks = self._get_ready_tasks(completed_task)
                        for new_task in new_ready_tasks:
                            await ready_tasks.put(new_task)
                        
                        # Log progress
                        logger.info(f"Workflow '{self.name}' progress: {completed_count}/{total_tasks} tasks completed")

        except Exception as e:
            # Cancel any running tasks
            for task in running_tasks:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass  # Expected for cancelled tasks
            raise RuntimeError(f"Workflow execution failed: {str(e)}") from e

    async def _execute_task(
        self,
        task: Task,
        info: TaskExecutionInfo,
        context: Context,
        completed_tasks: asyncio.Queue
    ) -> None:
        """Execute a single task and update its status."""
        try:
            await task.execute(context)
            info.end_time = asyncio.get_event_loop().time()
            info.status = "COMPLETED"
            await completed_tasks.put(task)
        except Exception as e:
            info.status = "FAILED"
            info.error = e
            raise

    def _get_ready_tasks(self, completed_task: Task) -> List[Task]:
        """Get tasks that are ready to execute after a task completes."""
        ready_tasks = []
        dependent_tasks = self._reverse_dependency_graph[completed_task]
        
        for task in dependent_tasks:
            # Check if all dependencies are completed
            if all(
                self._task_execution_info[dep].status == "COMPLETED"
                for dep in self._dependency_graph[task]
            ):
                ready_tasks.append(task)
                self._task_execution_info[task].dependencies_met = True
        
        return ready_tasks

    def _get_initial_tasks(self) -> List[Task]:
        """Get tasks that can be executed immediately."""
        return [
            task for task in self.tasks
            if not self._dependency_graph[task]
        ]

    def _validate_input_data(self, input_data: Dict[str, Any]) -> None:
        """Validate input data against workflow schema."""
        missing_inputs = set(self.inputs.keys()) - set(input_data.keys())
        if missing_inputs:
            raise ValueError(f"Missing required input(s): {missing_inputs}")

        for key, value in input_data.items():
            if key in self.inputs:
                expected_type = self.inputs[key]
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"Invalid type for input '{key}': expected {expected_type}, got {type(value)}"
                    )

    def _extract_outputs(self, context: Context) -> Dict[str, Any]:
        """Extract and validate workflow outputs from context."""
        output_data = {}
        for key in self.outputs.keys():
            if key not in context:
                raise RuntimeError(f"Expected output '{key}' not found in context")
            output_data[key] = context[key]
        return output_data

    def to_meta(self) -> MetaWorkflow:
        """Convert workflow to metadata representation."""
        return MetaWorkflow(
            name=self.name,
            description=self.description,
            tasks=[task.to_meta() for task in self.tasks],
            inputs=self.inputs,
            outputs=self.outputs
        )

    @classmethod
    def from_meta(cls, meta: MetaWorkflow) -> 'Workflow':
        """Create a workflow from metadata."""
        return cls(
            name=meta.name,
            description=meta.description,
            tasks=[Task.from_meta(task_meta) for task_meta in meta.tasks],
            inputs=meta.inputs,
            outputs=meta.outputs
        )
