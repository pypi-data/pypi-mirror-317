from qtstrap import *
from qtstrap.extras.command_palette import Command
from .actions import ActionsPage
from stagehand.components import StagehandPage
import json
import qtawesome as qta


default_page_type = 'Generic Actions'


class TabBar(QTabBar):
    def __init__(self, parent):
        super().__init__(parent)
        parent.setTabBar(self)
        self.setAcceptDrops(True)

    def get_page_from_pos(self, pos):
        tab_idx = self.tabAt(pos)
        page = self.parent().widget(tab_idx)
        return page

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        mime = event.mimeData()
        if mime.hasFormat('action_drop'):
            page = self.get_page_from_pos(event.pos())
            if hasattr(page, 'accept_action_drop'):
                event.accept()
                return

        event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        mime = event.mimeData()
        if mime.hasFormat('action_drop'):
            page = self.get_page_from_pos(event.pos())
            if hasattr(page, 'accept_action_drop'):
                event.accept()
                return

        event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        mime = event.mimeData()
        if mime.hasFormat('action_drop'):
            page = self.get_page_from_pos(event.pos())
            if hasattr(page, 'accept_action_drop'):
                data = bytes(mime.data('action_drop')).decode()
                page.accept_action_drop(json.loads(data))
                self.parent().setCurrentIndex(self.tabAt(event.pos()))
                event.accept()
                return

        event.ignore()


class MainTabWidget(QTabWidget):
    def __init__(self):
        super().__init__()

        self.setIconSize(QSize(25, 25))

        self.settings_file = OPTIONS.config_dir / 'actions.json'

        tab_bar = TabBar(self)
        tab_bar.setContextMenuPolicy(Qt.CustomContextMenu)
        tab_bar.customContextMenuRequested.connect(self.tab_context_menu)

        self.currentChanged.connect(self.save)

        more_pages_button = MenuButton('New Page')

        for c in StagehandPage.__subclasses__():
            if 'user' in c.tags:
                action = more_pages_button.addAction(c.page_type)
                action.triggered.connect(lambda _=None, p=c: self.create_page(p.page_type))

        corner = QWidget()
        with CHBoxLayout(corner, margins=(0, 0, 2, 0)) as layout:
            # layout.add(QPushButton(qta.icon('mdi.plus'), '', clicked=self.create_page))
            layout.add(more_pages_button)

        self.setCornerWidget(corner)
        self.saving_disabled = True

        self.setMovable(True)

        self.pages = []

        self.load()

        call_later(self.enable_saving, 250)

    def tab_context_menu(self, pos: QPoint):
        tab_bar = self.tabBar()
        tab_idx = tab_bar.tabAt(pos)
        page: StagehandPage = self.widget(tab_idx)

        try:
            page.tab_context_menu(self.mapToGlobal(pos), self, tab_idx)
        except NotImplementedError:
            menu = QMenu()
            menu.addAction('Rename Page').triggered.connect(lambda: self.rename_page(tab_idx))
            menu.addAction('Delete Page').triggered.connect(lambda: self.remove_page(tab_idx))
            menu.exec_(self.mapToGlobal(pos))

    def enable_saving(self):
        self.saving_disabled = False

    def fix_tab_names(self):
        [self.setTabText(i, self.widget(i).get_name()) for i in range(self.count())]

    def rename_page(self, index):
        self.setCurrentIndex(index)
        page = self.widget(index)
        page.label.start_editing()

    def remove_page(self, index):
        page = self.widget(index)
        self.pages.remove(page)
        self.removeTab(index)
        page.deleteLater()
        self.save()

    def get_unique_page_name(self):
        name = f'Page {len(self.pages) + 1}'

        # make sure the page name is unique
        page_names = [p.name for p in self.pages]
        i = 0
        while name in page_names:
            i += 1
            name = f'Page {len(self.pages) + 1 + i}'

        return name

    def create_page(self, page_type=default_page_type):
        page_class = StagehandPage.get_subclasses()[page_type]

        if 'singleton' in page_class.tags:
            name = page_class.page_type
            for p in self.pages:
                if p.page_type == page_class.page_type:
                    self.setCurrentWidget(p)
                    self.save()
                    return
        else:
            name = self.get_unique_page_name()

        new_page = page_class(name, changed=self.save, data={})
        self.add(new_page)
        self.save()

    def page_removed(self, page):
        self.pages.remove(page)
        self.save()

    def add(self, page):
        self.pages.append(page)
        idx = self.addTab(page, page.get_name())
        if hasattr(page, 'icon_name'):
            icon = qta.icon(page.icon_name)
            self.setTabIcon(idx, icon)
        self.setCurrentIndex(idx)

    def load(self):
        data = {}
        try:
            with open(self.settings_file, 'r') as f:
                data = json.loads(f.read())
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        if 'pages' in data and data['pages']:
            for name, page_data in data['pages'].items():
                page_type = page_data.get('page_type', default_page_type)
                if page_type in StagehandPage.get_subclasses():
                    page_class = StagehandPage.get_subclasses()[page_type]
                    page = page_class(name, changed=self.save, data=page_data)
                    self.add(page)
            if 'current_tab' in data:
                self.setCurrentIndex(data['current_tab'])
        else:
            default_data = {
                'actions': [
                    {
                        'name': 'Action',
                        'enabled': True,
                        'action': {
                            'type': 'sandbox',
                            'action': 'print("Hello world!")',
                        },
                        'trigger': {
                            'enabled': True,
                            'trigger_type': 'keyboard',
                            'trigger': '',
                        },
                        'filter': {
                            'enabled': True,
                            'filters': [],
                        },
                    }
                ]
            }
            self.add(ActionsPage('Page 1', changed=self.save, data=default_data))

    def save(self):
        self.fix_tab_names()

        if self.saving_disabled:
            return

        pages = [self.widget(i) for i in range(self.count())]

        data = {
            'current_tab': self.currentIndex(),
            'pages': {p.name: p.get_data() for p in pages},
        }

        with open(self.settings_file, 'w') as f:
            f.write(json.dumps(data, indent=4))
