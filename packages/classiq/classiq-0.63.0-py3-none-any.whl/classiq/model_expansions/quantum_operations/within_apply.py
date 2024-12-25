from classiq.interface.generator.functions.builtins.internal_operators import (
    WITHIN_APPLY_NAME,
)
from classiq.interface.model.within_apply_operation import WithinApply

from classiq.model_expansions.closure import Closure
from classiq.model_expansions.quantum_operations.emitter import Emitter
from classiq.model_expansions.scope import Scope


class WithinApplyEmitter(Emitter[WithinApply]):
    def emit(self, within_apply: WithinApply, /) -> None:
        within_apply_operation = Closure(
            name=WITHIN_APPLY_NAME,
            blocks=dict(within=within_apply.compute, apply=within_apply.action),
            scope=Scope(parent=self._current_scope),
        )
        context = self._expand_operation(within_apply_operation)
        self.emit_statement(
            WithinApply(
                compute=context.statements("within"),
                action=context.statements("apply"),
                source_ref=within_apply.source_ref,
            )
        )
