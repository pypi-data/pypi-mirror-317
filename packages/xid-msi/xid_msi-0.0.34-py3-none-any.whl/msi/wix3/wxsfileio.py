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
from enum import Enum
import os
import re
import uuid
from xml.dom import minidom as Minidom
from xml.dom.minidom import Document as MinidomDocument
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from ..filesystem import INode, DirectoryNode, FileNode, NodeManager
from .languagecode import LanguageCode


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
FILE_READTEXT: str = "rt"
FILE_WRITETEXT: str = "wt"
UTF8: str = "utf-8"
WIX: str = "wix"
WIX_NAMESPACE: str = "http://schemas.microsoft.com/wix/2006/wi"
EMPTY: str = ""
RE_REMOVE_NS0: str = "(ns0:|ns0|:ns0)"
LINEFEED: str = "\n"


#--------------------------------------------------------------------------------
# Windows installer XML Schema 읽고 쓰기.
#--------------------------------------------------------------------------------
class WXSFileIO:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__namespaces: dict
	__xmlFilePath: str
	__xmlElementTree: ElementTree


	#--------------------------------------------------------------------------------
	# 네임스페이스 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def Namespaces(self) -> dict:
		return self.__namespaces
	

	#--------------------------------------------------------------------------------
	# WXS XML 파일 경로 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def FilePath(self) -> dict:
		return self.__xmlFilePath
	

	#--------------------------------------------------------------------------------
	# WXS XML 트리 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def ElementTree(self) -> ElementTree:
		return self.__xmlElementTree

	#--------------------------------------------------------------------------------
	# WXS XML 루트 요소 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def RootElement(self) -> Element:
		rootElement: Element = self.ElementTree.getroot()
		return rootElement


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self) -> None:
		self.__namespaces = dict()
		self.__namespaces[WIX] = WIX_NAMESPACE
		self.__xmlFilePath = str()
		self.__xmlElementTree = None


	#--------------------------------------------------------------------------------
	# 초기화.
	#--------------------------------------------------------------------------------
	def Clear(self):
		self.__xmlFilePath = str()
		self.__xmlElementTree = None


	#--------------------------------------------------------------------------------
	# 파일을 불러왔는지 여부.
	#--------------------------------------------------------------------------------
	def IsLoaded(self) -> bool:
		if not self.FilePath or not self.ElementTree:
			return False
		return True


	#--------------------------------------------------------------------------------
	# 파일 불러오기.
	#--------------------------------------------------------------------------------
	def LoadFromFile(self, wxsFilePath: str) -> bool:
		if not wxsFilePath:
			return False
		if not os.path.isfile(wxsFilePath):
			return False
		
		self.__xmlFilePath = wxsFilePath
		self.__xmlElementTree = ElementTree.parse(self.__xmlFilePath)
		return True

	#--------------------------------------------------------------------------------
	# 파일 저장하기.
	#--------------------------------------------------------------------------------
	def SaveToFile(self, wxsFilePath: Optional[str] = None) -> bool:
		if not self.IsLoaded():
			return False

		if not wxsFilePath:
			wxsFilePath = self.__xmlFilePath

		xmlBytes: bytes = ElementTree.tostring(self.RootElement, xml_declaration = False, encoding = UTF8)
		xmlString = xmlBytes.decode(UTF8)
		xmlDocument: MinidomDocument = Minidom.parseString(xmlString)
		xmlString = xmlDocument.toprettyxml()
		xmlString = re.sub(RE_REMOVE_NS0, EMPTY, xmlString)
		xmlString = re.sub("^\t+$\n", EMPTY, xmlString, flags = re.MULTILINE)
		xmlString = re.sub("^\n", EMPTY, xmlString, flags = re.MULTILINE)
		if xmlString.endswith(LINEFEED):
			xmlString = xmlString[:-1]
		with builtins.open(wxsFilePath, mode = FILE_WRITETEXT, encoding = UTF8) as outputFile:
			outputFile.write(xmlString)
		
		# # 기본 저장.
		# self.__xmlElementTree.write(wxsFilePath, encoding = UTF8, xml_declaration = True)

		# # 다시 불러와서 정리.
		# with builtins.open(wxsFilePath, mode = FILE_READTEXT, encoding = UTF8) as inputFile:
		# 	content = inputFile.read()
		# 	content = content.replace("ns0:", "")
		# 	content = content.replace(":ns0", "")
		# 	content = content.replace(":ns0", "")
		# # 재저장.
		# with builtins.open(wxsFilePath, mode = FILE_WRITETEXT, encoding = UTF8) as outputFile:
		# 	outputFile.write(content)


	#--------------------------------------------------------------------------------
	# 찾기.
	# - 예: ComponentRef, PythonDirectoryComponent
	#--------------------------------------------------------------------------------
	def Find(self, name: str, id: str = None) -> Element:
		if not self.IsLoaded():
			return None
		elif id:
			return self.RootElement.find(f".//{WIX}:{name}[@Id='{id}']", namespaces = self.Namespaces)
		else:
			return self.RootElement.find(f".//{WIX}:{name}", namespaces = self.Namespaces)


	#--------------------------------------------------------------------------------
	# 검색.
	#--------------------------------------------------------------------------------
	def FindAll(self, name: str) -> list[Element]:
		if not self.IsLoaded():
			return list()
		else:
			wxsRootElement: Element = self.__xmlElementTree.getroot()
			return wxsRootElement.findall(f".//{WIX}:{name}", namespaces = self.__namespaces)


	#--------------------------------------------------------------------------------
	# 유효한 요소인지 여부.
	#--------------------------------------------------------------------------------
	@staticmethod
	def IsValidElement(element: Element) -> bool:
		if element == None:
			return False
		try:
			tag: str = element.tag
			return True
		except Exception as exception:
			return False

	#--------------------------------------------------------------------------------
	# 대상 요소의 자식 갯수를 반환.
	#--------------------------------------------------------------------------------	
	def GetChildCount(self, element: Element) -> int:
		if not self.IsLoaded():
			return 0
		if not WXSFileIO.IsValidElement(element):
			return 0
		children = element.findall("*")
		if not children:
			return 0
		return builtins.len(children)



#--------------------------------------------------------------------------------
# 기본 빌드 프로세스.
#--------------------------------------------------------------------------------
class BaseWIXBuildProcess:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__productCode: str
	__productVersion: str
	__productName: str
	__productManufacturer: str
	__productLanguague: LanguageCode


	#--------------------------------------------------------------------------------
	# 설치파일 코드 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def ProductCode(self) -> str:
		return self.__productCode


	#--------------------------------------------------------------------------------
	# 설치파일 코드 프로퍼티.
	#--------------------------------------------------------------------------------
	@ProductCode.setter
	def ProductCode(self, value: str) -> None:
		self.__productCode = value


	#--------------------------------------------------------------------------------
	# 설치파일 버전 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def ProductVersion(self) -> str:
		return self.__productVersion


	#--------------------------------------------------------------------------------
	# 설치파일 버전 프로퍼티.
	#--------------------------------------------------------------------------------
	@ProductVersion.setter
	def ProductVersion(self, value: str) -> None:
		self.__productVersion = value


	#--------------------------------------------------------------------------------
	# 설치파일 이름 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def ProductName(self) -> str:
		return self.__productName


	#--------------------------------------------------------------------------------
	# 설치파일 이름 프로퍼티.
	#--------------------------------------------------------------------------------
	@ProductName.setter
	def ProductName(self, value: str) -> None:
		self.__productName = value


	#--------------------------------------------------------------------------------
	# 설치파일 제조업체 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def ProductManufacturer(self) -> str:
		return self.__productManufacturer


	#--------------------------------------------------------------------------------
	# 설치파일 제조업체 프로퍼티.
	#--------------------------------------------------------------------------------
	@ProductManufacturer.setter
	def ProductManufacturer(self, value: str) -> None:
		self.__productManufacturer = value


	#--------------------------------------------------------------------------------
	# 설치파일 언어코드 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def ProductLaunguage(self) -> LanguageCode:
		return self.__productLanguague


	#--------------------------------------------------------------------------------
	# 설치파일 언어코드 프로퍼티.
	#--------------------------------------------------------------------------------
	@ProductLaunguage.setter
	def ProductLaunguage(self, value: LanguageCode) -> None:
		self.__productLanguague = value


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self) -> None:
		self.__wixNamespaces = dict()
		self.__wixNamespaces["wix"] = "http://schemas.microsoft.com/wix/2006/wi"
		self.__productCode = "{A1B2C3D4-5E6F-G7H8-IJKL-1M2N3O4P5Q6R}"
		self.__productVersion = "0.0.0"
		self.__productName = "ProductName"
		self.__productManufacturer = "ProductManufacturer"
		self.__productLanguague: LanguageCode = LanguageCode.ENGLISH