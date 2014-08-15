from ..cleaner import Cleaner


class References(Cleaner):

    full_name = "References"
    description = "Checks for references, we want a flat scene."
    fail_msg = "Found {0} references:\n{1}\nCleaning will import these refs."
    clean_msg = "Imported {0} references:\n{1}"
    pass_msg = "No references found!"

    def setup(self):
        import pymel.core as pm
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

    def clean(self):
        imported = []
        
        for ref in self.references:
            ref.importContents(removeNamespace=True)
            imported.append(ref.refNode.name())
        msg = self.clean_msg.format(
            len(imported),
            ", ".join(imported))

        self.references = []

        return True, msg


class IntermediateObjects(Cleaner):

    full_name = "Intermediate Objects"
    description = "Stranded intermediate objects (hidden shape nodes)."
    fail_msg = (
        "Found {0} intermediate objects:\n{1}\n"
        "These will be deleted upon cleaning.")
    clean_msg = "Deleted {0} intermediate objects:\n{1}"
    pass_msg = "No intermediate objects found!"

    def setup(self):
        import pymel.core as pm
        self.intermediates = []

    def check(self):
        inos = []
        nodes = pm.ls(dag=True)
        for node in nodes:
            if node.isIntermediate() and not node.listConnections():
                inos.append(node)

        if inos:
            self.intermediates = inos
            msg = self.fail_msg.format(
                len(inos), 
                ", ".join([str(ino) for ino in inos]))
            return False, msg

        return True, self.pass_msg

    def clean(self):
        deleted = []

        for intermediate in self.intermediates:
            deleted.append(str(intermediate))
            pm.delete(intermediate)
        msg = self.clean_msg.format(
            len(deleted),
            ", ".join(deleted))

        self.references = []

        return True, msg