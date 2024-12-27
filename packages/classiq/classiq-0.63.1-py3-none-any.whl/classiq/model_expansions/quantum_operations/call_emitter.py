from collections.abc import Sequence
from itertools import chain
from typing import (
    TYPE_CHECKING,
    Generic,
    Optional,
    cast,
)

from classiq.interface.debug_info.debug_info import FunctionDebugInfo
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.generated_circuit_data import OperationLevel
from classiq.interface.model.classical_parameter_declaration import (
    ClassicalParameterDeclaration,
)
from classiq.interface.model.handle_binding import HandleBinding
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_call import ArgValue, QuantumFunctionCall
from classiq.interface.model.quantum_function_declaration import (
    NamedParamsQuantumFunctionDeclaration,
    PositionalArg,
)
from classiq.interface.model.quantum_lambda_function import (
    OperandIdentifier,
    QuantumLambdaFunction,
)
from classiq.interface.model.quantum_statement import QuantumStatement
from classiq.interface.model.variable_declaration_statement import (
    VariableDeclarationStatement,
)

from classiq.model_expansions.capturing.captured_vars import (
    validate_args_are_not_propagated,
)
from classiq.model_expansions.closure import FunctionClosure, GenerativeClosure
from classiq.model_expansions.evaluators.argument_types import (
    add_information_from_output_arguments,
)
from classiq.model_expansions.evaluators.parameter_types import (
    evaluate_parameter_types_from_args,
)
from classiq.model_expansions.function_builder import (
    FunctionContext,
)
from classiq.model_expansions.quantum_operations.emitter import (
    Emitter,
    QuantumStatementT,
)
from classiq.model_expansions.scope import Evaluated, QuantumSymbol, Scope
from classiq.model_expansions.transformers.var_splitter import VarSplitter
from classiq.qmod.builtins.functions import allocate, free
from classiq.qmod.model_state_container import QMODULE

if TYPE_CHECKING:
    from classiq.model_expansions.interpreter import Interpreter


class CallEmitter(Generic[QuantumStatementT], Emitter[QuantumStatementT], VarSplitter):
    def __init__(self, interpreter: "Interpreter") -> None:
        Emitter.__init__(self, interpreter)
        VarSplitter.__init__(self, interpreter._builder.current_scope)

    @staticmethod
    def _should_wrap(body: Sequence[QuantumStatement]) -> bool:
        # This protects shadowing of captured variables (i.e, bad user code) by wrapping the body in a function
        # I'm sure there are better ways to handle it, but this is the simplest way to do it for now
        return any(isinstance(stmt, VariableDeclarationStatement) for stmt in body)

    def _create_expanded_wrapping_function(
        self, name: str, body: Sequence[QuantumStatement]
    ) -> QuantumFunctionCall:
        wrapping_function = FunctionClosure.create(
            name=self._counted_name_allocator.allocate(name),
            body=body,
            scope=Scope(parent=self._current_scope),
            is_lambda=True,
        )
        return self._create_quantum_function_call(wrapping_function, list())

    def _emit_quantum_function_call(
        self,
        function: FunctionClosure,
        args: list[ArgValue],
        propagated_debug_info: Optional[FunctionDebugInfo] = None,
    ) -> QuantumFunctionCall:
        call = self._create_quantum_function_call(
            function, args, propagated_debug_info=propagated_debug_info
        )
        self.emit_statement(call)
        return call

    def _create_quantum_function_call(
        self,
        function: FunctionClosure,
        args: list[ArgValue],
        propagated_debug_info: Optional[FunctionDebugInfo] = None,
    ) -> QuantumFunctionCall:
        function = function.clone()
        function = function.set_depth(self._builder.current_function.depth + 1)
        evaluated_args = [self._interpreter.evaluate(arg) for arg in args]
        new_declaration = self._prepare_fully_typed_declaration(
            function, evaluated_args
        )
        new_positional_arg_decls = new_declaration.positional_arg_declarations
        is_atomic = function.is_atomic
        if (
            self._interpreter._is_shallow
            and self._is_function_purely_declarative(function)
            and self._are_args_purely_declarative(args)
        ):
            is_atomic = True
            self._interpreter.add_purely_declarative_function(function)
        new_function_name = function.name
        if not is_atomic:  # perform monomorphization per interpreted parameters set
            self._add_params_to_scope(
                new_positional_arg_decls, evaluated_args, function
            )
            context = self._expand_operation(
                function.with_new_declaration(new_declaration)
            )
            function_context = cast(FunctionContext, context)
            closure_id = function_context.closure.closure_id
            function_def = self._expanded_functions.get(closure_id)
            if function_def is None:
                function_def = self._create_function_definition(function_context)
                self._expanded_functions[closure_id] = function_def
                self._top_level_scope[function_def.name] = Evaluated(
                    value=function_context.closure.with_new_declaration(function_def)
                )
                compilation_metadata = self._functions_compilation_metadata.get(
                    function.name
                )
                if compilation_metadata is not None:
                    self._expanded_functions_compilation_metadata[function_def.name] = (
                        compilation_metadata
                    )
            else:
                self._expanded_functions_compilation_metadata[
                    function_def.name
                ].occurrences_number += 1

            new_declaration = function_def
            new_function_name = function_def.name

        new_positional_args = self._get_new_positional_args(
            evaluated_args, is_atomic, new_positional_arg_decls
        )
        captured_args = function.captured_vars.get_captured_args(
            self._builder.current_function
        )
        validate_args_are_not_propagated(new_positional_args, captured_args)
        new_positional_args.extend(captured_args)
        new_call = QuantumFunctionCall(
            function=new_function_name,
            positional_args=new_positional_args,
        )
        is_allocate_or_free = (
            new_call.func_name == allocate.func_decl.name
            or new_call.func_name == free.func_decl.name
        )
        parameters = {
            arg_decl.name: FunctionDebugInfo.param_controller(value=evaluated_arg.value)
            for arg_decl, evaluated_arg in zip(new_positional_arg_decls, evaluated_args)
            if isinstance(arg_decl, ClassicalParameterDeclaration)
        }

        port_to_passed_variable_map = {
            arg_decl.name: str(evaluated_arg.value.handle)
            for arg_decl, evaluated_arg in zip(new_positional_arg_decls, evaluated_args)
            if isinstance(arg_decl, PortDeclaration)
        }
        self._debug_info[new_call.uuid] = FunctionDebugInfo(
            name=new_call.func_name,
            level=OperationLevel.QMOD_FUNCTION_CALL,
            parameters=(
                parameters
                if propagated_debug_info is None
                else propagated_debug_info.parameters
            ),
            is_allocate_or_free=is_allocate_or_free,
            port_to_passed_variable_map=port_to_passed_variable_map,
        )
        new_call.set_func_decl(new_declaration)
        return new_call

    def _create_function_definition(
        self, function_context: FunctionContext
    ) -> NativeFunctionDefinition:
        func_def = self._builder.create_definition(function_context)

        captured_ports = function_context.closure.captured_vars.get_captured_ports()
        if len(captured_ports) == 0:
            return func_def
        func_def.positional_arg_declarations = list(
            chain.from_iterable((func_def.positional_arg_declarations, captured_ports))
        )

        if not function_context.is_lambda:
            return func_def
        func_def.body = self.rewrite(
            func_def.body, function_context.closure.captured_vars.get_captured_mapping()
        )

        return func_def

    @staticmethod
    def _add_params_to_scope(
        parameters: Sequence[PositionalArg],
        arguments: Sequence[Evaluated],
        closure: FunctionClosure,
    ) -> None:
        for parameter, argument in zip(parameters, arguments):
            if isinstance(argument.value, QuantumSymbol):
                assert isinstance(parameter, PortDeclaration)
                closure.scope[parameter.name] = Evaluated(
                    QuantumSymbol(
                        handle=HandleBinding(name=parameter.name),
                        quantum_type=parameter.quantum_type,
                    ),
                    defining_function=closure,
                )
            else:
                closure.scope[parameter.name] = argument

    def _get_new_positional_args(
        self,
        evaluated_args: list[Evaluated],
        is_atomic: bool,
        new_positional_arg_decls: Sequence[PositionalArg],
    ) -> list[ArgValue]:
        evaluated_args = add_information_from_output_arguments(
            new_positional_arg_decls, evaluated_args
        )
        if is_atomic:
            return [arg.emit() for arg in evaluated_args]

        positional_args = [
            arg.emit() for arg in evaluated_args if isinstance(arg.value, QuantumSymbol)
        ]

        return positional_args

    def _prepare_fully_typed_declaration(
        self, function: FunctionClosure, evaluated_args: list[Evaluated]
    ) -> NamedParamsQuantumFunctionDeclaration:
        """
        Given, for example,
        def my_func(x: int, q: QArray["x"], p: QArray[]) -> None:
        ...
        def main(...):
            ...
            allocate(5, s)
            my_func(3, r, s)
        The code below will evaluate x to be 3, q to be of size 3 and p to be of size 5.
        Note that it requires a scope for the parameter declaration space, which is
        different from the call scope. For example, the former uses r,s and the latter
        uses p, q.
        """
        # The signature scope is passed as a separate argument to avoid contaminating the statement execution scope
        return NamedParamsQuantumFunctionDeclaration(
            name=function.name,
            positional_arg_declarations=evaluate_parameter_types_from_args(
                function,
                function.signature_scope,
                evaluated_args,
            ),
        )

    def _is_function_purely_declarative(self, function: FunctionClosure) -> bool:
        if function.name not in QMODULE.native_defs:
            return False

        if isinstance(function, GenerativeClosure):
            return False

        if any(
            not param.quantum_type.is_instantiated
            for param in function.positional_arg_declarations
            if isinstance(param, PortDeclaration)
            and param.direction == PortDeclarationDirection.Output
        ):
            return False

        dependencies = QMODULE.function_dependencies[function.name]
        return self._are_identifiers_purely_declarative(dependencies)

    def _are_args_purely_declarative(self, args: list[ArgValue]) -> bool:
        if any(
            isinstance(arg, (OperandIdentifier, QuantumLambdaFunction))
            or (
                isinstance(arg, list)
                and any(
                    isinstance(item, (OperandIdentifier, QuantumLambdaFunction))
                    for item in arg
                )
            )
            for arg in args
        ):
            return False

        dependencies = [arg for arg in args if isinstance(arg, str)]
        dependencies += [
            cast(str, item) for arg in args if isinstance(arg, list) for item in arg
        ]
        return self._are_identifiers_purely_declarative(dependencies)

    def _are_identifiers_purely_declarative(self, dependencies: list[str]) -> bool:
        return not any(
            isinstance(self._current_scope[dep].value, GenerativeClosure)
            for dep in dependencies
        )
