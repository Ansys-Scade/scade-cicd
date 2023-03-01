# ---------------------------------------------------------------------------
# mcr.py (c) ANSYS 2020
#
# patch for TestApplication
#
# ESEG - JH
# ---------------------------------------------------------------------------

import json
from enum import Enum
from lxml import etree
from typing import List
import os.path as ospath
from pathlib import Path

import scade_env
from scade.model.project.stdproject import Project
from scade.model.testenv import TestApplication
import scade.test.suite.mcoverage.dynamic as mcd

# ---------------------------------------------------------------------------
# classes
# ---------------------------------------------------------------------------

class File:
    def __init__(self, owner = None, pathname: str = None, *args, **kwargs):
        self.pathname = pathname
        self.owner = owner
        if self.pathname:
            self.load()

    def load(self) -> bool:
        pass


class InfoFile(File):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def load(self) -> bool:
        # n/a
        pass


class TraceFile(File):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def load(self) -> bool:
        # n/a
        pass


class TraceabilityFile(File):
    def __init__(self, *args, **kwargs):
        self.trace_files = []
        super().__init__(*args, **kwargs)


    def load(self) -> bool:
        try:
            f = open(self.pathname)
        except Exception as e:
            print(e)
            return False

        dir = ospath.dirname(self.pathname)
        d = json.load(f)
        for operator in d.get('operators', []):
            for mono in operator.get('monomorphic_instances', []):
                pathname = ospath.join(dir, mono.get('tra_file'))
                self.trace_files.append(TraceFile(self, pathname))

        return True


class CoverageFile(File):
    def __init__(self, *args, **kwargs):
        self.traceability_files = []
        self.info_files = []
        super().__init__(*args, **kwargs)


    def load(self) -> bool:
        try:
            tree = etree.parse(self.pathname)
        except Exception as e:
            print(e)
            return False
        dir = ospath.dirname(self.pathname)
        root = tree.getroot()
        for info in root.findall('.//InfoFile'):
            pathname = ospath.join(dir, info.get('pathname'))
            self.info_files.append(InfoFile(self, pathname))
        for trace in root.findall('.//TraceabilityFile'):
            pathname = ospath.join(dir, trace.get('pathname'))
            self.traceability_files.append(TraceabilityFile(self, pathname))

        return True


class ReportFile(File):
    def __init__(self, *args, **kwargs):
        self.report = None
        super().__init__(*args, **kwargs)


    def load(self) -> bool:
        try:
            f = open(self.pathname)
        except Exception as e:
            print(e)
            return False

        self.report = mcd.Report(json.load(f))

        return True


class MergeDir(File):
    def __init__(self, basename: str, *args, **kwargs):
        self.basename = basename
        self.traceability_file = None
        self.info_file = None
        self.report_file = None
        super().__init__(*args, **kwargs)


    def load(self) -> bool:
        # pathname is a directory
        dir = Path(self.pathname).resolve()
        self.info_file = InfoFile(self, str(dir / ('%s_coverage.info' % self.basename)))
        self.traceability_file = TraceabilityFile(self, str(dir / ('%s_traceability.json' % self.basename)))
        self.report_file = ReportFile(self, str(dir / ('%s_report.json' % self.basename)))

        return True

# ---------------------------------------------------------------------------
# new functions/properties for TestApplication
# ---------------------------------------------------------------------------

def _load_coverage_data(self: TestApplication, project: Project):
    # extension: load the coverage files
    # load the procedures referenced in the project
    for file in project.file_refs:
        path = Path(file.pathname)
        if path.suffix.lower() == '.mcr':
            self.coverage_files.append(CoverageFile(self, file.pathname))
    # search for merge results
    path = Path(project.pathname)
    merge_dir = path.parent / 'MC_Merged_Results'
    if merge_dir.exists():
        self.coverage_merge_dir = MergeDir(path.stem, self, str(merge_dir))


def _get_coverage_files(self, attribute: str) -> List[CoverageFile]:
    return self.__dict__.setdefault(attribute, [])


def _set_coverage_files(self, attribute: str, files: List[CoverageFile]):
    self.__dict__[attribute] = files


def _get_coverage_merge_dir(self, attribute: str) -> MergeDir:
    return self.__dict__.setdefault(attribute, None)


def _set_coverage_merge_dir(self, attribute: str, file: MergeDir):
    self.__dict__[attribute] = file


class _Property(object):
    "Variant from PyProperty_Type() in Objects/descrobject.c"

    def __init__(self, attribute, fget = None, fset = None, fdel = None, doc = None):
        self.attribute = attribute
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

    def __get__(self, obj, objtype = None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj, self.attribute)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, self.attribute, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj, self.attribute)


# declare new properties/functions
TestApplication.load_coverage_data = _load_coverage_data
TestApplication.coverage_files = _Property('coverage_files', _get_coverage_files, _set_coverage_files)
TestApplication.coverage_merge_dir = _Property('coverage_merge_dir', _get_coverage_merge_dir, _set_coverage_merge_dir)

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# end of file
# ---------------------------------------------------------------------------

