import pytest
from at_common_workflow.core.context import Context
from threading import Thread
import time, asyncio

class TestContext:
    
    def test_init_empty(self):
        context = Context()
        assert len(context) == 0

    def test_init_with_data(self):
        initial_data = {"key1": "value1", "key2": 2}
        context = Context(initial_data)
        assert dict(context) == initial_data
        # Verify deep copy
        initial_data["key1"] = "changed"
        assert context["key1"] == "value1"

    def test_setitem_getitem(self):
        context = Context()
        context["test"] = {"nested": "value"}
        assert context["test"] == {"nested": "value"}
        
        # Test deep copy on get
        retrieved = context["test"]
        retrieved["nested"] = "changed"
        assert context["test"]["nested"] == "value"

    def test_delitem(self):
        context = Context({"key": "value"})
        del context["key"]
        assert "key" not in context
        with pytest.raises(KeyError):
            del context["nonexistent"]

    def test_clear(self):
        context = Context({"key1": "value1", "key2": "value2"})
        context.clear()
        assert len(context) == 0

    def test_update(self):
        context = Context({"key1": "value1"})
        context.update({"key2": "value2", "key1": "updated"})
        assert context["key1"] == "updated"
        assert context["key2"] == "value2"

    def test_get(self):
        context = Context({"key": {"nested": "value"}})
        assert context.get("key") == {"nested": "value"}
        assert context.get("nonexistent") is None
        assert context.get("nonexistent", "default") == "default"
        
        # Test deep copy
        retrieved = context.get("key")
        retrieved["nested"] = "changed"
        assert context["key"]["nested"] == "value"

    def test_contains(self):
        context = Context({"key": "value"})
        assert "key" in context
        assert "nonexistent" not in context

    def test_validate_key(self):
        context = Context()
        with pytest.raises(TypeError, match="Key must be a string"):
            context[123] = "value"
        with pytest.raises(TypeError, match="Key must be a string"):
            context.get(123)
        with pytest.raises(TypeError, match="Key must be a string"):
            123 in context

    def test_thread_safety(self):
        context = Context()
        iterations = 1000
        
        def writer():
            for i in range(iterations):
                context[f"key{i}"] = i
                time.sleep(0.0001)  # Force thread switching
                
        def reader():
            read_count = 0
            for _ in range(iterations):
                try:
                    _ = context[f"key{read_count}"]
                    read_count += 1
                except KeyError:
                    pass
                time.sleep(0.0001)  # Force thread switching

        # Create and start threads
        writer_thread = Thread(target=writer)
        reader_thread = Thread(target=reader)
        
        writer_thread.start()
        reader_thread.start()
        
        writer_thread.join()
        reader_thread.join()
        
        # Verify all writes completed
        assert len(context) == iterations

    def test_copy(self):
        original = Context({"key": {"nested": "value"}})
        copied = original.copy()
        
        # Verify it's a different object
        assert original is not copied
        
        # Verify contents are the same
        assert dict(original) == dict(copied)
        
        # Verify deep copy
        copied["key"]["nested"] = "changed"
        assert original["key"]["nested"] == "value"

    def test_nested_structures(self):
        context = Context()
        nested_dict = {
            "level1": {
                "level2": {
                    "level3": "value"
                }
            }
        }
        context["nested"] = nested_dict
        
        # Modify original
        nested_dict["level1"]["level2"]["level3"] = "changed"
        
        # Verify context value remained unchanged
        assert context["nested"]["level1"]["level2"]["level3"] == "value"

    def test_complex_values(self):
        context = Context()
        
        # Test with various types
        test_data = {
            "list": [1, 2, 3],
            "tuple": (4, 5, 6),
            "set": {7, 8, 9},
            "dict": {"key": "value"},
            "none": None,
            "int": 42,
            "float": 3.14,
            "bool": True,
            "str": "test"
        }
        
        context.update(test_data)
        
        # Verify all values
        for key, value in test_data.items():
            assert context[key] == value

    def test_concurrent_update_operations(self):
        """Test multiple concurrent update operations on the context"""
        context = Context()
        def updater(start, end):
            for i in range(start, end):
                context.update({f"key{i}": i})
        
        threads = [
            Thread(target=updater, args=(i*100, (i+1)*100))
            for i in range(10)
        ]
        [t.start() for t in threads]
        [t.join() for t in threads]
        
        assert len(context) == 1000
        for i in range(1000):
            assert context[f"key{i}"] == i

    @pytest.mark.asyncio
    async def test_concurrent_context_access(self):
        context = Context({"key": 0})
        async def increment():
            for _ in range(100):
                context["key"] = context["key"] + 1
        await asyncio.gather(*[increment() for _ in range(10)])
        assert context["key"] == 1000