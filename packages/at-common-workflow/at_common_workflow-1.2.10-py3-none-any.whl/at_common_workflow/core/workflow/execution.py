import asyncio
import logging
from typing import Dict
from at_common_workflow.types.meta import TaskExecutionInfo
from at_common_workflow.core.task import Task
from at_common_workflow.core.context import Context

logger = logging.getLogger(__name__)

class WorkflowExecutor:
    @staticmethod
    async def execute_workflow(
        workflow_name: str,
        tasks: list[Task],
        task_execution_info: Dict[Task, TaskExecutionInfo],
        reverse_dependency_graph: Dict[Task, set],
        dependency_graph: Dict[Task, set],
        ready_tasks: asyncio.Queue,
        completed_tasks: asyncio.Queue,
        context: Context
    ) -> None:
        running_tasks = set()
        try:
            completed_count = 0
            total_tasks = len(tasks)

            while completed_count < total_tasks:
                while not ready_tasks.empty():
                    task = await ready_tasks.get()
                    info = task_execution_info[task]
                    info.status = "RUNNING"
                    info.start_time = asyncio.get_event_loop().time()
                    
                    task_coro = WorkflowExecutor.execute_task(task, info, context, completed_tasks)
                    running_tasks.add(asyncio.create_task(task_coro))

                if running_tasks:
                    done, pending = await asyncio.wait(
                        running_tasks, 
                        return_when=asyncio.FIRST_COMPLETED
                    )
                    running_tasks = pending
                    
                    for task_future in done:
                        try:
                            await task_future
                            completed_task = await completed_tasks.get()
                            completed_count += 1
                            
                            new_ready_tasks = WorkflowExecutor.get_ready_tasks(
                                completed_task,
                                reverse_dependency_graph,
                                dependency_graph,
                                task_execution_info
                            )
                            for new_task in new_ready_tasks:
                                await ready_tasks.put(new_task)
                            
                            logger.info(f"Workflow '{workflow_name}' progress: {completed_count}/{total_tasks} tasks completed")
                        except Exception as e:
                            raise RuntimeError(f"Task execution failed: {str(e)}") from e

        except Exception as e:
            logger.error(f"Workflow execution failed: {str(e)}")
            raise
        finally:
            # Clean up any running tasks
            for task in running_tasks:
                task.cancel()
            if running_tasks:
                await asyncio.gather(*running_tasks, return_exceptions=True)

    @staticmethod
    async def execute_task(
        task: Task,
        info: TaskExecutionInfo,
        context: Context,
        completed_tasks: asyncio.Queue
    ) -> None:
        try:
            await task.execute(context)
            info.end_time = asyncio.get_event_loop().time()
            info.status = "COMPLETED"
            await completed_tasks.put(task)
        except Exception as e:
            info.status = "FAILED"
            info.error = e
            info.end_time = asyncio.get_event_loop().time()
            await completed_tasks.put(task)
            raise

    @staticmethod
    def get_ready_tasks(
        completed_task: Task,
        reverse_dependency_graph: Dict[Task, set],
        dependency_graph: Dict[Task, set],
        task_execution_info: Dict[Task, TaskExecutionInfo]
    ) -> list[Task]:
        ready_tasks = []
        dependent_tasks = reverse_dependency_graph[completed_task]
        
        for task in dependent_tasks:
            if all(
                task_execution_info[dep].status == "COMPLETED"
                for dep in dependency_graph[task]
            ):
                ready_tasks.append(task)
                task_execution_info[task].dependencies_met = True
        
        return ready_tasks