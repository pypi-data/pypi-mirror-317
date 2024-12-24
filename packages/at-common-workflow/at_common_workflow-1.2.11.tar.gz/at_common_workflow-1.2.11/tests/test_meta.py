import pytest
from at_common_workflow.types.meta import (
    AllowedTypes, ValidatedDict, Schema, Mappings, Arguments, MetaFunc, MetaTask, MetaWorkflow, WorkflowValidationError, type_to_string, Dict, List, Any
)
import time

class TestAllowedTypes:
    def test_get_types(self):
        types = AllowedTypes.get_types()
        assert isinstance(types, tuple)
        assert str in types
        assert int in types
        assert float in types
        assert bool in types
        assert dict in types
        assert list in types
        assert Dict in types
        assert List in types

    def test_get_type_map(self):
        type_map = AllowedTypes.get_type_map()
        assert isinstance(type_map, dict)
        assert type_map['str'] == str
        assert type_map['int'] == int
        assert type_map['float'] == float
        assert type_map['bool'] == bool
        assert type_map['dict'] == dict
        assert type_map['list'] == list
        assert type_map['Dict'] == Dict
        assert type_map['List'] == List

class TestSchema:
    def test_schema_serialization(self):
        schema = Schema({'key': str})
        serialized = schema.to_dict()
        assert serialized == {'key': 'str'}
        
        deserialized = Schema.from_dict(serialized)
        assert isinstance(deserialized, Schema)
        assert dict(deserialized) == {'key': str}

    def test_invalid_type_name(self):
        with pytest.raises(KeyError):
            Schema.from_dict({'key': 'invalid_type'})

class TestMappings:
    def test_schema_validation(self):
        source_schema = Schema({'input': str})
        target_schema = Schema({'output': str})
        
        # Valid mapping
        valid_mapping = Mappings(
            {'input': 'output'}, 
            source_schema=source_schema,
            target_schema=target_schema
        )
        assert dict(valid_mapping) == {'input': 'output'}
        
        # Invalid source key
        with pytest.raises(KeyError, match="Mapping source 'invalid' not found in schema"):
            Mappings(
                {'invalid': 'output'},
                source_schema=source_schema,
                target_schema=target_schema
            )
        
        # Invalid target key
        with pytest.raises(KeyError, match="Mapping target 'invalid' not found in schema"):
            Mappings(
                {'input': 'invalid'},
                source_schema=source_schema,
                target_schema=target_schema
            )

    def test_mappings_serialization(self):
        mappings = Mappings({'source': 'target'})
        serialized = mappings.to_dict()
        assert serialized == {'source': 'target'}
        
        deserialized = Mappings.from_dict(serialized)
        assert isinstance(deserialized, Mappings)
        assert dict(deserialized) == {'source': 'target'}

class TestArguments:
    def test_none_value_validation(self):
        with pytest.raises(ValueError, match="Argument 'key' cannot be None"):
            Arguments({'key': None})

    def test_type_validation_with_allowed_types(self):
        # Test all allowed types
        valid_args = {
            'str_val': 'string',
            'int_val': 42,
            'float_val': 3.14,
            'bool_val': True,
            'dict_val': {'nested': 'value'},
            'list_val': [1, 2, 3]
        }
        args = Arguments(valid_args)
        assert dict(args) == valid_args

        # Test custom type (should work because Any is allowed)
        class CustomType:
            pass

        custom_args = Arguments({'custom': CustomType()})
        assert isinstance(custom_args['custom'], CustomType)

    def test_type_validation_with_any(self):
        # Test various Python types that should be accepted with Any
        class CustomClass:
            def __init__(self, value):
                self.value = value

        class ChildClass(CustomClass):
            pass

        valid_complex_args = {
            'custom_class': CustomClass(42),
            'child_class': ChildClass("test"),
            'lambda_func': lambda x: x * 2,
            'generator': (i for i in range(5)),
            'complex_obj': complex(1, 2),
            'module_obj': time,  # Using the time module as an example
            'none_type': type(None),
            'nested_structure': {
                'tuple': (1, "string", 3.14),
                'set': {1, 2, 3},
                'custom': CustomClass(123)
            }
        }

        # All these should be accepted because Any is allowed
        args = Arguments(valid_complex_args)
        assert dict(args) == valid_complex_args

        # Test that methods and bound methods are accepted
        class WithMethods:
            def instance_method(self):
                pass
            
            @classmethod
            def class_method(cls):
                pass
            
            @staticmethod
            def static_method():
                pass

        obj = WithMethods()
        method_args = {
            'instance_method': obj.instance_method,
            'class_method': WithMethods.class_method,
            'static_method': WithMethods.static_method
        }
        
        args = Arguments(method_args)
        assert dict(args) == method_args

        # Test with mixed standard and custom types
        mixed_args = {
            'str_val': 'string',
            'custom_val': CustomClass(42),
            'list_of_custom': [CustomClass(i) for i in range(3)],
            'dict_of_custom': {
                'a': CustomClass(1),
                'b': ChildClass(2)
            }
        }
        
        args = Arguments(mixed_args)
        assert dict(args) == mixed_args

class TestValidatedDict:
    def test_abstract_class(self):
        with pytest.raises(TypeError):
            ValidatedDict({})  # Cannot instantiate abstract class

    def test_to_dict_conversion(self):
        class ConcreteDict(ValidatedDict[str]):
            def _validate(self, data):
                pass

        data = {'key': 'value'}
        validated = ConcreteDict(data)
        assert validated.to_dict() == data 

class TestTypeToString:
    def test_simple_types(self):
        assert type_to_string(str) == 'str'
        assert type_to_string(int) == 'int'
        
    def test_generic_types(self):
        assert type_to_string(list[str]) == 'list[str]'
        assert type_to_string(dict[str, int]) == 'dict[str, int]'

class TestMetaFunc:
    def test_valid_creation(self):
        func = MetaFunc(
            module='test_module',
            name='test_func',
            args=Schema({'input': str}),
            rets=Schema({'output': int}),
            has_kwargs=True
        )
        assert func.module == 'test_module'
        assert func.name == 'test_func'
        assert func.has_kwargs is True
        
    def test_invalid_creation(self):
        with pytest.raises(WorkflowValidationError):
            MetaFunc(module='', name='test')
        with pytest.raises(WorkflowValidationError):
            MetaFunc(module='test', name='')
            
    def test_serialization(self):
        func = MetaFunc(
            module='test_module',
            name='test_func',
            args=Schema({'input': str}),
            rets=Schema({'output': int}),
            has_kwargs=True
        )
        serialized = func.to_dict()
        deserialized = MetaFunc.from_dict(serialized)
        assert deserialized.module == func.module
        assert deserialized.name == func.name
        assert dict(deserialized.args) == dict(func.args)
        assert dict(deserialized.rets) == dict(func.rets)
        assert deserialized.has_kwargs == func.has_kwargs

    def test_default_has_kwargs(self):
        """Test that has_kwargs defaults to False"""
        func = MetaFunc(
            module='test_module',
            name='test_func',
            args=Schema({}),
            rets=Schema({})
        )
        assert func.has_kwargs is False

    def test_kwargs_serialization(self):
        """Test that **kwargs is filtered from args during serialization"""
        func = MetaFunc(
            module='test_module',
            name='test_func',
            args=Schema({'input': str, '**kwargs': Dict[str, Any]}),
            rets=Schema({'output': int}),
            has_kwargs=True
        )
        serialized = func.to_dict()
        assert '**kwargs' not in serialized['args']
        assert serialized['has_kwargs'] is True
        
        deserialized = MetaFunc.from_dict(serialized)
        assert '**kwargs' not in deserialized.args
        assert deserialized.has_kwargs is True

class TestMetaTask:
    def test_complete_task_creation(self):
        func = MetaFunc('test_module', 'test_func')
        task = MetaTask(
            name='test_task',
            description='Test task description',
            func=func,
            fixed_args=Arguments({'fixed': 'value'}),
            inputs=Schema({'input': str}),
            outputs=Schema({'output': int}),
            input_mappings=Mappings({'input': 'arg_input'}),
            output_mappings=Mappings({'ret_output': 'output'})
        )
        assert task.name == 'test_task'
        assert task.description == 'Test task description'
        
    def test_serialization(self):
        func = MetaFunc('test_module', 'test_func')
        task = MetaTask(
            name='test_task',
            description='Test task description',
            func=func
        )
        serialized = task.to_dict()
        deserialized = MetaTask.from_dict(serialized)
        assert deserialized.name == task.name
        assert deserialized.description == task.description
        assert deserialized.func.module == task.func.module

class TestMetaWorkflow:
    def test_workflow_creation(self):
        task1 = MetaTask(
            name='task1',
            description='First task',
            func=MetaFunc('module1', 'func1')
        )
        task2 = MetaTask(
            name='task2',
            description='Second task',
            func=MetaFunc('module2', 'func2')
        )
        workflow = MetaWorkflow(
            name='test_workflow',
            description='Test workflow',
            tasks=[task1, task2],
            inputs=Schema({'workflow_input': str}),
            outputs=Schema({'workflow_output': int})
        )
        assert len(workflow.tasks) == 2
        assert workflow.name == 'test_workflow'
        
    def test_workflow_serialization(self):
        task = MetaTask(
            name='task1',
            description='Test task',
            func=MetaFunc('module1', 'func1')
        )
        workflow = MetaWorkflow(
            name='test_workflow',
            description='Test workflow',
            tasks=[task],
            inputs=Schema({}),
            outputs=Schema({})
        )
        serialized = workflow.to_dict()
        deserialized = MetaWorkflow.from_dict(serialized)
        assert deserialized.name == workflow.name
        assert deserialized.description == workflow.description
        assert len(deserialized.tasks) == len(workflow.tasks)
        assert deserialized.tasks[0].name == workflow.tasks[0].name