from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

import orjson as json
from loguru import logger
from socks import method

from pyechonext.request import Request


class Response:
	"""
	This dataclass describes a response.
	"""

	default_content_type: str = "text/html"
	default_charset: str = "UTF-8"
	unicode_errors: str = "strict"
	default_conditional_response: bool = False
	default_body_encoding: str = "UTF-8"

	def __init__(
		self,
		request: Request = None,
		use_i18n: bool = False,
		status_code: Optional[int] = 200,
		body: Optional[str] = None,
		headers: Optional[Dict[str, str]] = {},
		content_type: Optional[str] = None,
		charset: Optional[str] = None,
		i18n_params: Optional[dict] = {},
	):
		"""
		Constructs a new instance.

		:param		request:	   The request
		:type		request:	   Request
		:param		use_i18n:	   The use i 18 n
		:type		use_i18n:	   bool
		:param		status_code:   The status code
		:type		status_code:   int
		:param		body:		   The body
		:type		body:		   str
		:param		headers:	   The headers
		:type		headers:	   Dict[str, str]
		:param		content_type:  The content type
		:type		content_type:  str
		:param		charset:	   The charset
		:type		charset:	   str
		:param		kwargs:		   The keywords arguments
		:type		kwargs:		   dictionary
		"""
		if status_code == 200:
			self.status_code: str = "200 OK"
		else:
			self.status_code: str = str(status_code)

		if content_type is None:
			self.content_type: str = self.default_content_type
		else:
			self.content_type: str = content_type

		if charset is None:
			self.charset: str = self.default_charset
		else:
			self.charset: str = charset

		if body is not None:
			self.body: str = body
		else:
			self.body: str = ""

		self._headerslist: List[Any] = headers
		self._added_headers: List[Any] = []
		self.request: Request = request
		self.extra: Dict[Any, Any] = {}

		self.use_i18n: bool = use_i18n
		self.i18n_kwargs: Dict[Any, Any] = i18n_params

		self._update_headers()

	def __getattr__(self, item: Any) -> Union[Any, None]:
		"""
		Magic method for get attrs (from extra)

		:param		item:  The item
		:type		item:  Any

		:returns:	Item from self.extra or None
		:rtype:		Union[Any, None]
		"""
		return self.extra.get(item, None)

	def _structuring_headers(self, environ):
		headers = {
			"Host": environ.get("HTTP_HOST"),
			"Accept": environ.get("HTTP_ACCEPT"),
			"User-Agent": environ.get("HTTP_USER_AGENT"),
		}

		for name, value in headers.items():
			self._headerslist.append((name, value))

		for header_tuple in self._added_headers:
			self._headerslist.append(header_tuple)

	def _update_headers(self) -> None:
		"""
		Sets the headers by environ.

		:param		environ:  The environ
		:type		environ:  dict
		"""
		self._headerslist = [
			("Content-Type", f"{self.content_type}; charset={self.charset}"),
			("Content-Length", str(len(self.body))),
		]

	def add_headers(self, headers: List[Tuple[str, str]]):
		"""
		Adds new headers.

		:param		headers:  The headers
		:type		headers:  List[Tuple[str, str]]
		"""
		for header in headers:
			self._added_headers.append(header)

	def _encode_body(self):
		"""
		Encodes a body.
		"""
		if self.content_type.split("/")[-1] == "json":
			self.body = str(self.json)

		try:
			self.body = self.body.encode("UTF-8")
		except AttributeError:
			self.body = str(self.body).encode("UTF-8")

	def __call__(self, environ: dict, start_response: method) -> Iterable:
		"""
		Makes the Response object callable.

		:param		environ:		 The environ
		:type		environ:		 dict
		:param		start_response:	 The start response
		:type		start_response:	 method

		:returns:	response body
		:rtype:		Iterable
		"""
		self._encode_body()

		self._update_headers()
		self._structuring_headers(environ)

		logger.debug(
			f"[{environ.get('REQUEST_METHOD')} {self.status_code}] Run response: {self.content_type}"
		)

		start_response(status=self.status_code, headers=self._headerslist)

		return iter([self.body])

	@property
	def json(self) -> dict:
		"""
		Parse request body as JSON.

		:returns:	json body
		:rtype:		dict
		"""
		if self.body:
			if self.content_type == "application/json":
				return json.loads(self.body)
			else:
				return json.loads(json.dumps(self.body))

		return {}

	def __repr__(self):
		"""
		Returns a unambiguous string representation of the object (for debug...).

		:returns:	String representation of the object.
		:rtype:		str
		"""
		return f"<{self.__class__.__name__} at 0x{abs(id(self)):x} {self.status_code}>"
