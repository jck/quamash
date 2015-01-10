# © 2014 Mark Harviston <mark.harviston@gmail.com>
# © 2014 Arve Knudsen <arve.knudsen@gmail.com>
# BSD License
import pytest
import quamash


@pytest.fixture(params=['PySide', 'PyQt4', 'PyQt5'])
def qthread_factory(request):
	return __import__(request.param + '.QtCore', fromlist=(request.param,)).QThread


@pytest.fixture
def executor(request, qthread_factory):
	exe = quamash.QThreadExecutor(qthread_factory, 5)
	request.addfinalizer(exe.shutdown)
	return exe


@pytest.fixture
def shutdown_executor(qthread_factory):
	exe = quamash.QThreadExecutor(qthread_factory, 5)
	exe.shutdown()
	return exe


def test_shutdown_after_shutdown(shutdown_executor):
	with pytest.raises(RuntimeError):
		shutdown_executor.shutdown()


def test_ctx_after_shutdown(shutdown_executor):
	with pytest.raises(RuntimeError):
		with shutdown_executor:
			pass


def test_submit_after_shutdown(shutdown_executor):
	with pytest.raises(RuntimeError):
		shutdown_executor.submit(None)


def test_run_in_executor_without_loop(executor):
	f = executor.submit(lambda x: 2 + x, 2)
	r = f.result()
	assert r == 4


def test_run_in_executor_as_ctx_manager(qthread_factory):
	with quamash.QThreadExecutor(qthread_factory) as executor:
		f = executor.submit(lambda x: 2 + x, 2)
		r = f.result()
	assert r == 4
