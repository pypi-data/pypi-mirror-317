from qtstrap import *
import qtawesome as qta
from qtstrap.extras.style import colors
import json


LOG_FILTER_COLORS = {
    'dark': {
        'D': colors.aqua,  # DEBUG
        'I': colors.green,  # INFO
        'W': colors.orange,  # WARNING
        'E': colors.red,  # ERROR
        'C': colors.fuchsia,  # CRITICAL
        'off': colors.gray,
        'enabled': colors.gray,
        'disabled': colors.silver,
    },
    'light': {
        'D': colors.blue,  # DEBUG
        'I': colors.green,  # INFO
        'W': colors.orange,  # WARNING
        'E': colors.red,  # ERROR
        'C': colors.fuchsia,  # CRITICAL
        'off': colors.black,
        'enabled': colors.black,
        'disabled': colors.gray,
    },
}


def get_color(key):
    return LOG_FILTER_COLORS[OPTIONS.theme][key]


class LoggerDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        self.initStyleOption(option, index)
        text = index.data(Qt.DisplayRole)
        checked = index.data(Qt.UserRole)

        if text is None:
            return

        painter.save()

        if len(text) == 1:
            if option.state & QStyle.State_Selected and checked:
                painter.setPen(QPen(get_color(text)))
            else:
                painter.setPen(QPen(get_color('off')))
            painter.drawText(option.rect, Qt.AlignCenter, text)
        else:
            if option.state & QStyle.State_Selected:
                painter.setPen(QPen(get_color('enabled')))
            else:
                painter.setPen(QPen(get_color('disabled')))
            painter.drawText(option.rect, Qt.AlignLeft, text)

        painter.restore()


class LoggerTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent, name, full_name):
        super().__init__(parent)

        self.setText(0, name)
        self.name = name
        self.full_name = full_name

        self.levels = {
            'DEBUG': True,
            'INFO': True,
            'WARNING': True,
            'ERROR': True,
            'CRITICAL': True,
        }

        self.update_data()
        self.selected = False

    def clicked(self, column):
        if column == 0:
            if self.full_name != 'global':
                self.setSelected(not self.isSelected())
            else:
                self.selected = not self.selected
        else:
            if self.data(column, Qt.UserRole):
                self.setData(column, Qt.UserRole, False)
                self.levels[self.text(column)] = False
            else:
                self.setData(column, Qt.UserRole, True)
                self.levels[self.text(column)] = True

    def double_clicked(self, column):
        def select_children(item, state):
            item.setSelected(state)
            for i in range(item.childCount()):
                select_children(item.child(i), state)

        if column == 0:
            if self.full_name != 'global':
                state = self.isSelected()
            else:
                state = self.selected

            for i in range(self.childCount()):
                select_children(self.child(i), state)

    def update_data(self):
        for i, level in enumerate(self.levels):
            self.setData(i + 1, Qt.UserRole, self.levels[level])
            self.setText(i + 1, level[:1])
            self.setTextAlignment(i + 1, Qt.AlignCenter)

    def set_levels(self, level_filter=[]):
        for level in level_filter:
            if level in self.levels:
                self.levels[level] = True

        self.update_data()

    def get_levels(self):
        return [level for level in self.levels if self.levels[level]]

    def set_all_levels(self, state: bool):
        for level in self.levels:
            self.levels[level] = state
        self.update_data()


class LoggerTreeWidget(QTreeWidget):
    filter_updated = Signal()

    def __init__(self):
        super().__init__()

        self.setItemDelegate(LoggerDelegate())
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setRootIsDecorated(False)
        self.setIndentation(10)
        self.setStyleSheet('QTreeView::branch { border-image: url(none.png); }')
        self.setUniformRowHeights(True)
        self.setExpandsOnDoubleClick(False)
        self.setItemsExpandable(False)
        self.setFocusPolicy(Qt.NoFocus)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.header().setMinimumSectionSize(1)
        self.header().hide()
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(0, QHeaderView.Stretch)

        self.setColumnCount(7)
        for i in range(1, 7):
            self.setColumnWidth(i, 15)

        self.loggers = {}
        self.visible_loggers = []

        self.itemClicked.connect(self.click)
        self.itemDoubleClicked.connect(self.double_click)
        self.itemSelectionChanged.connect(self.selection_changed)

        self.root = LoggerTreeWidgetItem(self, 'global', 'global')
        self.loggers['global'] = self.root
        self.root.setSelected(True)

    def click(self, item, column):
        item.clicked(column)
        self.selection_changed()

    def double_click(self, item, column):
        item.double_clicked(column)
        self.selection_changed()

    def selection_changed(self):
        self.visible_loggers = [item.full_name for item in self.selectedItems()]
        self.filter_updated.emit()

    def register_logger(self, full_name):
        if full_name in self.loggers:
            return
        else:
            parts = full_name.rsplit('.', 1)  # split off the last name only
            name = parts[-1]

            if len(parts) == 1:
                parent = self.root
            else:
                if parts[0] not in self.loggers:
                    self.register_logger(parts[0])
                parent = self.loggers[parts[0]]

            self.loggers[full_name] = LoggerTreeWidgetItem(parent, name, full_name)
            self.loggers[full_name].setSelected(True)

        self.expandAll()
        self.selection_changed()

    def register_loggers(self, loggers):
        for name in loggers:
            self.register_logger(name)

    def contextMenuEvent(self, event):
        menu = QMenu()
        pos = event.globalPos()
        menu.addAction(QAction('Select Only', menu, triggered=lambda: self.select_only(pos)))
        menu.addAction(QAction('Select All', menu, triggered=self.select_all))
        menu.addAction(QAction('Deselect All', menu, triggered=self.deselect_all))
        menu.addAction(QAction('All Levels', menu, triggered=lambda: self.enable_all_levels(pos)))
        menu.addAction(QAction('No Levels', menu, triggered=lambda: self.disable_all_levels(pos)))
        menu.addAction(QAction('Enable Everything', menu, triggered=self.enable_everything))
        menu.addAction(QAction('Disable Everything', menu, triggered=self.disable_everything))
        menu.exec_(event.globalPos())

    def set_levels_of_children(self, item, state):
        if hasattr(item, 'set_all_levels'):
            item.set_all_levels(state)
        for i in range(item.childCount()):
            self.set_levels_of_children(item.child(i), state)

    def enable_everything(self):
        self.select_all()
        self.set_levels_of_children(self.invisibleRootItem(), True)

    def disable_everything(self):
        self.deselect_all()
        self.set_levels_of_children(self.invisibleRootItem(), False)

    def enable_all_levels(self, pos):
        self.itemAt(self.viewport().mapFromGlobal(pos)).set_all_levels(True)
        self.selection_changed()

    def disable_all_levels(self, pos):
        self.itemAt(self.viewport().mapFromGlobal(pos)).set_all_levels(False)
        self.selection_changed()

    def set_visible_loggers(self, visible_loggers):
        def set_visible(item):
            if hasattr(item, 'full_name'):
                if item.full_name in visible_loggers:
                    item.setSelected(True)
                else:
                    item.setSelected(False)

            for i in range(item.childCount()):
                set_visible(item.child(i))

        set_visible(self.invisibleRootItem())

    def select_all(self):
        def select_children(item):
            item.setSelected(True)
            for i in range(item.childCount()):
                select_children(item.child(i))

        select_children(self.invisibleRootItem())

    def deselect_all(self):
        self.clearSelection()
        self.root.setSelected(True)

    def select_only(self, pos):
        self.deselect_all()
        self.itemAt(self.viewport().mapFromGlobal(pos)).setSelected(True)
        self.selection_changed()


class ProfileSelector(QWidget):
    added = Signal(str)
    removed = Signal(str)
    changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.setStyleSheet('QPushButton { max-width: 20px; }')

        self.selector = QComboBox()
        self.editor = QLineEdit()
        self.editor.setPlaceholderText('Profile name')

        self.menu_btn = MenuButton()

        self.menu_btn.addAction('New Profile').triggered.connect(self.on_add)
        self.menu_btn.addAction('Delete Profile').triggered.connect(self.on_remove)

        self.selector.currentIndexChanged.connect(self.on_change)

        self.editor.installEventFilter(self)
        self.editor.hide()

        with CGridLayout(self, margins=0, spacing=2) as layout:
            layout.add(self.selector, 0, 0, 1, 3)
            layout.add(self.editor, 0, 0, 1, 3)
            layout.add(self.menu_btn, 0, 4)

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return:
                self.on_accept()
                return True

            if event.key() == QtCore.Qt.Key_Escape:
                self.on_cancel()
                event.accept()
                return True

        return False

    def on_change(self):
        name = self.selector.currentText()
        self.changed.emit(name)

    def on_add(self):
        self.selector.hide()
        self.editor.show()
        self.editor.setFocus()

    def on_accept(self):
        self.selector.show()
        self.editor.hide()

        name = self.editor.text()
        if len(name) > 0:
            self.added.emit(name)
        self.editor.clear()

    def on_cancel(self):
        self.selector.show()
        self.editor.hide()
        self.editor.clear()

    def on_remove(self):
        name = self.selector.currentText()
        self.removed.emit(name)


class FilterControls(QWidget):
    empty_profile = {
        'loggers': {
            'global': [
                'DEBUG',
                'INFO',
                'WARNING',
                'ERROR',
                'CRITICAL',
            ],
        },
        'visible_loggers': [
            'global',
        ],
        'text': '',
        'current_session_only': True,
        'query_limit': 1000,
    }

    default_settings = {
        'selected_profile': 'default',
        'registered_loggers': ['global'],
        'profiles': {'default': empty_profile},
    }

    def __init__(self, table):
        super().__init__()

        self.setStyleSheet(
            """
            QTreeWidget {
                selection-background-color: transparent;
                selection-color: lightgray; 
                color: gray;
            }
        """
        )
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.settings_file = OPTIONS.config_dir / 'log_profiles.json'

        self.table = table
        self.table.columns_changed.connect(self.columns_changed)

        # create widgets
        self.profiles = ProfileSelector()

        self.text_filter = QLineEdit()
        self.text_filter.textChanged.connect(self.update_filter)
        self.text_filter.setClearButtonEnabled(True)
        self.text_filter.setPlaceholderText('filter by text')

        self.logger_filter = LoggerTreeWidget()
        self.session_checkbox = QCheckBox()
        self.query_limit = QLineEdit()
        self.query_limit.setValidator(QIntValidator())

        # load settings and send filter components to widgets
        prev = json.dumps(self.default_settings)
        try:
            with open(self.settings_file, 'r') as f:
                prev = f.read()
        except:
            pass

        self.settings = json.loads(prev)

        profiles = self.settings['profiles']
        current_profile_name = self.settings['selected_profile']
        if current_profile_name not in profiles:
            current_profile_name = list(profiles.keys())[0]
        self.current_profile = profiles[current_profile_name]

        self.logger_filter.register_loggers(self.settings['registered_loggers'])
        self.profiles.selector.addItems(profiles)

        for logger in self.current_profile['loggers']:
            self.logger_filter.register_logger(logger)

        self.logger_filter.set_visible_loggers(self.current_profile['visible_loggers'])
        self.session_checkbox.setChecked(self.current_profile['current_session_only'])
        self.query_limit.setText(str(self.current_profile['query_limit']))
        self.table.set_columns(self.current_profile.get('column_data', {}))

        # connect signals
        self.logger_filter.filter_updated.connect(self.update_filter)
        self.profiles.selector.setCurrentIndex(self.profiles.selector.findText(current_profile_name))
        self.profiles.changed.connect(self.change_profile)
        self.profiles.added.connect(self.add_profile)
        self.profiles.removed.connect(self.remove_profile)
        self.session_checkbox.stateChanged.connect(self.update_filter)
        self.query_limit.textChanged.connect(self.update_filter)

        # send the filter to the model
        self.update_filter()

        # controls layout
        with CVBoxLayout(self, margins=0) as layout:
            layout.add(self.profiles)
            with layout.hbox() as layout:
                layout.add(QLabel('Current Session:'))
                layout.add(self.session_checkbox)
                layout.add(QLabel(), 1)
            with layout.hbox() as layout:
                layout.add(QLabel('Query Limit:'))
                layout.add(self.query_limit)
                layout.add(QLabel(), 1)
            layout.add(self.text_filter)
            layout.add(self.logger_filter)

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            f.write(json.dumps(self.settings, indent=4))

    def add_profile(self, name):
        new_profile = dict(self.empty_profile)
        self.settings['profiles'][name] = new_profile
        self.profiles.selector.addItem(name)
        self.profiles.selector.setCurrentIndex(self.profiles.selector.findText(name))

    def remove_profile(self, name):
        index = self.profiles.selector.findText(name)
        self.profiles.selector.removeItem(index)

        self.settings['profiles'].pop(name)
        self.save_settings()

    def change_profile(self, profile_name):
        self.settings['selected_profile'] = profile_name

        self.current_profile = self.settings['profiles'][profile_name]
        self.logger_filter.set_visible_loggers(self.current_profile['visible_loggers'])
        self.table.set_columns(self.current_profile.get('column_data', {}))
        self.update_filter()

    def columns_changed(self):
        self.current_profile['column_data'] = self.table.profile.column_data
        self.table.set_columns(self.current_profile.get('column_data', {}))
        self.save_settings()

    def update_filter(self):
        text = self.text_filter.text()
        loggers = {item.full_name: item.get_levels() for _, item in self.logger_filter.loggers.items()}
        visible_loggers = self.logger_filter.visible_loggers

        self.settings['registered_loggers'] = list(self.logger_filter.loggers.keys())
        self.current_profile['text'] = text
        self.current_profile['loggers'] = loggers
        self.current_profile['visible_loggers'] = visible_loggers
        self.current_profile['current_session_only'] = self.session_checkbox.isChecked()
        self.current_profile['query_limit'] = int(self.query_limit.text())

        self.table.set_filter(self.current_profile)
        self.save_settings()
