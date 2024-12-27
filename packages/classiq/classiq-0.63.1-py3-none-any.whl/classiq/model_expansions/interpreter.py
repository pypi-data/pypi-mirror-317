from collections import defaultdict
from collections.abc import Sequence
from contextlib import nullcontext
from functools import singledispatchmethod
from typing import Any, Optional, cast

import numpy as np
from numpy.random import permutation
from pydantic import ValidationError

from classiq.interface.exceptions import (
    ClassiqError,
    ClassiqExpansionError,
    ClassiqInternalExpansionError,
)
from classiq.interface.generator.constant import Constant
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.builtins.internal_operators import (
    CONTROL_OPERATOR_NAME,
    INVERT_OPERATOR_NAME,
    WITHIN_APPLY_NAME,
)
from classiq.interface.generator.types.compilation_metadata import CompilationMetadata
from classiq.interface.model.bind_operation import BindOperation
from classiq.interface.model.classical_if import ClassicalIf
from classiq.interface.model.control import Control
from classiq.interface.model.handle_binding import (
    FieldHandleBinding,
    HandleBinding,
    SlicedHandleBinding,
    SubscriptHandleBinding,
)
from classiq.interface.model.inplace_binary_operation import InplaceBinaryOperation
from classiq.interface.model.invert import Invert
from classiq.interface.model.model import MAIN_FUNCTION_NAME, Model
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.phase_operation import PhaseOperation
from classiq.interface.model.power import Power
from classiq.interface.model.quantum_expressions.quantum_expression import (
    QuantumAssignmentOperation,
)
from classiq.interface.model.quantum_function_call import (
    QuantumFunctionCall,
)
from classiq.interface.model.quantum_function_declaration import (
    NamedParamsQuantumFunctionDeclaration,
    QuantumFunctionDeclaration,
)
from classiq.interface.model.quantum_lambda_function import (
    OperandIdentifier,
    QuantumLambdaFunction,
)
from classiq.interface.model.quantum_statement import QuantumStatement
from classiq.interface.model.repeat import Repeat
from classiq.interface.model.variable_declaration_statement import (
    VariableDeclarationStatement,
)
from classiq.interface.model.within_apply_operation import WithinApply

from classiq.model_expansions.closure import (
    Closure,
    FunctionClosure,
    GenerativeClosure,
    GenerativeFunctionClosure,
)
from classiq.model_expansions.debug_flag import debug_mode
from classiq.model_expansions.evaluators.classical_expression import (
    evaluate_classical_expression,
)
from classiq.model_expansions.expression_renamer import ExpressionRenamer
from classiq.model_expansions.function_builder import (
    FunctionContext,
    OperationBuilder,
    OperationContext,
)
from classiq.model_expansions.generative_functions import emit_generative_statements
from classiq.model_expansions.quantum_operations import (
    BindEmitter,
    ClassicalIfEmitter,
    ControlEmitter,
    InplaceBinaryOperationEmitter,
    InvertEmitter,
    PowerEmitter,
    QuantumAssignmentOperationEmitter,
    QuantumFunctionCallEmitter,
    RepeatEmitter,
    VariableDeclarationStatementEmitter,
    WithinApplyEmitter,
)
from classiq.model_expansions.quantum_operations.phase import PhaseEmitter
from classiq.model_expansions.quantum_operations.shallow_emitter import ShallowEmitter
from classiq.model_expansions.scope import Evaluated, QuantumSymbol, Scope
from classiq.model_expansions.scope_initialization import (
    add_constants_to_scope,
    add_entry_point_params_to_scope,
    add_functions_to_scope,
    add_generative_functions_to_scope,
    get_main_renamer,
    init_top_level_scope,
)
from classiq.model_expansions.utils.counted_name_allocator import CountedNameAllocator
from classiq.qmod.builtins.functions import permute
from classiq.qmod.model_state_container import QMODULE, ModelStateContainer
from classiq.qmod.quantum_function import GenerativeQFunc
from classiq.qmod.semantics.error_manager import ErrorManager


class Interpreter:
    def __init__(
        self,
        model: Model,
        generative_functions: Optional[list[GenerativeQFunc]] = None,
        is_normalizer: bool = False,
        is_shallow: bool = False,
    ) -> None:
        self._is_normalizer = is_normalizer
        self._is_shallow = is_shallow
        self._model = model
        self._top_level_scope = Scope()
        self._counted_name_allocator = CountedNameAllocator()
        self._builder = OperationBuilder(
            self._top_level_scope, self._counted_name_allocator
        )
        self._expanded_functions: dict[str, NativeFunctionDefinition] = {}

        init_top_level_scope(model, generative_functions or [], self._top_level_scope)
        self._main_renamer: Optional[ExpressionRenamer] = (
            get_main_renamer(self._get_function_declarations())
            if self._is_normalizer
            else None
        )
        self._functions_compilation_metadata: dict[str, CompilationMetadata] = dict(
            self._model.functions_compilation_metadata
        )
        self._expanded_functions_compilation_metadata: dict[
            str, CompilationMetadata
        ] = defaultdict(CompilationMetadata)
        self._counted_name_allocator = CountedNameAllocator()
        self._error_manager: ErrorManager = ErrorManager()

    def _expand_main_func(self) -> None:
        main_func = self._top_level_scope[MAIN_FUNCTION_NAME].value
        closure_constructor: Any
        if isinstance(main_func, GenerativeFunctionClosure):
            closure_constructor = GenerativeFunctionClosure
            extra_args = {
                "generative_blocks": {"body": main_func.generative_blocks["body"]}
            }
        else:
            closure_constructor = FunctionClosure
            extra_args = {"body": main_func.body}
        main_closure = closure_constructor.create(
            name=main_func.name,
            positional_arg_declarations=main_func.positional_arg_declarations,
            scope=Scope(parent=self._top_level_scope),
            expr_renamer=self._main_renamer,
            _depth=0,
            **extra_args,
        )

        add_entry_point_params_to_scope(
            main_closure.positional_arg_declarations, main_closure
        )
        context = self._expand_operation(main_closure)
        self._expanded_functions[main_closure.closure_id] = (
            self._builder.create_definition(cast(FunctionContext, context))
        )

    def expand(self) -> Model:
        try:
            with self._error_manager.call("main"):
                self._expand_main_func()
        except Exception as e:
            if isinstance(e, ClassiqInternalExpansionError) or debug_mode.get():
                raise e
            if not isinstance(e, (ClassiqError, ValidationError)):
                raise ClassiqInternalExpansionError(str(e)) from None
            prefix = ""
            if not isinstance(e, ClassiqExpansionError):
                prefix = f"{type(e).__name__}: "
            self._error_manager.add_error(f"{prefix}{e}")
        finally:
            self._error_manager.report_errors(ClassiqExpansionError)

        return Model(
            constraints=self._model.constraints,
            preferences=self._model.preferences,
            classical_execution_code=self._model.classical_execution_code,
            execution_preferences=self._model.execution_preferences,
            functions=list(self._expanded_functions.values()),
            constants=self._model.constants,
            enums=list(QMODULE.enum_decls.values()),
            types=list(QMODULE.type_decls.values()),
            qstructs=list(QMODULE.qstruct_decls.values()),
            debug_info=self._model.debug_info,
            functions_compilation_metadata=self._expanded_functions_compilation_metadata,
        )

    @singledispatchmethod
    def evaluate(self, expression: Any) -> Evaluated:
        raise NotImplementedError(f"Cannot evaluate {expression!r}")

    @evaluate.register
    def evaluate_classical_expression(self, expression: Expression) -> Evaluated:
        return evaluate_classical_expression(expression, self._builder.current_scope)

    @evaluate.register
    def evaluate_identifier(self, identifier: str) -> Evaluated:
        return self._builder.current_scope[identifier]

    @evaluate.register
    def evaluate_lambda(self, function: QuantumLambdaFunction) -> Evaluated:
        renamed_params = [
            param.rename(function.pos_rename_params[idx])
            for idx, param in enumerate(function.func_decl.positional_arg_declarations)
        ]
        func_decl = NamedParamsQuantumFunctionDeclaration(
            name=self._counted_name_allocator.allocate(
                function.func_decl.name or "<lambda>"
            ),
            positional_arg_declarations=renamed_params,
        )

        closure_class: type[FunctionClosure]
        extra_args: dict[str, Any]
        if function.is_generative():
            closure_class = GenerativeFunctionClosure
            extra_args = {
                "generative_blocks": {
                    "body": GenerativeQFunc(function.py_callable, func_decl),
                }
            }
        else:
            closure_class = FunctionClosure
            extra_args = {}

        return Evaluated(
            value=closure_class.create(
                name=func_decl.name,
                positional_arg_declarations=func_decl.positional_arg_declarations,
                body=function.body,
                scope=Scope(parent=self._builder.current_scope),
                is_lambda=True,
                **extra_args,
            ),
            defining_function=self._builder.current_function,
        )

    @evaluate.register
    def evaluate_handle_binding(self, handle_binding: HandleBinding) -> Evaluated:
        return self.evaluate(handle_binding.name)

    @evaluate.register
    def evaluate_sliced_handle_binding(
        self, sliced_handle_binding: SlicedHandleBinding
    ) -> Evaluated:
        quantum_variable = self.evaluate(sliced_handle_binding.base_handle).as_type(
            QuantumSymbol
        )
        start = self.evaluate(sliced_handle_binding.start).as_type(int)
        end = self.evaluate(sliced_handle_binding.end).as_type(int)
        return Evaluated(value=quantum_variable[start:end])

    @evaluate.register
    def evaluate_list(self, value: list) -> Evaluated:
        return Evaluated(value=[self.evaluate(arg).value for arg in value])

    @evaluate.register
    def evaluate_subscript_handle(self, subscript: SubscriptHandleBinding) -> Evaluated:
        base_value = self.evaluate(subscript.base_handle)
        index_value = self.evaluate(subscript.index).as_type(int)
        return Evaluated(value=base_value.value[index_value])

    @evaluate.register
    def evaluate_subscript_operand(self, subscript: OperandIdentifier) -> Evaluated:
        base_value = self.evaluate(subscript.name)
        index_value = self.evaluate(subscript.index).as_type(int)
        return Evaluated(value=base_value.value[index_value])

    @evaluate.register
    def evaluate_field_access(self, field_access: FieldHandleBinding) -> Evaluated:
        base_value = self.evaluate(field_access.base_handle)
        return Evaluated(value=base_value.value.fields[field_access.field])

    @singledispatchmethod
    def emit(self, statement: QuantumStatement) -> None:
        raise NotImplementedError(f"Cannot emit {statement!r}")

    @emit.register
    def emit_quantum_function_call(self, call: QuantumFunctionCall) -> None:
        QuantumFunctionCallEmitter(self).emit(call)

    @emit.register
    def emit_bind(self, bind: BindOperation) -> None:
        BindEmitter(self).emit(bind)

    @emit.register
    def emit_quantum_assignment_operation(self, op: QuantumAssignmentOperation) -> None:
        if self._is_normalizer:
            ShallowEmitter(
                self, "assignment_operation", components=["expression", "result_var"]
            ).emit(op)
        else:
            QuantumAssignmentOperationEmitter(self).emit(op)

    @emit.register
    def emit_inplace_binary_operation(self, op: InplaceBinaryOperation) -> None:
        if self._is_normalizer:
            ShallowEmitter(
                self, "inplace_binary_operation", components=["target", "value"]
            ).emit(op)
        else:
            InplaceBinaryOperationEmitter(self).emit(op)

    @emit.register
    def emit_variable_declaration(
        self, variable_declaration: VariableDeclarationStatement
    ) -> None:
        VariableDeclarationStatementEmitter(self).emit(variable_declaration)

    @emit.register
    def emit_classical_if(self, classical_if: ClassicalIf) -> None:
        ClassicalIfEmitter(self).emit(classical_if)

    @emit.register
    def emit_within_apply(self, within_apply: WithinApply) -> None:
        if self._is_normalizer:
            ShallowEmitter(
                self,
                WITHIN_APPLY_NAME,
                components=["within", "apply", "compute", "action"],
            ).emit(within_apply)
        else:
            WithinApplyEmitter(self).emit(within_apply)

    @emit.register
    def emit_invert(self, invert: Invert) -> None:
        if self._is_normalizer:
            ShallowEmitter(self, INVERT_OPERATOR_NAME, components=["body"]).emit(invert)
        else:
            InvertEmitter(self).emit(invert)

    @emit.register
    def emit_repeat(self, repeat: Repeat) -> None:
        RepeatEmitter(self).emit(repeat)

    @emit.register
    def emit_control(self, control: Control) -> None:
        if self._is_normalizer:
            ShallowEmitter(
                self,
                CONTROL_OPERATOR_NAME,
                components=["expression", "body", "else_block"],
            ).emit(control)
        else:
            ControlEmitter(self).emit(control)

    @emit.register
    def emit_power(self, power: Power) -> None:
        if self._is_normalizer:
            ShallowEmitter(
                self, CONTROL_OPERATOR_NAME, components=["power", "body"]
            ).emit(power)
        else:
            PowerEmitter(self).emit(power)

    @emit.register
    def emit_phase(self, phase: PhaseOperation) -> None:
        if self._is_normalizer:
            ShallowEmitter(self, "phase", components=["expression", "theta"]).emit(
                phase
            )
        else:
            PhaseEmitter(self).emit(phase)

    def _expand_block(self, block: Sequence[QuantumStatement], block_name: str) -> None:
        with self._builder.block_context(block_name):
            for statement in block:
                self.emit_statement(statement)

    def emit_statement(self, statement: QuantumStatement) -> None:
        source_ref = statement.source_ref
        error_context = (
            self._error_manager.node_context(statement)
            if source_ref is not None
            else nullcontext()
        )
        with error_context, self._builder.source_ref_context(source_ref):
            self.emit(statement)

    def _expand_operation(self, operation: Closure) -> OperationContext:
        with self._builder.operation_context(operation) as context:
            if isinstance(operation, FunctionClosure) and (
                (func_def := self._expanded_functions.get(operation.closure_id))
                is not None
            ):
                captured_vars = self._top_level_scope[func_def.name].value.captured_vars
                operation.captured_vars.update(captured_vars)
            elif isinstance(operation, FunctionClosure) and operation.name == "permute":
                # special expansion since permute is generative
                self._expand_permute()
            elif isinstance(operation, GenerativeClosure):
                args = [
                    self.evaluate(param.name)
                    for param in operation.positional_arg_declarations
                ]
                emit_generative_statements(self, operation, args)
            else:
                for block, block_body in operation.blocks.items():
                    self._expand_block(block_body, block)

        return context

    def _expand_permute(self) -> None:
        functions = self.evaluate("functions").as_type(list)
        functions_permutation = permutation(np.array(range(len(functions))))
        calls: list[QuantumFunctionCall] = []
        for function_index in functions_permutation:
            permute_call = QuantumFunctionCall(
                function=OperandIdentifier(
                    name="functions", index=Expression(expr=f"{function_index}")
                )
            )
            permute_call.set_func_decl(permute.func_decl)
            calls.append(permute_call)
        self._expand_block(calls, "body")

    def _get_function_declarations(self) -> Sequence[QuantumFunctionDeclaration]:
        return [
            QuantumFunctionDeclaration(
                name=func_closure.name,
                positional_arg_declarations=func_closure.positional_arg_declarations,
            )
            for func in self._top_level_scope.values()
            if isinstance(func_closure := func.value, FunctionClosure)
        ]

    def add_constant(self, constant: Constant) -> None:
        add_constants_to_scope([constant], self._top_level_scope)

    def update_declarative_functions(
        self,
        functions: dict[str, NativeFunctionDefinition],
        qmodule: ModelStateContainer,
    ) -> None:
        add_functions_to_scope(list(functions.values()), self._top_level_scope)
        for dec_func_name in functions:
            if dec_func_name in qmodule.functions_compilation_metadata:
                self._functions_compilation_metadata[dec_func_name] = (
                    qmodule.functions_compilation_metadata[dec_func_name]
                )

    def update_generative_functions(
        self, generative_functions: dict[str, GenerativeQFunc]
    ) -> None:
        add_generative_functions_to_scope(
            list(generative_functions.values()), self._top_level_scope
        )
        for name, gen_func in generative_functions.items():
            if gen_func.compilation_metadata is not None:
                self._functions_compilation_metadata[name] = (
                    gen_func.compilation_metadata
                )

    def add_purely_declarative_function(self, function: FunctionClosure) -> None:
        functions_to_add = [function.name] + QMODULE.function_dependencies[
            function.name
        ]
        for func in functions_to_add:
            if func not in self._expanded_functions and func in QMODULE.native_defs:
                self._expanded_functions[func] = QMODULE.native_defs[func]
                if func in QMODULE.functions_compilation_metadata:
                    self._expanded_functions_compilation_metadata[func] = (
                        QMODULE.functions_compilation_metadata[func]
                    )
