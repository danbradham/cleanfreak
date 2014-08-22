import pymel.core as pm
from ..checker import Checker


class References(Checker):

    full_name = "References"
    description = "Checks for references, we want a flat scene."
    fail_msg = "Found {0} references:\n{1}\nfixing will import these refs."
    fix_msg = "Imported {0} references:\n{1}"
    pass_msg = "No references found!"

    def setup(self):
        self.references = []

    def check(self):
        refs = pm.listReferences(refNodes=False, references=True)

        if refs:
            self.references = refs
            msg = self.fail_msg.format(
                len(refs),
                ", ".join([ref.refNode.name() for ref in refs]))
            return False, msg

        return True, self.pass_msg

    def fix(self):
        imported = []

        for ref in self.references:
            ref.importContents(removeNamespace=True)
            imported.append(ref.refNode.name())
        msg = self.fix_msg.format(
            len(imported),
            ", ".join(imported))

        self.references = []

        return True, msg


class IntermediateObjects(Checker):

    full_name = "Intermediate Objects"
    description = "Stranded intermediate objects (hidden shape nodes)."
    fail_msg = (
        "Found {0} intermediate objects:\n{1}\n"
        "These will be deleted upon fixing.")
    fix_msg = "Deleted {0} intermediate objects:\n{1}"
    pass_msg = "No intermediate objects found!"

    def setup(self):
        self.intermediates = []

    def check(self):
        self.intermediates = []
        nodes = pm.ls(dag=True)
        for node in nodes:
            if node.isIntermediate() and not node.listConnections():
                self.intermediates.append(node)

        if self.intermediates:
            msg = self.fail_msg.format(
                len(self.intermediates),
                ", ".join([str(node) for node in self.intermediates]))
            return False, msg

        return True, self.pass_msg

    def fix(self):
        deleted = []

        for intermediate in self.intermediates:
            deleted.append(str(intermediate))
            pm.delete(intermediate)
        msg = self.fix_msg.format(
            len(deleted),
            ", ".join(deleted))

        self.references = []

        return True, msg


class UngroupedGeo(Checker):

    full_name = "Ungrouped Geometry"
    description = "Top-level geometry, we'll have none of that."
    fail_msg = (
        "Found {0} ungrouped nodes:\n{1}\n"
        "These will be grouped together upon fixing.")
    fix_msg = "Grouped {0} nodes:\n{1}"
    pass_msg = "No ungrouped geometry found!"

    def setup(self):
        self.ungrouped = []

    def check(self):
        nodes = pm.ls(dag=True)
        for node in nodes:
            if node.isIntermediate() and not node.listConnections():
                self.ungrouped.append(node)

        if self.ungrouped:
            msg = self.fail_msg.format(
                len(self.ungrouped),
                ", ".join([str(node) for node in self.ungrouped]))
            return False, msg

        return True, self.pass_msg

    def fix(self):
        pm.group(self.ungrouped)
        msg = self.fix_msg.format(
            len(self.ungrouped),
            ", ".join(self.ungrouped))

        self.ungrouped = []

        return True, msg
