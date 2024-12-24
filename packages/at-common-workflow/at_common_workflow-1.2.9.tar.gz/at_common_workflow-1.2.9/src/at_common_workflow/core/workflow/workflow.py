from typing import Union, Dict, List, Any
from ...types.meta import Schema, MetaWorkflow
from ..task import Task
from ..context import Context
from .execution import TaskExecutionInfo
from .dependency import DependencyManager
from .validation import WorkflowValidator
from .execution import WorkflowExecutor
import asyncio
import logging

logger = logging.getLogger(__name__)

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
        
        # Initialize internal state
        self._task_execution_info = {
            task: TaskExecutionInfo(status="PENDING")
            for task in tasks
        }
        
        # Build dependency graphs
        self._dependency_graph = DependencyManager.build_dependency_graph(tasks)
        self._reverse_dependency_graph = DependencyManager.build_reverse_dependency_graph(
            self._dependency_graph
        )
        
        # Validate the workflow structure
        WorkflowValidator.validate_workflow(
            name, description, tasks, self.inputs, self.outputs, self._dependency_graph
        )

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
            # Validate input data
            WorkflowValidator.validate_input_data(input_data, self.inputs)
            context = Context(input_data)
            
            # Initialize queues for task management
            ready_tasks = asyncio.Queue()
            completed_tasks = asyncio.Queue()
            
            # Get and queue initial tasks
            initial_tasks = DependencyManager.get_initial_tasks(self.tasks, self._dependency_graph)
            for task in initial_tasks:
                await ready_tasks.put(task)

            # Execute workflow
            await WorkflowExecutor.execute_workflow(
                self.name,
                self.tasks,
                self._task_execution_info,
                self._reverse_dependency_graph,
                self._dependency_graph,
                ready_tasks,
                completed_tasks,
                context
            )

            # Extract and validate outputs
            return self._extract_outputs(context)

        except Exception as e:
            logger.error(f"Workflow '{self.name}' failed: {str(e)}")
            raise

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