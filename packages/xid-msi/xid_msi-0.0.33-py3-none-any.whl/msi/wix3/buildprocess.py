#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
import os
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from subprocess import Popen as Process
import uuid
from xml.dom import minidom
from xml.dom.minidom import Document


#--------------------------------------------------------------------------------
# 빌드 프로세스.
#--------------------------------------------------------------------------------
class BuildProcess:
	#--------------------------------------------------------------------------------
	# 시작.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Run() -> None:
		currentFilePath: str = os.path.abspath(__file__)
		rootPath: str = os.path.dirname(currentFilePath)
		resourcePath: str = os.path.join(rootPath, "res")
		sourcePath: str = os.path.join(rootPath, "src")
		packagingPath: str = os.path.join(rootPath, "packaging")
		exportersPath: str = os.path.join(packagingPath, "Babylon.js Exporters")
		startupPath: str = os.path.join(packagingPath, "Startup")
		pythonPath: str = os.path.join(packagingPath, "Python")
		mainWXSFilePath: str = os.path.join(packagingPath, "main.wxs")
		dynamicWXSFilePath: str = os.path.join(packagingPath, "dynamic.wxs")

		tree = ElementTree.parse(dynamicWXSFilePath)
		root = tree.getroot()
		namespace = {
			"wix": "http://schemas.microsoft.com/wix/2006/wi"
		}
		ElementTree.register_namespace("", namespace["wix"])
		# componentGroup = root.find(".//wix:ComponentGroup")
		for component in root.findall(".//wix:Component", namespace):
			targetID: str = component.get("Id")
			if targetID == "AssembliesDirectoryComponent":
				builtins.print("AssembliesDirectoryComponent")
				BuildProcess.ClearAllFiles(component)
				BuildProcess.AddFiles(component, exportersPath)
			elif targetID == "AltavaMaxPluginDirectoryComponent":
				builtins.print("AltavaMaxPluginDirectoryComponent")
				BuildProcess.ClearAllFiles(component)
				BuildProcess.AddFile(component, os.path.join(sourcePath, "__init__.py"))
				# BuildProcess.AddFiles(component, resourcePath)
				# BuildProcess.AddFiles(component, sourcePath)
			elif targetID == "StartupDirectoryComponent":
				builtins.print("StartupDirectoryComponent")
				BuildProcess.ClearAllFiles(component)
				BuildProcess.AddFiles(component, startupPath)
			elif targetID == "PythonDirectoryComponent":
				builtins.print("PythonDirectoryComponent")
				BuildProcess.ClearAllFiles(component)
				BuildProcess.AddFile(component, os.path.join(pythonPath, "install.bat"), "PythonPackageInstallBatchFile")
				BuildProcess.AddFile(component, os.path.join(pythonPath, "uninstall.bat"), "PythonPackageUninstallBatchFile")
				BuildProcess.AddFile(component, os.path.join(pythonPath, "requirements.txt"))
		
		xmlString: str = ElementTree.tostring(root, "utf-8")
		xmlDocument: Document = minidom.parseString(xmlString)
		xmlString = xmlDocument.toprettyxml(indent="\t")
		lines = [line for line in xmlString.splitlines() if line.strip()]
		xmlString = "\n".join(lines)
		with open(dynamicWXSFilePath, "wt", encoding="utf-8") as file:
			file.write(xmlString)


	#--------------------------------------------------------------------------------
	# 파일들 제거.
	#--------------------------------------------------------------------------------
	@staticmethod
	def ClearAllFiles(component: Element) -> None:
		for child in list(component):
			component.remove(child)


	#--------------------------------------------------------------------------------
	# 파일들을 추가.
	#--------------------------------------------------------------------------------
	@staticmethod
	def AddFile(component: Element, targetFilePath: str, uniqueID: str = None) -> Element:
		if not uniqueID:
			uniqueID = str(uuid.uuid4())
			uniqueID = uniqueID.replace("-", "")
			uniqueID = f"File_{uniqueID}"
		targetFilePath = targetFilePath.replace("\\", "/")
		targetFileName = os.path.basename(targetFilePath)
		file = Element("File")
		file.set("Id", uniqueID)
		file.set("Source", targetFilePath)
		component.append(file)
		return file


	#--------------------------------------------------------------------------------
	# 파일들을 추가.
	#--------------------------------------------------------------------------------
	@staticmethod
	def AddFiles(component: Element, startDirectory: str) -> None:
		for rootPath, _, fileNames in os.walk(startDirectory):
			for fileName in fileNames:
				filePath: str = os.path.join(rootPath, fileName)
				BuildProcess.AddFile(component, filePath)