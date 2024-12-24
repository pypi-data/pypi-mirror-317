import pytest
from at_common_workflow.types.meta import (
    AllowedTypes, ValidatedDict, Schema, Mappings, Arguments, MetaFunc, MetaTask, MetaWorkflow, WorkflowValidationError, type_to_string, Dict, List, Context
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

    def test_context_type_handling(self):
        type_map = AllowedTypes.get_type_map()
        assert 'Context' in type_map
        assert type_map['Context'] == Context
        
        # Test schema with Context type
        schema = Schema({'context': Context})
        assert dict(schema) == {'context': Context}

    def test_context_type_validation(self):
        """Test validation of Context type in various scenarios"""
        # Test direct Context type in schema
        simple_schema = Schema({'context': Context})
        assert dict(simple_schema) == {'context': Context}

        # Test Context in list/dict types
        list_schema = Schema({
            'contexts': List[Context]
        })
        assert list_schema['contexts'] == List[Context]

        dict_schema = Schema({
            'context_map': Dict[str, Context]
        })
        assert dict_schema['context_map'] == Dict[str, Context]

        # Verify Context is in allowed types
        assert Context in AllowedTypes.get_types()
        
        # Test type string conversion
        assert type_to_string(Context) == 'Context'

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

        # Test invalid type
        class CustomType:
            pass

        with pytest.raises(TypeError, match="Invalid type for argument 'invalid'"):
            Arguments({'invalid': CustomType()})

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
            rets=Schema({'output': int})
        )
        assert func.module == 'test_module'
        assert func.name == 'test_func'
        
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
            rets=Schema({'output': int})
        )
        serialized = func.to_dict()
        deserialized = MetaFunc.from_dict(serialized)
        assert deserialized.module == func.module
        assert deserialized.name == func.name
        assert dict(deserialized.args) == dict(func.args)
        assert dict(deserialized.rets) == dict(func.rets)

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