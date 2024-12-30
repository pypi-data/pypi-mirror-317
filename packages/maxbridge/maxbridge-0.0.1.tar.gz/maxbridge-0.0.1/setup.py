#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import IO, TextIO, BinaryIO
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
import os
import setuptools


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
UTF8: str = "utf-8"
FILE_READTEXT: str = "rt"


#--------------------------------------------------------------------------------
# 참조 메타 데이터 목록.
#--------------------------------------------------------------------------------
NAME: str = "maxbridge"
AUTHOR: str = "ddukbaek2"
AUTHOR_EMAIL: str = "ddukbaek2@gmail.com"
DESCRIPTION: str = "Autodesk 3ds Max to Python Bridge."
LONG_DESCRIPTION_CONTENT_TYPE: str = "text/markdown"
URL: str = "https://ddukbaek2.com"
PYTHON_REQUIRES: str = ">=3.9.7" # 실제로는 3.10.11 이상.
LONGDESCRIPTION: str = str()
with open(file = "README.md", mode = FILE_READTEXT, encoding = UTF8) as file: LONGDESCRIPTION = file.read()
with open(file = "VERSION", mode = FILE_READTEXT, encoding = UTF8) as file: VERSION = file.read()


#--------------------------------------------------------------------------------
# 빌드.
#--------------------------------------------------------------------------------
setuptools.setup(
	name = NAME,
	version = VERSION,
	author = AUTHOR,
	author_email = AUTHOR_EMAIL,
	description = DESCRIPTION,
	long_description = LONGDESCRIPTION,
	long_description_content_type = LONG_DESCRIPTION_CONTENT_TYPE,
	url = URL,
	packages = setuptools.find_packages(where = "src"),
	include_package_data = True,
	package_dir = { "": "src" },
	package_data = {
		"": [
			"res/*"
		],
	},
	scripts = [

	],
	entry_points = {
		"console_scripts": [
			"maxbridge=maxbridge.commandmanager:CommandManager.Run"
		]
	},
	install_requires = [
		"ptvsd",
		"xid-xpl"
	],
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: Microsoft :: Windows"
	],
	python_requires = PYTHON_REQUIRES
)