import qtawesome as qta
from qtpy.shiboken import delete, isValid

from qtstrap import *
from qtstrap.extras.style import qcolors

from .inspector import Inspector

try:
    from qtstrap.extras.command_palette import Command, CommandPalette

    command_palette_available = True
except:
    command_palette_available = False


class SceneTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent, node: 'TreeNode'):
        super().__init__(parent)

        self.node = node
        self.obj = node.obj

        obj = node.obj

        if name := obj.objectName():
            self.setForeground(0, qcolors.white)
            self.setText(0, name)
        else:
            self.setForeground(0, qcolors.gray)
            self.setText(0, f'<{type(obj).__name__}>')

        self.update_visibility_icon()

    def update_visibility_icon(self):
        if isinstance(self.obj, QWidget):
            if self.obj.isVisible():
                self.setIcon(1, qta.icon('fa5.eye'))
            else:
                self.setIcon(1, qta.icon('fa5.eye-slash'))

    def toggle_visibility(self):
        if isinstance(self.obj, QWidget):
            if self.obj.isVisible():
                self.obj.hide()
            else:
                self.obj.show()

            self.update_visibility_icon()


class TreeNode(QObject):
    inverse: dict[QObject, 'TreeNode'] = {}

    def __init__(self, obj: QObject = None, parent: QObject = None, item_parent: QObject = None):
        super().__init__(parent)
        self.obj = obj
        self._children: list[TreeNode] = []
        self.item = SceneTreeWidgetItem(item_parent, self)

        self.inverse[obj] = self

        self.obj.installEventFilter(self)
        # self.obj.destroyed.connect(self.obj_destroyed)

    def eventFilter(self, watched: QObject, event) -> bool:
        if not isValid(self.item):
            return False

        if isinstance(event, (QShowEvent, QHideEvent)):
            self.item.update_visibility_icon()

        if isinstance(event, QChildEvent):
            new_obj = event.child()
            if isinstance(new_obj, (QWidget, QLayout)):
                self.scan()

        return False

    def obj_destroyed(self, obj):
        if obj in self.inverse:
            node = self.inverse[obj]
            if isValid(node.item):
                node.item.parent().removeChild(node.item)
                delete(node.item)

            self.inverse.pop(obj)

    def scan(self):
        for child_obj in self.obj.children():
            if child_obj in self.inverse:
                continue
            if isinstance(child_obj, TreeNode):
                continue
            if isinstance(child_obj, (QWidget, QLayout)):
                node = TreeNode(obj=child_obj, parent=self, item_parent=self.item)
                self._children.append(node)
                node.scan()


class SceneTree(QTreeWidget):
    inspection_requested = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setColumnCount(2)
        self.header().hide()
        self.header().setMinimumSectionSize(1)
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(0, QHeaderView.Stretch)

        for i in range(1, 2):
            self.setColumnWidth(i, 30)

        self.itemClicked.connect(self.click)
        self.itemDoubleClicked.connect(self.double_click)
        self.itemSelectionChanged.connect(self.selection_changed)

    def click(self, item: SceneTreeWidgetItem, column: int):
        if column == 0:
            self.inspection_requested.emit(item)
        if column == 1:
            item.toggle_visibility()

    def double_click(self, item: SceneTreeWidgetItem, column: int):
        pass

    def selection_changed(self):
        pass

    def contextMenuEvent(self, event: QContextMenuEvent):
        pos = event.globalPos()
        item: SceneTreeWidgetItem = self.itemAt(self.viewport().mapFromGlobal(pos))
        menu = QMenu()

        if isinstance(item.obj, QWidget):
            if item.obj.isVisible():
                menu.addAction('Hide').triggered.connect(item.toggle_visibility)
            else:
                menu.addAction('Show').triggered.connect(item.toggle_visibility)

        menu.addAction('Open REPL')
        menu.addAction('Edit Style')

        menu.exec_(pos)

    def scan(self, obj):
        self.clear()
        self.root_node = TreeNode(obj=obj, item_parent=self)
        self.root_node.scan()
        self.root_node.item.setExpanded(True)


class SceneTreeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.tree = SceneTree()
        self.inspector = Inspector()

        self.tree.inspection_requested.connect(self.inspector.inspect)

        with PersistentCSplitter('scene_tree_splitter', self) as splitter:
            splitter.add(self.tree)
            splitter.add(self.inspector)


class SceneTreeDockWidget(BaseDockWidget):
    _title = 'Scene Tree'
    _starting_area = Qt.LeftDockWidgetArea
    _shortcut = 'Ctrl+L'

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.scene_tree = SceneTreeWidget(self)
        self.setWidget(self.scene_tree)

        if command_palette_available:
            self.commands = [
                Command('Scene Tree: Show scene tree', triggered=self.show),
                Command('Scene Tree: Hide scene tree', triggered=self.hide),
            ]

        call_later(lambda: self.scene_tree.tree.scan(self.parent()), 2000)
