import scade
import scade.model.suite as suite
from scade.model.suite import get_roots as get_sessions
from scade.model.suite.visitors import Visit
from scade.model.testenv import get_roots as get_applications
import scade.model.testenv as test

def outputln(text):
    scade.output(text + '\n')


def report_traceability(path, reqs):
    if reqs:
        outputln('%s: %s' % (path, ' '.join(reqs)))
    # else: do not flood the output


class Requirements(Visit):
    def visit_traceable(self, a, *args):
        super().visit_traceable(a, *args)
        report_traceability(a.get_full_path(), a.requirement_ids)


def visit_test(path, e):
    new_path = path + [e.name]
    if isinstance(e, test.Traceable):
        report_traceability('/'.join(new_path), e.requirement_ids)
    if isinstance(e, test.Folder) or isinstance(e, test.Procedure):
        for sub in e. test_elements:
            visit_test(new_path, sub)


for session in get_sessions():
    # Put an action on the item
    Requirements().visit(session.model)


for app in get_applications():
    for procedure in app.procedures:
        visit_test([], procedure)
