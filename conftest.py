import sys
import os.path
import logging
sys.path.insert(0, os.path.dirname(__file__))
logging.basicConfig(
	level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

if os.name == 'nt':
	collect_ignore = ['quamash/_unix.py']
else:
	collect_ignore = ['quamash/_windows.py']


def pytest_addoption(parser):
	parser.addoption("--qtimpl", default='PySide')


def pytest_generate_tests(metafunc):
	if 'qtimpl' in metafunc.fixturenames:
		metafunc.parametrize('qtimpl', [metafunc.config.option.qtimpl])
