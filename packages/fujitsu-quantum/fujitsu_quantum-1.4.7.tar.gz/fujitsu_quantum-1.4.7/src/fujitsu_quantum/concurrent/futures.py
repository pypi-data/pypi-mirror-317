# (C) 2024 Fujitsu Limited

import sys
from concurrent.futures import ProcessPoolExecutor
from typing import List, Union

if sys.version_info >= (3, 9):
    from collections.abc import Sequence
else:
    # collections.abc.Sequence is not subscriptable in Python 3.8 or older.
    # collections.abc.Sequence is deprecated since Python 3.9
    from typing import Sequence

from fujitsu_quantum.devices import QPU, Simulator
from fujitsu_quantum.results import EstimationResult, SamplingResult
from fujitsu_quantum.tasks import EstimationTask, SamplingTask


class Executor:
    """This class enables users to simultaneously submit multiple quantum tasks and retrieve results."""

    def __init__(self, max_workers: int):
        self.executor = ProcessPoolExecutor(max_workers=max_workers)

    def submit_sampling_tasks(self, device: Union[QPU, Simulator], code_list, *args, **kwargs) -> List[SamplingTask]:
        task_futures = []
        for code in code_list:
            if kwargs is None:
                kwargs = {'code': code}
            else:
                kwargs['code'] = code

            task_futures.append(self.executor.submit(device.submit_sampling_task, *args, **kwargs))

        tasks = [tf.result() for tf in task_futures]
        return tasks

    def submit_estimation_tasks(self, device: Union[QPU, Simulator], code_list, *args, **kwargs)\
            -> List[EstimationTask]:

        task_futures = []
        for code in code_list:
            if kwargs is None:
                kwargs = {'code': code}
            else:
                kwargs['code'] = code

            task_futures.append(self.executor.submit(device.submit_estimation_task, *args, **kwargs))

        tasks = [tf.result() for tf in task_futures]
        return tasks

    def get_results(self, tasks: Sequence[Union[EstimationTask, SamplingTask]])\
            -> List[Union[EstimationResult, SamplingResult]]:

        result_futures = []
        for task in tasks:
            result_futures.append(self.executor.submit(Executor._get_task_result, task))

        results = [rf.result() for rf in result_futures]
        return results

    @staticmethod
    def _get_task_result(task: Union[EstimationTask, SamplingTask]) -> Union[EstimationResult, SamplingResult]:
        return task.result()
