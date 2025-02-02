# /********************************************************************************
# * Copyright (c) 2023 Contributors to the Eclipse Foundation
# *
# * See the NOTICE file(s) distributed with this work for additional
# * information regarding copyright ownership.
# *
# * This program and the accompanying materials are made available under the
# * terms of the Apache License 2.0 which is available at
# * http://www.apache.org/licenses/LICENSE-2.0
# *
# * SPDX-License-Identifier: Apache-2.0
# ********************************************************************************/

import logging
from typing import Any, Callable, Dict, List

from lib.action import Action, ActionContext
from lib.animator import Animator
from lib.datapoint import MockedDataPoint
from lib.trigger import Trigger, TriggerResult
from lib.types import Event, ExecutionContext

log = logging.getLogger("behavior")


class Behavior:
    """Programmable behavior of a mocked datapoint."""

    def __init__(
        self,
        trigger: Trigger,
        condition: Callable[[ExecutionContext], bool],
        action: Action,
    ):
        self._trigger = trigger
        self._condition = condition
        self._action = action

    def check_trigger(self, execution_context: ExecutionContext) -> TriggerResult:
        """Check the activation of the behavior's trigger."""
        return self._trigger.check(execution_context)

    def is_condition_fulfilled(self, execution_context: ExecutionContext) -> bool:
        """Check the condition of the behavior."""
        return self._condition(execution_context)

    def get_trigger_type(self) -> Any:
        """Return the type of the trigger."""
        return type(self._trigger)

    def execute(
        self,
        action_context: ActionContext,
        animators: List[Animator],
    ):
        """Execute the programmed action."""
        self._action.execute(action_context, animators)


class BehaviorExecutor:
    """Manager/executor for all behaviors."""

    def __init__(
        self,
        mocked_datapoints: Dict[str, MockedDataPoint],
        behaviors: Dict[str, List[Behavior]],
        pending_event_list: List[Event],
    ):
        self._mocked_datapoints = mocked_datapoints
        self._behaviors = behaviors
        self._pending_event_list = pending_event_list

    def execute(self, delta_time: float, animators):
        """Executes all behaviors in order given that their trigger has activated and their respective conditions are met."""

        for path, behaviors in self._behaviors.items():
            matched_datapoint = self._mocked_datapoints[path]
            for behavior in behaviors:
                execution_context = ExecutionContext(
                    path, self._pending_event_list, self._mocked_datapoints, delta_time
                )
                trigger_result = behavior.check_trigger(execution_context)
                if trigger_result.is_active() and behavior.is_condition_fulfilled(
                    execution_context
                ):
                    log.info(f"Running behavior for {path}")
                    behavior.execute(
                        ActionContext(
                            trigger_result, execution_context, matched_datapoint
                        ),
                        animators,
                    )
                    break
