import re
import pymel.core as pm
from cleanfreak.checker import Checker


class MayaChecker(Checker):

    def select(self):
        if self.selection:
            pm.select(self.selection)


class References(MayaChecker):

    full_name = "References"
    description = "Checks for references, we want a flat scene."
    fail_msg = "Found {0} references:\n{1}\nfixing will import these refs."
    fix_msg = "Imported {0} references:\n{1}"
    pass_msg = "No references found!"

    def check(self):
        self.selection = pm.listReferences(refNodes=False, references=True)

        if self.selection:
            names = ", ".join([ref.refNode.name() for ref in self.selection])
            msg = self.fail_msg.format(len(self.selection), names)
            return False, msg

        return True, self.pass_msg

    def fix(self):

        imported = []
        for ref in self.selection:
            ref.importContents(removeNamespace=True)
            imported.append(ref.refNode.name())

        msg = self.fix_msg.format(len(imported), ", ".join(imported))

        return True, msg


class IntermediateObjects(MayaChecker):

    full_name = "Intermediate Objects"
    description = "Stranded intermediate objects (hidden shape nodes)."
    fail_msg = (
        "Found {0} intermediate objects:\n{1}\n"
        "These will be deleted upon fixing.")
    fix_msg = "Deleted {0} intermediate objects:\n{1}"
    pass_msg = "No intermediate objects found!"

    def check(self):

        nodes = pm.ls(dag=True)
        for node in nodes:
            if node.isIntermediate() and not node.listConnections():
                self.selection.append(node)

        if self.selection:
            names = ", ".join([str(node) for node in self.selection])
            msg = self.fail_msg.format(len(self.selection), names)
            return False, msg

        return True, self.pass_msg

    def fix(self):

        deleted = []
        for intermediate in self.selection:
            deleted.append(str(intermediate))
            pm.delete(intermediate)

        msg = self.fix_msg.format(len(deleted), ", ".join(deleted))

        return True, msg


class UngroupedGeo(MayaChecker):

    full_name = "Ungrouped Geometry"
    description = "Top-level geometry, we'll have none of that."
    fail_msg = (
        "Found {0} ungrouped nodes:\n{1}\n"
        "These will be grouped together upon fixing.")
    fix_msg = "Grouped {0} nodes:\n{1}"
    pass_msg = "No ungrouped geometry found!"

    def check(self):
        nodes = [pm.listRelatives(n, parent=True) for n in pm.ls(type="mesh")]
        for node in nodes:
            if not pm.listRelatives(node, parent=True):
                self.selection.append(node)

        if self.selection:
            names = ", ".join([str(node) for node in self.selection])
            msg = self.fail_msg.format(len(self.selection), names)
            return False, msg

        return True, self.pass_msg

    def fix(self):

        pm.group(self.selection, name="GEO_GROUP_RENAME_ME")

        names = ", ".join(self.selection)
        msg = self.fix_msg.format(len(self.selection), names)

        return True, msg


class HasUVs(MayaChecker):

    full_name = "Has UVs"
    description = "Check if all meshes have UVs"
    fail_msg = (
        "Found {0} meshes without UVs:\n{1}\n"
        "These will be automatic mapped upon fixing.")
    fix_msg = "Automapped {0} meshes:\n{1}"
    pass_msg = "All your meshes have UVs. Congrats!"

    def check(self):

        nodes = [pm.listRelatives(n, parent=True) for n in pm.ls(type="mesh")]
        for node in nodes:
            num_components = pm.polyEvaluate(node, vertex=True, uvcoord=True)
            if num_components['uvcoord'] < num_components['vertex']:
                self.selection.append(node)

        if self.selection:
            names = ", ".join([str(node) for node in self.selection])
            msg = self.fail_msg.format(len(self.selection), names)
            return False, msg

        return True, self.pass_msg

    def fix(self):

        for node in self.selection:
            pm.polyAutoProjection(node)

        msg = self.fix_msg.format(len(self.selection), ", ".join(self.selection))

        return True, msg


class ExtraCameras(MayaChecker):

    full_name = "Extra Cameras"
    description = "Check for non-default cameras"
    fail_msg = (
        "Found {0} extra cameras:\n{1}\n"
        "These will be removed on fix.")
    fix_msg = "Deleted {0} cameras:\n{1}"
    pass_msg = "No extra cameras in your scene!"

    def check(self):

        default_cameras = []
        for c in ['frontShape', 'perspShape', 'sideShape', 'topShape']:
            default_cameras.append(pm.PyNode(c))

        for c in pm.ls(cameras=True):
            if not c in default_cameras:
                self.selection.append(c.getParent())

        if self.selection:
            names = ", ".join([str(c) for c in self.selection])
            msg = self.fail_msg.format(len(self.selection), names)
            return False, msg

        return True, self.pass_msg

    def fix(self):

        deleted = []
        for c in self.selection:
            deleted.append(str(c))
            pm.delete(c)

        msg = self.fix_msg.format(len(deleted), ", ".join(deleted))

        return True, msg


class DisplayLayers(MayaChecker):

    full_name = "Display Layers"
    description = "Check for display layers"
    fail_msg = (
        "Found {0} display layers:\n{1}\n"
        "These will be removed on fix.")
    fix_msg = "Deleted {0} display layers:\n{1}"
    pass_msg = "No display layers in your scene!"

    def check(self):

        default_layer = pm.PyNode('defaultLayer')
        self.selection = [l for l in pm.ls(type='displayLayer')
                               if not l == default_layer]

        if self.selection:
            msg = self.fail_msg.format(
                len(self.selection),
                ", ".join([str(c) for c in self.selection]))
            return False, msg

        return True, self.pass_msg

    def fix(self):

        deleted = []
        for c in self.selection:
            deleted.append(str(c))
            pm.delete(c)

        msg = self.fix_msg.format(len(deleted), ", ".join(deleted))

        return True, msg


class UnappliedTextures(MayaChecker):

    full_name = "Unapplied Textures"
    description = "Check for unapplied textures."
    fail_msg = (
        "Found {0} unapplied textures:\n{1}\n"
        "These will be removed on fix.")
    fix_msg = "Deleted {0} unapplied textures:\n{1}"
    pass_msg = "No unapplied textures in your scene!"

    def check(self):

        default_destinations = set([pm.PyNode('defaultTextureList1')])
        for t in pm.ls(textures=True):
            destinations = set(t.destinations()) - default_destinations
            if not destinations:
                self.selection.append(t)

        if self.selection:
            msg = self.fail_msg.format(
                len(self.selection),
                ", ".join([str(c) for c in self.selection]))
            return False, msg

        return True, self.pass_msg

    def fix(self):

        deleted = []
        for c in self.selection:
            deleted.append(str(c))
            pm.delete(c)

        msg = self.fix_msg.format(len(deleted), ", ".join(deleted))

        return True, msg


class UnappliedShaders(MayaChecker):

    full_name = "Unapplied Shaders"
    description = "Check for unapplied shaders."
    fail_msg = (
        "Found {0} unapplied shaders:\n{1}\n"
        "These will be removed on fix.")
    fix_msg = "Deleted {0} unapplied shaders:\n{1}"
    pass_msg = "No unapplied shaders in your scene!"

    def check(self):

        default_shaders = (pm.PyNode('lambert1'), pm.PyNode('particleCloud1'))
        self.selection = []
        shaders = pm.ls(materials=True)
        sgroups = [s.shadingGroups() for s in shaders]
        shaded_nodes = [[sg.dagSetMembers.inputs() for sg in sgs]
                        for sgs in sgroups]

        for shader, sgroup, nodes in zip(shaders, sgroups, shaded_nodes):
            if shader in default_shaders:
                continue
            if not any(sgroup) or not any(nodes):
                self.selection.append(shader)

        if self.selection:
            names = ", ".join([str(c) for c in self.selection])
            msg = self.fail_msg.format(len(self.selection), names)
            return False, msg

        return True, self.pass_msg

    def fix(self):

        deleted = []
        for c in self.selection:
            deleted.append(str(c))
            pm.delete(c)

        msg = self.fix_msg.format(len(deleted), ", ".join(deleted))

        return True, msg


class AppliedShaders(MayaChecker):

    full_name = "Applied Shaders"
    description = "Check for applied shaders."
    fail_msg = (
        "Found {0} applied shaders:\n{1}\n"
        "You should clean these up yourself.")
    fix_msg = "{0} applied shaders, clean these up yourself:\n{1}"
    pass_msg = "No applied shaders in your scene!"

    def check(self):

        default_shaders = (pm.PyNode('lambert1'), pm.PyNode('particleCloud1'))
        self.selection = []
        shaders = pm.ls(materials=True)
        sgroups = [s.shadingGroups() for s in shaders]
        shaded_nodes = [[sg.dagSetMembers.inputs() for sg in sgs]
                         for sgs in sgroups]

        for shader, sgroup, nodes in zip(shaders, sgroups, shaded_nodes):
            if shader in default_shaders:
                continue
            if any(nodes):
                self.selection.append(shader)

        if self.selection:
            shader_names = ", ".join([str(c) for c in self.selection])
            msg = self.fail_msg.format(len(self.selection), shader_name)
            return False, msg

        return True, self.pass_msg

    def fix(self):
        shader_names = ", ".join([str(c) for c in self.selection])
        msg = self.fix_msg.format(len(self.selection), shader_name)

        return False, msg


class CameraName(MayaChecker):

    full_name = "Camera Name"
    description = "Check for properly named camera."
    fail_msg = "No camera matches name:\n {0}\n Rename one of your cameras!"
    fix_msg = "Rename one of your cameras to: {0}"
    pass_msg = "Found a properly named camera!"

    def filepath_to_camera(self, filepath):
        vn_pattern = r'([\._]?v?\d+)$'
        basename = filepath.basename().splitext()[0]
        return re.sub(vn_pattern, '', basename).replace('anim', 'cam')

    def check(self):
        self.camera_name = self.filepath_to_camera(pm.system.sceneName())

        if not pm.objExists(self.camera_name):
            return False, self.fail_msg.format(self.camera_name)

        return True, self.pass_msg

    def fix(self):
        return self.fix_msg.format(self.camera_name)


class MeshesHaveMaterialIDs(MayaChecker):

    full_name = 'Meshes Have Material IDs'
    description = 'Make sure all mesh objects have a material ID attribute'
    fail_msg = '{0} mesh objects do not have material IDs.:\n{1}'
    fix_msg = fail_msg
    pass_msg = 'All mesh objects have material IDs.'

    def check(self):
        mesh_transforms = [m.getParent() for m in pm.ls(type='mesh')]

        for m in mesh_transforms:
            if not m.hasAttr('materialID'):
                self.selection.append(m)

        if self.selection:
            names = ", ".join([str(c) for c in self.selection])
            msg = self.fail_msg.format(len(self.selection), names)
            return False, msg

        return True, self.pass_msg

    def fix(self):
        names = ", ".join([str(c) for c in self.selection])
        msg = self.fail_msg.format(len(self.selection), names)
        return False, msg
