# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from typing import List, Optional, Union
from pydantic import BaseModel

from polaris.runs.convergence.convergence_iteration import ConvergenceIteration


class IterationSchedule(BaseModel):
    first_iteration: int = 1
    """The first normal iteration at which the scheduled operation should be undertaken (i.e. start)"""

    last_iteration: int
    """Last normal iteration at which the scheduled operation can take place, note that it is not
    guaranteed to happen at this iteration unless it is specified by the start and step parameters."""

    every_x_iter: Optional[int]
    """The number of iterations between the scheduled operations (i.e. step)"""

    pattern: List[bool]
    """A recurring pattern of on/off iterations that will be repeated between the given start and end iterations"""

    on_abm_init: bool = False
    """A special case flag - should this process be run on abm_init iteration?"""

    def __init__(self, first_iteration, last_iteration, every_x_iter=None, pattern=None, **kwargs):
        if every_x_iter is not None and pattern is not None:
            raise RuntimeError("Can't have both a recurring pattern and a recurring frequency")
        if every_x_iter is None and pattern is None:
            raise RuntimeError("Must provide either a recurring pattern or a recurring frequency")

        if pattern is None:
            pattern = [1] + [0] * (every_x_iter - 1)  # 1 on, then off for the rest of the cycle

        pattern = [0] * (first_iteration - 1) + pattern * (last_iteration - first_iteration)
        pattern = pattern[:last_iteration]
        super().__init__(
            first_iteration=first_iteration,
            last_iteration=last_iteration,
            every_x_iter=every_x_iter,
            pattern=pattern,
            **kwargs,
        )

    def at_iteration(self, it: Union[int, ConvergenceIteration]):
        if isinstance(it, ConvergenceIteration):
            if it.is_abm_init and self.on_abm_init:
                return True
            if not it.is_standard:
                return False

            # It's a standard iteration, get it's number and check the schedule
            it = it.iteration_number

        # Check the overall range
        if it < self.first_iteration or it > self.last_iteration:
            return False

        # If we are in range - we can just look up the correct entry in the pattern
        return bool(self.pattern[it - 1])
