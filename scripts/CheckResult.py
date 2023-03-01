# ---------------------------------------------------------------------------
# CheckResult.py (c) ANSYS 2021
#
# retrieve tests results and overall status
#
# ESEG - JH
# ---------------------------------------------------------------------------

from argparse import ArgumentParser
from configparser import ConfigParser
from enum import Enum
from functools import reduce
from lxml import etree
from pathlib import Path

from scade_env import load_project
from scade.model.project.stdproject import get_roots as get_projects, Project
from scade.model.testenv import get_roots as get_test_applications
from scade.test.suite.mcoverage.utils import Status as MCStatus

import mcr

# ---------------------------------------------------------------------------
# computations
# ---------------------------------------------------------------------------

class TestResults:
    ERR_PASSED = 0
    ERR_FAILED = 1
    ERR_NO_RESULTS = 2
    ERR_LOAD_ERROR = 3

    def __init__(self, project: Project):
        self.project = project
        self.application = None
        self.procedures = {}
        for application in get_test_applications():
            if application.project == self.project:
                self.application = application
            # merge procedures from other project if any
            self.procedures.update({Path(procedure.pathname).stem: procedure for procedure in application.procedures})
        assert self.application
        self.status = self.ERR_NO_RESULTS
        self.metadatas = {}


    def dump(self, path: Path):
        pass


class TEEMETRICS(Enum):
    PASSED_TESTS = 'Number of passed tests'
    FAILED_TESTS = 'Number of failed tests'
    PASSED_PROCEDURES = 'Number of passed test procedures'
    FAILED_PROCEDURES = 'Number of failed test procedures'
    PASSED_RECORDS = 'Number of passed test records'
    FAILED_RECORDS = 'Number of failed test records'


class TestTeeResults(TestResults):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # test results, if any
        if len(self.application.result_files) == 0:
            return

        # cache for results
        app_result = (0, 0)
        file_results = {}
        record_results = {}

        # compute the status pass/failed of each procedure/record
        project_passed = 0
        project_failed = 0
        for file in self.application.result_files:
            file_passed = 0
            file_failed = 0
            file = file.raw_file
            for record in file.result_records:
                passed = len([result for result in record.results if result.status == 1])
                failed = len([result for result in record.results if result.status == 0])
                record_results[record] = (passed, failed)
                file_passed += passed
                file_failed += failed
            file_results[file] = (file_passed, file_failed)
            project_passed += file_passed
            project_failed += file_failed
        app_result = (project_passed, project_failed)

        self.metadatas[TEEMETRICS.PASSED_TESTS] = app_result[0]
        self.metadatas[TEEMETRICS.FAILED_TESTS] = app_result[1]
        self.metadatas[TEEMETRICS.PASSED_PROCEDURES] = len([file for file, status in file_results.items() if status[1] == 0])
        self.metadatas[TEEMETRICS.FAILED_PROCEDURES] = len([file for file, status in file_results.items() if status[1] != 0])
        self.metadatas[TEEMETRICS.PASSED_RECORDS] = len([record for record, status in record_results.items() if status[1] == 0])
        self.metadatas[TEEMETRICS.FAILED_RECORDS] = len([record for record, status in record_results.items() if status[1] != 0])
        failed = self.metadatas[TEEMETRICS.FAILED_TESTS]
        self.status = self.ERR_PASSED if failed == 0 else self.ERR_FAILED


    def dump(self, path: Path):
        tree = etree.ElementTree(etree.fromstring('<testsuites/>'))
        root = tree.getroot()
        root.set('disabled', '0')
        if len(self.application.result_files) == 0:
            # no result files, set the satus error for all tests
            record_count = reduce(lambda x, y: x + y, [len(procedure.records) for procedure in self.procedures.values()], 0)
            root.set('errors', str(record_count))
            root.set('tests', str(record_count))
            for id, procedure in enumerate(self.procedures.values()):
                ts = etree.SubElement(root, 'testsuite')
                ts.set('name', procedure.name)
                ts.set('id', str(id))
                for record in procedure.records:
                    tc = etree.SubElement(ts, 'testcase')
                    tc.set('name', '%s/%s' % (procedure.name, record.name))
                    tc.set('classname', procedure.operator)
                    tr = etree.SubElement(tc, 'error')
                    tr.set('message', 'test not executed')
                    tr.set('type', 'error')
                ts.set('tests', str(len(procedure.records)))
                ts.set('errors', str(len(procedure.records)))
        else:
            root.set('failures', str(self.metadatas[TEEMETRICS.FAILED_RECORDS]))
            root.set('tests', str(self.metadatas[TEEMETRICS.FAILED_RECORDS] + self.metadatas[TEEMETRICS.PASSED_RECORDS]))
    
            for id, file in enumerate(self.application.result_files):
                file_passed = 0
                file_failed = 0
                file = file.raw_file
                ts = etree.SubElement(root, 'testsuite')
                procedure_filename = Path(file.procedure_filename).stem
                procedure = self.procedures.get(procedure_filename)
                if procedure:
                    operator = procedure.operator
                    procedure_name = procedure.name
                else:
                    operator = '<unknown>'
                    procedure_name = procedure_filename
                ts.set('name', procedure_name)
                ts.set('id', str(id))
                failed = False
                for record in file.result_records:
                    tc = etree.SubElement(ts, 'testcase')
                    tc.set('name', '%s/%s' % (procedure_name, record.name))
                    tc.set('classname', operator)
                    for result in record.results:
                        if not result.status:
                            failed = True
                            tr = etree.SubElement(tc, 'failure')
                            tr.set('message', '(%d) %s: %s (expected %s)' % (result.step, result.item_path, result.actual_value, result.expected_value))
                            tr.set('type', 'value error')
                    if failed:
                        file_failed += 1
                    else:
                        file_passed += 1
                ts.set('tests', str(file_passed + file_failed))
                ts.set('failures', str(file_failed))

        tree.write(str(path), pretty_print = True)


class TestMcResults(TestResults):
    MCMETRICS = {
        MCStatus.OBSERVED: 'Observed',
        MCStatus.OBSERVED_JUSTIFIED: 'Observed justified',
        MCStatus.JUSTIFIED: 'Justified',
        MCStatus.NOT_OBSERVED: 'Not observed',
        MCStatus.NOT_COVERABLE: 'Not coverable'
    }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # extension: load the coverage files
        # load the procedures referenced in the project
        self.application.load_coverage_data(self.project)

        if self.application.coverage_merge_dir:
            report = self.application.coverage_merge_dir.report_file.report
            coverage_points = report.get_coverage_points()
            for status, metric in self.MCMETRICS.items():
                self.metadatas[metric] = coverage_points.filter_status(status).count()

            not_observed = self.metadatas[self.MCMETRICS[MCStatus.NOT_OBSERVED]]
            # self.status = self.ERR_PASSED if not_observed == 0 else self.ERR_FAILED
            # error on partial coverage disabled
            self.status = self.ERR_PASSED

            # add coverage ratios
            total = coverage_points.count()
            # round value to 2 digits
            self.metadatas['Coverage %'] = int(10000 * (total - not_observed) / total + 0.5) / 100

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    parser = ArgumentParser(description = 'SCADE Test results')
    parser.add_argument('project', metavar = '<project>', help = 'SCADE project')
    parser.add_argument('-v', '--verbose', action = 'store_true', help = 'Display the results on the standard output')
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('--tee', action = 'store_true')
    group.add_argument('--mc', action = 'store_true')
    parser.add_argument('-o', '--output', metavar = '<output>', help = 'Output result file')

    options = parser.parse_args()

    try:
        load_project(options.project)
    except:
        pass
    if len(get_projects()) == 0:
        print('failed to load project: %s' % options.project)
        exit(TestResults.ERR_LOAD_ERROR)
    else:
        test_path = get_projects()[0].get_scalar_tool_prop_def('QTE', 'TEST_PROJECT', None, None)
        if test_path:
            test_path = Path(get_projects()[0].pathname).parent / test_path
            try:
                load_project(str(test_path))
            except:
                pass
            if len(get_projects()) == 1:
                print('failed to load project: %s' % test_path)
                exit(TestResults.ERR_LOAD_ERROR)
        # main(get_projects()[0], get_sessions()[0], options)
        if options.tee:
            results = TestTeeResults(get_projects()[0])
        else:
            results = TestMcResults(get_projects()[0])

        if options.output:
            results.dump(Path(options.output))

        if options.verbose:
            for data, value in results.metadatas.items():
                print('{0} = {1}'.format(data, value))

        exit(results.status)

'''
UT options
start: .
-v "../Demos/Battery Management System/Models/SW/BMS_Result/BMS_Result.etp" --tee
-v "../Demos/Battery Management System/Models/SW/BMS_Result/BMS_Result.etp" --mc
'''

# ---------------------------------------------------------------------------
# end of file
# ---------------------------------------------------------------------------
