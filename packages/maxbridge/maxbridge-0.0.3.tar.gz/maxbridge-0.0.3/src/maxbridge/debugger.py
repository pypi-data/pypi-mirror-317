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
from xpl import Builtins
import random
from socket import AF_INET, SOCK_STREAM
from socket import socket as Socket
import ptvsd


#--------------------------------------------------------------------------------
# 디버거.
#--------------------------------------------------------------------------------
class Debugger:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 사용 가능한 포트인지 여부.
	#--------------------------------------------------------------------------------
	@staticmethod
	def UsablePort(port: int) -> bool:
		with Socket(AF_INET, SOCK_STREAM) as socket:
			try:
				socket.bind(("localhost", port))
				return True
			except OSError:
				return False
			

	#--------------------------------------------------------------------------------
	# 실행.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Run(port: int = 5678) -> None:
		port: int = 5678
		while not Debugger.UsablePort(port):
			port = random.randint(1024, 65535)
		ptvsd.enable_attach(address = ("localhost", port))
		builtins.print(f"maxbridge.debugger started. (localhost:{port})")