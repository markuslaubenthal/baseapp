import pytest
from multiprocessing import Process

from baseapp import BaseApp
from baseapp.registry.services import ServiceExecutor
from baseapp.registry import ExecutorState
from ..services.fixtures.MockService import MockService, mockServiceProvider
from ..services.fixtures_non_discoverable.WaitService import IndefiniteWaitService, StoppableWaitService
from click.testing import CliRunner
from unittest import mock
import os
import time

class TestServiceExecutor:
    def test_emptyrun(self):
        service = MockService
        executor = ServiceExecutor(service)
        executor_process = Process(target=executor.run)
        assert executor.getCurrentState() == ExecutorState.IDLE
        executor_process.start()
        time.sleep(0.5)
        
        assert executor.getCurrentState() == ExecutorState.RUNNING
        executor_process.join(timeout=3)
        assert executor.getCurrentState() == ExecutorState.FINISHED
                
    def test_stoppable_service(self):
        service = StoppableWaitService
        executor = ServiceExecutor(service)
        executor_process = Process(target=executor.run)
        executor_process.start()
        executor_process.join(timeout=1)
        assert executor.getCurrentState() == ExecutorState.RUNNING
        executor.stop()
        executor_process.join(timeout=2)
        assert executor.getCurrentState() == ExecutorState.STOPPED
        
    def test_non_stoppable_service_terminates_after_timeout(self):
        service = IndefiniteWaitService
        executor = ServiceExecutor(service)
        executor_process = Process(target=executor.run)
        executor_process.start()
        time.sleep(0.1)
        executor.stop()
        executor_process.join(timeout=6)
        assert executor_process.is_alive() == False
        executor_process.join()
        assert executor.getCurrentState() == ExecutorState.TERMINATED
        
    @pytest.mark.skip(reason="This test is not yet implemented")
    def test_executor_ignores_interrupt(self):
        service = MockService
        executor = ServiceExecutor(service)
        executor.ignore_interrupt = True
        assert False