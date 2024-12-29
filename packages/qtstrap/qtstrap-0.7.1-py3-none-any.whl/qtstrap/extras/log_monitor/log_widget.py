from qtstrap import *
from qtpy.QtSql import *
from .log_table_view import LogTableView
from .log_filter_controls import FilterControls
from .log_database_handler import DatabaseHandler, db_conn_name


try:
    from qtstrap.extras.command_palette import CommandPalette, Command

    command_palette_available = True
except:
    command_palette_available = False


class LogMonitorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.tab_name = 'Log Monitor'

        if command_palette_available:
            self.commands = [
                Command('Log Monitor: Switch profile', triggered=self.open_profile_prompt),
            ]

        self.log_table = LogTableView()
        DatabaseHandler.register_callback(self.log_table.schedule_refresh)

        self.filter_controls = FilterControls(table=self.log_table)
        self.filter_controls.update_filter()

        self.query_existing_loggers()

        with PersistentCSplitter('log_monitor_splitter', self) as splitter:
            splitter.add(self.filter_controls, 1)
            splitter.add(self.log_table, 10)

    def open_profile_prompt(self):
        profiles = list(self.filter_controls.settings['profiles'].keys())

        self.completer = QCompleter(self, profiles)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)

        def cb(result):
            print(result)

        call_later(lambda: CommandPalette().open(placeholder='Select a profile', cb=cb, completer=self.completer))

    def query_existing_loggers(self):
        db = QSqlDatabase.database(db_conn_name)
        query = db.exec_("SELECT Source FROM 'log'")
        loggers = set()
        while query.next():
            loggers.add(query.value(0))
        self.filter_controls.logger_filter.register_loggers(loggers)


class LogMonitorDockWidget(BaseDockWidget):
    _title = 'Log Monitor'
    _starting_area = Qt.BottomDockWidgetArea
    _shortcut = 'Ctrl+`'

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWidget(LogMonitorWidget(self))

        if command_palette_available:
            self.commands = [
                Command('Log Monitor: Show log monitor', triggered=self.show),
                Command('Log Monitor: Hide log monitor', triggered=self.hide),
            ]


class LogMonitorDropdown(QWidget):
    def __init__(self, parent=None, shortcut='`'):
        super().__init__(parent=parent)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.setFocusPolicy(Qt.StrongFocus)

        self.shortcut = shortcut

        parent.installEventFilter(self)

        CHBoxLayout(self, margins=0).add(LogMonitorWidget(self))

        if command_palette_available:
            self.commands = [
                Command('Log Monitor: Show log monitor', triggered=self.show, shortcut=self.shortcut),
                Command('Log Monitor: Hide log monitor', triggered=self.hide),
            ]

        self.hide()

    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        if self.isVisible():
            if isinstance(event, QMoveEvent):
                self.center_on_parent()
            if isinstance(event, QResizeEvent):
                self.center_on_parent()

        return super().eventFilter(source, event)

    def toggleViewAction(self):
        action = QAction('Toggle Log Monitor', self)
        action.setShortcut(self.shortcut)
        action.triggered.connect(self.toggle_view)
        return action

    def toggle_view(self):
        if self.isVisible():
            self.hide()
        else:
            self.center_on_parent()
            self.show()

    def center_on_parent(self):
        offset = 33
        r = self.parent().frameGeometry()
        rect = QRect(r.x(), r.y() + offset, r.width(), r.height() - (offset * 2))
        self.setGeometry(rect)
