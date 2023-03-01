
from argparse import ArgumentParser
from pathlib import Path

from scade_env import load_project
from scade.model.project.stdproject import get_roots as get_projects, Project
import scade.model.suite as suite
from scade.model.suite import get_roots as get_sessions
from scade.model.suite.visitors import Visit


class Requirements(Visit):
    def visit_traceable(self, a, *args):
        super().visit_traceable(a, *args)
        try:
            if (a.name == "ModeController"):
                print("found HLR")
        except:
            pass
        if a.requirement_ids:
            print('%s: %s' % (a.get_full_path(), ' '.join(a.requirement_ids)))


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    parser = ArgumentParser(description = 'List HLRs in SCADE Project')
    parser.add_argument('project', metavar = '<project>', help = 'SCADE project')
    parser.add_argument('-v', '--verbose', action = 'store_true', help = 'Display the results on the standard output')
    parser.add_argument('-o', '--output', metavar = '<output>', help = 'Output result file')

    options = parser.parse_args(["c:/AnsysDev/demos/AerospaceDefense/CabinePressureControlSystem/03_Design/Software/CPCS_Software.etp"])

    try:
        load_project(options.project)
    except:
        pass
    if len(get_projects()) == 0:
        print('failed to load project: %s' % options.project)
        exit(1)
    else:
    # gather model data
        #session = get_sessions()[0]
        model = get_sessions()[0].model
        Requirements().visit(model)

        exit(0)