from typing import Dict, Set
from collections import defaultdict
from ..task import Task

class DependencyManager:
    @staticmethod
    def build_dependency_graph(tasks: list[Task]) -> Dict[Task, Set[Task]]:
        """Build a graph of task dependencies."""
        graph = defaultdict(set)
        for task in tasks:
            for other_task in tasks:
                if task != other_task:
                    if any(key in other_task.outputs for key in task.inputs.keys()):
                        graph[task].add(other_task)
        return graph

    @staticmethod
    def build_reverse_dependency_graph(dependency_graph: Dict[Task, Set[Task]]) -> Dict[Task, Set[Task]]:
        """Build a reverse graph of task dependencies."""
        graph = defaultdict(set)
        for task, deps in dependency_graph.items():
            for dep in deps:
                graph[dep].add(task)
        return graph

    @staticmethod
    def get_initial_tasks(tasks: list[Task], dependency_graph: Dict[Task, Set[Task]]) -> list[Task]:
        """Get tasks that can be executed immediately."""
        return [
            task for task in tasks
            if not dependency_graph[task]
        ]