import pytest
import asyncio
from at_common_workflow.core.workflow import Workflow
from at_common_workflow.core.task import Task
from at_common_workflow.types.meta import MetaWorkflow
from at_common_workflow.core.context import Context

# Test fixtures
async def task1_func(*, x: int) -> int:
    return x + 1

async def task2_func(y: int) -> int:
    return y * 2

async def task3_func(z: int) -> int:
    return z - 1

@pytest.fixture
def simple_task1():
    return Task(
        name="task1",
        description="Add 1",
        func=task1_func,
        fixed_args={},
        inputs={"task1_input": int},
        outputs={"output1": int},
        input_mappings={"task1_input": "x"},
        output_mappings={"output1": "ret"}
    )

@pytest.fixture
def simple_task2():
    return Task(
        name="task2",
        description="Multiply by 2",
        func=task2_func,
        fixed_args={},
        inputs={"input": int},
        outputs={"output2": int},
        input_mappings={"input": "y"},
        output_mappings={"output2": "ret"}
    )

@pytest.fixture
def simple_task3():
    return Task(
        name="task3",
        description="Subtract 1",
        func=task3_func,
        fixed_args={},
        inputs={"input": int},
        outputs={"output3": int},
        input_mappings={"input": "z"},
        output_mappings={"output3": "ret"}
    )

class TestWorkflow:
    # Test initialization
    def test_init_basic(self, simple_task1):
        workflow = Workflow(
            name="test_workflow",
            description="Test workflow",
            tasks=[simple_task1],
            inputs={"task1_input": int},
            outputs={"output1": int}
        )
        assert workflow.name == "test_workflow"
        assert len(workflow.tasks) == 1

    def test_init_validation(self):
        with pytest.raises(ValueError):
            Workflow(
                name="",  # Empty name
                description="Test workflow",
                tasks=[],
                inputs={"input": int},
                outputs={"output": int}
            )

    # Test dependency management
    def test_dependency_detection(self, simple_task1, simple_task2):
        task2_modified = Task(
            name="task2",
            description="Multiply by 2",
            func=task2_func,
            fixed_args={},
            inputs={"output1": int},
            outputs={"output2": int},
            input_mappings={"output1": "y"},
            output_mappings={"output2": "ret"}
        )
        
        workflow = Workflow(
            name="dependency_test",
            description="Test dependencies",
            tasks=[simple_task1, task2_modified],
            inputs={"task1_input": int},
            outputs={"output2": int}
        )
        assert len(workflow._dependency_graph) == 2

    def test_circular_dependency_detection(self):
        task1 = Task(
            name="circular1",
            description="Circular task 1",
            func=task1_func,
            fixed_args={},
            inputs={"output2": int},
            outputs={"output1": int},
            input_mappings={"output2": "x"},
            output_mappings={"output1": "ret"}
        )
        
        task2 = Task(
            name="circular2",
            description="Circular task 2",
            func=task2_func,
            fixed_args={},
            inputs={"output1": int},
            outputs={"output2": int},
            input_mappings={"output1": "y"},
            output_mappings={"output2": "ret"}
        )

        with pytest.raises(ValueError, match="Circular dependency detected"):
            Workflow(
                name="circular_workflow",
                description="Test circular dependencies",
                tasks=[task1, task2],
                inputs={"start": int},
                outputs={"output1": int}
            )

    # Test execution
    @pytest.mark.asyncio
    async def test_simple_execution(self, simple_task1):
        workflow = Workflow(
            name="simple_workflow",
            description="Simple workflow test",
            tasks=[simple_task1],
            inputs={"task1_input": int},
            outputs={"output1": int}
        )
        
        result = await workflow.run({"task1_input": 5})
        assert result["output1"] == 6

    @pytest.mark.asyncio
    async def test_parallel_execution(self, simple_task1, simple_task2, simple_task3):
        workflow = Workflow(
            name="parallel_workflow",
            description="Parallel workflow test",
            tasks=[simple_task1, simple_task2, simple_task3],
            inputs={
                "task1_input": int,
                "input": int,
                "z": int
            },
            outputs={
                "output1": int,
                "output2": int,
                "output3": int
            }
        )
        
        result = await workflow.run({
            "task1_input": 5,
            "input": 10,
            "z": 15
        })
        
        assert result["output1"] == 6
        assert result["output2"] == 20
        assert result["output3"] == 9

    @pytest.mark.asyncio
    async def test_sequential_execution(self, simple_task1, simple_task2):
        task2_modified = Task(
            name="task2",
            description="Multiply by 2",
            func=task2_func,
            fixed_args={},
            inputs={"output1": int},
            outputs={"output2": int},
            input_mappings={"output1": "y"},
            output_mappings={"output2": "ret"}
        )
        
        workflow = Workflow(
            name="sequential_workflow",
            description="Sequential workflow test",
            tasks=[simple_task1, task2_modified],
            inputs={"task1_input": int},
            outputs={"output2": int}
        )
        
        result = await workflow.run({"task1_input": 5})
        assert result["output2"] == 12  # (5 + 1) * 2

    # Test error handling
    @pytest.mark.asyncio
    async def test_missing_input(self, simple_task1):
        workflow = Workflow(
            name="error_workflow",
            description="Error workflow test",
            tasks=[simple_task1],
            inputs={"task1_input": int},
            outputs={"output1": int}
        )
        
        with pytest.raises(ValueError):
            await workflow.run({})

    @pytest.mark.asyncio
    async def test_task_execution_error(self):
        async def failing_task_func(dummy: int = 0) -> int:
            raise RuntimeError("Task failed")
        
        failing_task = Task(
            name="failing_task",
            description="Task that fails",
            func=failing_task_func,
            fixed_args={},
            inputs={"dummy": int},
            outputs={"output": int},
            input_mappings={"dummy": "dummy"},
            output_mappings={"output": "ret"}
        )
        
        workflow = Workflow(
            name="failing_workflow",
            description="Workflow with failing task",
            tasks=[failing_task],
            inputs={"dummy": int},
            outputs={"output": int}
        )
        
        with pytest.raises(RuntimeError):
            await workflow.run({"dummy": 0})

    # Test metadata conversion
    def test_to_meta(self, simple_task1):
        workflow = Workflow(
            name="meta_workflow",
            description="Metadata test workflow",
            tasks=[simple_task1],
            inputs={"task1_input": int},
            outputs={"output1": int}
        )
        
        meta = workflow.to_meta()
        assert isinstance(meta, MetaWorkflow)
        assert meta.name == workflow.name
        assert meta.description == workflow.description

    def test_from_meta(self, simple_task1):
        original = Workflow(
            name="original_workflow",
            description="Original workflow",
            tasks=[simple_task1],
            inputs={"task1_input": int},
            outputs={"output1": int}
        )
        
        meta = original.to_meta()
        reconstructed = Workflow.from_meta(meta)
        
        assert reconstructed.name == original.name
        assert reconstructed.description == original.description
        assert len(reconstructed.tasks) == len(original.tasks)

    # Test cancellation
    @pytest.mark.asyncio
    async def test_workflow_cancellation(self):
        async def long_task_func(*args) -> int:
            try:
                await asyncio.sleep(10)
                return 42
            except asyncio.CancelledError:
                raise

        long_task = Task(
            name="long_task",
            description="Long-running task",
            func=long_task_func,
            fixed_args={},
            inputs={},
            outputs={"output": int},
            input_mappings={},
            output_mappings={"output": "ret"}
        )
        
        workflow = Workflow(
            name="cancellation_workflow",
            description="Cancellation test workflow",
            tasks=[long_task],
            inputs={},
            outputs={"output": int}
        )
        
        with pytest.raises((asyncio.CancelledError, TimeoutError)):
            async with asyncio.timeout(0.1):
                await workflow.run({})

    @pytest.mark.asyncio
    async def test_task_status_tracking(self, simple_task1):
        workflow = Workflow(
            name="status_workflow",
            description="Status tracking test",
            tasks=[simple_task1],
            inputs={"task1_input": int},
            outputs={"output1": int}
        )
        
        await workflow.run({"task1_input": 5})
        assert workflow._task_execution_info[simple_task1].status == "COMPLETED"

    @pytest.mark.asyncio
    async def test_invalid_output_type(self):
        async def bad_type_func(x: int) -> str:
            return "not an int"
        
        task = Task(
            name="bad_type",
            description="Returns wrong type",
            func=bad_type_func,
            fixed_args={},
            inputs={"input": int},
            outputs={"output": int},
            input_mappings={"input": "x"},
            output_mappings={"output": "ret"}
        )
        
        workflow = Workflow(
            name="type_error_workflow",
            description="Type error test",
            tasks=[task],
            inputs={"input": int},
            outputs={"output": int}
        )
        
        with pytest.raises(RuntimeError, match="Task execution failed: Output 'output' expected type <class 'int'>, got <class 'str'>"):
            await workflow.run({"input": 5})

    @pytest.mark.asyncio
    async def test_large_workflow(self):
        tasks = []
        for i in range(100):
            tasks.append(Task(
                name=f"task_{i}",
                description=f"Task {i}",
                func=lambda x: x,
                fixed_args={},
                inputs={"input": int},
                outputs={"output": int},
                input_mappings={"input": "x"},
                output_mappings={"output": "ret"}
            ))
        
        workflow = Workflow(
            name="large_workflow",
            description="Large workflow test",
            tasks=tasks,
            inputs={"input": int},
            outputs={"output": int}
        )
        
        result = await workflow.run({"input": 1})
        assert result["output"] == 1

    @pytest.mark.asyncio
    async def test_partial_workflow_completion(self):
        async def failing_task_func():
            raise RuntimeError("Task failed")
        
        # Create a Task instance for simple_task1
        task1 = Task(
            name="simple_task1",
            description="Simple task 1",
            func=task1_func,  # Changed from simple_task1 to task1_func
            fixed_args={},
            inputs={"task1_input": int},
            outputs={"output1": int},
            input_mappings={"task1_input": "x"},
            output_mappings={"output1": "ret"}
        )

        task2 = Task(
            name="failing_task",
            description="Failing task",
            func=failing_task_func,
            fixed_args={},
            inputs={},
            outputs={"output": int},
            input_mappings={},
            output_mappings={"output": "ret"}
        )

        workflow = Workflow(
            name="partial_workflow",
            description="Partial completion test",
            tasks=[task1, task2],
            inputs={"task1_input": int},
            outputs={"output1": int, "output": int}
        )
        
        with pytest.raises(RuntimeError):
            await workflow.run({"task1_input": 5})
        
        # Check that task1 completed successfully
        assert workflow._task_execution_info[task1].status == "COMPLETED"
        assert workflow._task_execution_info[task2].status == "FAILED"

    @pytest.mark.asyncio
    async def test_workflow_timeout(self):
        async def slow_task():
            await asyncio.sleep(2)
            return 42
        
        task = Task(
            name="slow_task",
            description="Slow task",
            func=slow_task,
            fixed_args={},
            inputs={},
            outputs={"output": int},
            input_mappings={},
            output_mappings={"output": "ret"}
        )
        
        workflow = Workflow(
            name="timeout_workflow",
            description="Timeout test",
            tasks=[task],
            inputs={},
            outputs={"output": int}
        )
        
        with pytest.raises(asyncio.TimeoutError):
            async with asyncio.timeout(1):
                await workflow.run({})