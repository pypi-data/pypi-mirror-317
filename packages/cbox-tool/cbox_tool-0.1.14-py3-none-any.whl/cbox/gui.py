import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
    QMessageBox, QFileDialog, QTabWidget, QListWidget, QListWidgetItem,
    QSplitter, QFrame, QHeaderView, QInputDialog, QDialog, QFormLayout,
    QMenu, QToolBar, QStyle, QComboBox, QTextEdit, QMenuBar
)
from PySide6.QtCore import Qt, QSize, Signal, QTimer
from PySide6.QtGui import QIcon, QFont, QColor, QBrush, QAction, QCursor

from .mybox import CBox
from .i18n import tr

class StyledButton(QPushButton):
    def __init__(self, text_key, icon=None, parent=None, primary=False):
        super().__init__(tr(text_key), parent)
        self.setProperty("text_key", text_key)  # 存储文本键以便后续翻译
        if icon:
            self.setIcon(icon)
        
        color = "#0d6efd" if primary else "#f8f9fa"
        hover_color = "#0b5ed7" if primary else "#e9ecef"
        text_color = "white" if primary else "#495057"
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border: 1px solid {color};
                border-radius: 4px;
                padding: 6px 12px;
                color: {text_color};
                min-width: 80px;
                font-weight: {"bold" if primary else "normal"};
            }}
            QPushButton:hover {{
                background-color: {hover_color};
                border-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {"#0a58ca" if primary else "#dee2e6"};
            }}
            QPushButton:disabled {{
                background-color: #e9ecef;
                color: #adb5bd;
            }}
        """)

    def retranslate_ui(self):
        self.setText(tr(self.property("text_key")))

class CommitDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(tr("commit_changes"))
        self.setMinimumWidth(500)
        layout = QVBoxLayout(self)

        # 提交信息输入框
        self.message_edit = QTextEdit()
        self.message_edit.setPlaceholderText(tr("input_commit_message"))
        self.message_edit.setMinimumHeight(100)
        layout.addWidget(self.message_edit)

        # 按钮
        button_layout = QHBoxLayout()
        commit_button = StyledButton("commit", primary=True)
        commit_button.setProperty("text_key", "commit")
        cancel_button = StyledButton("cancel")
        cancel_button.setProperty("text_key", "cancel")
        commit_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(commit_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

    def get_message(self):
        return self.message_edit.toPlainText().strip()

    def retranslate_ui(self):
        self.setWindowTitle(tr("commit_changes"))
        self.message_edit.setPlaceholderText(tr("input_commit_message"))
        for button in self.findChildren(StyledButton):
            if button.property("text_key"):
                button.setText(tr(button.property("text_key")))

class AddWorkspaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(tr("add_workspace"))
        self.setMinimumWidth(400)
        layout = QFormLayout(self)

        # 工作空间名称
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(tr("input_workspace_name"))
        layout.addRow(tr("workspace_name"), self.name_input)

        # 工作空间路径
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText(tr("select_workspace_path"))
        browse_button = StyledButton("browse")
        browse_button.setProperty("text_key", "browse")
        browse_button.clicked.connect(self.browse_path)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_button)
        layout.addRow(tr("workspace_path"), path_layout)

        # 按钮
        button_layout = QHBoxLayout()
        ok_button = StyledButton("confirm", primary=True)
        ok_button.setProperty("text_key", "confirm")
        cancel_button = StyledButton("cancel")
        cancel_button.setProperty("text_key", "cancel")
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addRow("", button_layout)

    def browse_path(self):
        path = QFileDialog.getExistingDirectory(self, tr("select_workspace_directory"))
        if path:
            self.path_input.setText(path)

    def get_data(self):
        return {
            "name": self.name_input.text(),
            "path": self.path_input.text()
        }

    def retranslate_ui(self):
        self.setWindowTitle(tr("add_workspace"))
        self.name_input.setPlaceholderText(tr("input_workspace_name"))
        self.path_input.setPlaceholderText(tr("select_workspace_path"))
        
        # 更新表单标签
        for i in range(self.layout().rowCount()):
            label = self.layout().itemAt(i, QFormLayout.LabelRole)
            if label and label.widget():
                if "workspace_name" in label.widget().text():
                    label.widget().setText(tr("workspace_name"))
                elif "workspace_path" in label.widget().text():
                    label.widget().setText(tr("workspace_path"))

        # 更新按钮文本
        for button in self.findChildren(StyledButton):
            if button.property("text_key"):
                button.setText(tr(button.property("text_key")))

class BranchDialog(QDialog):
    def __init__(self, parent=None, mode="create"):
        super().__init__(parent)
        self.mode = mode
        self.branches = []
        self.setup_ui()

    def setup_ui(self):
        self.setMinimumWidth(400)
        layout = QFormLayout(self)

        if self.mode == "create":
            self.setWindowTitle(tr("create_branch"))
            # 分支名称输入
            self.branch_input = QLineEdit()
            self.branch_input.setPlaceholderText(tr("input_branch_name"))
            layout.addRow(tr("branch_name"), self.branch_input)

            # 起始点选择（可选）
            self.start_point = QLineEdit()
            self.start_point.setPlaceholderText(tr("optional_start_point"))
            layout.addRow(tr("start_point"), self.start_point)
        else:
            if self.mode == "switch":
                self.setWindowTitle(tr("switch_branch"))
            else:
                self.setWindowTitle(tr("merge_branch"))
            self.branch_input = QLineEdit()
            self.branch_input.setPlaceholderText(tr("input_branch_name"))
            layout.addRow(tr("branch_name"), self.branch_input)
            # # 分支选择下拉框
            # self.branch_combo = QComboBox()
            # self.branch_combo.setStyleSheet("""
            #     QComboBox {
            #         border: 1px solid #dee2e6;
            #         border-radius: 4px;
            #         padding: 6px 12px;
            #         background-color: white;
            #     }
            #     QComboBox::drop-down {
            #         border: none;
            #     }
            #     QComboBox::down-arrow {
            #         image: url(down_arrow.png);
            #         width: 12px;
            #         height: 12px;
            #     }
            # """)
            # layout.addRow(tr("select_branch"), self.branch_combo)

        # 按钮
        button_layout = QHBoxLayout()
        ok_button = StyledButton("confirm", primary=True)
        ok_button.setProperty("text_key", "confirm")
        cancel_button = StyledButton("cancel")
        cancel_button.setProperty("text_key", "cancel")
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addRow("", button_layout)

    def set_branches(self, branches):
        self.branches = branches
        if self.mode != "create":
            self.branch_combo.clear()
            self.branch_combo.addItems(branches)

    def get_data(self):
        if self.mode == "create":
            return {
                "name": self.branch_input.text(),
                "start_point": self.start_point.text() or None
            }
        else:
            return {
                "name": self.branch_input.text()
            }

    def retranslate_ui(self):
        if self.mode == "create":
            self.setWindowTitle(tr("create_branch"))
            self.branch_input.setPlaceholderText(tr("input_branch_name"))
            self.start_point.setPlaceholderText(tr("optional_start_point"))
            # 更新表单标签
            for i in range(self.layout().rowCount()):
                label = self.layout().itemAt(i, QFormLayout.LabelRole)
                if label and label.widget():
                    if "branch_name" in label.widget().text():
                        label.widget().setText(tr("branch_name"))
                    elif "start_point" in label.widget().text():
                        label.widget().setText(tr("start_point"))
        else:
            self.setWindowTitle(tr("switch_branch"))
            # 更新表单标签
            for i in range(self.layout().rowCount()):
                label = self.layout().itemAt(i, QFormLayout.LabelRole)
                if label and label.widget():
                    if "select_branch" in label.widget().text():
                        label.widget().setText(tr("select_branch"))

        # 更新按钮文本
        for button in self.findChildren(StyledButton):
            if button.property("text_key"):
                button.setText(tr(button.property("text_key")))

class WorkspaceListItem(QListWidgetItem):
    def __init__(self, name, path, changes_count=0):
        super().__init__()
        self.name = name
        self.path = path
        self.changes_count = changes_count
        self.update_text()
        self.setToolTip(f"{tr('path')}: {path}")
        
    def update_text(self):
        text = self.name
        if self.changes_count > 0:
            text += f" ({self.changes_count})"
        self.setText(text)

    def update_changes_count(self, count):
        self.changes_count = count
        self.update_text()

class WorkspacePanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        # 标题和按钮
        header_layout = QHBoxLayout()
        title = QLabel(tr("workspace"))
        title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #212529;
            }
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()

        # 添加按钮
        add_button = StyledButton("add")
        add_button.setProperty("text_key", "add")
        add_button.clicked.connect(self.add_workspace)
        header_layout.addWidget(add_button)

        # 移除按钮
        remove_button = StyledButton("remove")
        remove_button.setProperty("text_key", "remove")
        remove_button.clicked.connect(self.main_window.remove_workspace)
        header_layout.addWidget(remove_button)

        layout.addLayout(header_layout)

        # 工作空间列表
        self.workspace_list = QListWidget()
        self.workspace_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background-color: white;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #dee2e6;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QListWidget::item:hover {
                background-color: #f8f9fa;
            }
        """)
        layout.addWidget(self.workspace_list)

    def add_workspace(self):
        dialog = AddWorkspaceDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            try:
                self.main_window.cbox.add_workspace(data["name"], data["path"])
                self.main_window.refresh_workspaces_list()
            except Exception as e:
                QMessageBox.warning(self, tr("error"), str(e))

    def retranslate_ui(self):
        # 更新标题
        title = self.findChild(QLabel)
        if title:
            title.setText(tr("workspace"))
        
        # 更新按钮文本
        for button in self.findChildren(StyledButton):
            if button.property("text_key"):
                button.setText(tr(button.property("text_key")))

class RepositoryPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        # 标题和按钮
        header_layout = QHBoxLayout()
        title = QLabel(tr("repo_name"))
        title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #212529;
            }
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()

        # 按钮组
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # 克隆按钮
        clone_button = StyledButton("clone")
        clone_button.setProperty("text_key", "clone")
        clone_button.clicked.connect(self.clone_repo)
        button_layout.addWidget(clone_button)

        # 导入按钮
        import_button = StyledButton("import")
        import_button.setProperty("text_key", "import")
        import_button.clicked.connect(self.import_repo)
        button_layout.addWidget(import_button)

        # 批量导入按钮
        batch_import_button = StyledButton("batch_import")
        batch_import_button.setProperty("text_key", "batch_import")
        batch_import_button.clicked.connect(self.batch_import_repos)
        button_layout.addWidget(batch_import_button)

        # 移除按钮
        remove_button = StyledButton("remove")
        remove_button.setProperty("text_key", "remove")
        remove_button.clicked.connect(self.remove_repos)
        button_layout.addWidget(remove_button)

        header_layout.addLayout(button_layout)
        layout.addLayout(header_layout)

        # 仓库表格
        self.repos_table = QTableWidget()
        self.repos_table.setColumnCount(5)
        self.repos_table.setHorizontalHeaderLabels([
            tr("repo_name"),
            tr("current_branch"),
            tr("status"),
            tr("untracked"),
            tr("last_commit")
        ])
        self.repos_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.repos_table.setSelectionMode(QTableWidget.ExtendedSelection)
        self.repos_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.repos_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.repos_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.repos_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.repos_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.repos_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 4px;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                border-right: 1px solid #dee2e6;
                border-bottom: 1px solid #dee2e6;
                font-weight: bold;
                color: #495057;
            }
        """)
        layout.addWidget(self.repos_table)

        # 操作按钮组
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)

        # 分支按钮
        branch_button = StyledButton("branch")
        branch_button.setProperty("text_key", "branch_action")
        branch_button.clicked.connect(self.show_branch_menu)
        actions_layout.addWidget(branch_button)

        # 提交按钮
        commit_button = StyledButton("commit")
        commit_button.setProperty("text_key", "commit")
        commit_button.clicked.connect(self.commit_changes)
        actions_layout.addWidget(commit_button)

        # 推送按钮
        push_button = StyledButton("push")
        push_button.setProperty("text_key", "push")
        push_button.clicked.connect(self.push_changes)
        actions_layout.addWidget(push_button)

        # 拉取按钮
        pull_button = StyledButton("pull")
        pull_button.setProperty("text_key", "pull")
        pull_button.clicked.connect(self.pull_changes)
        actions_layout.addWidget(pull_button)

        # 刷新按钮
        refresh_button = StyledButton("refresh")
        refresh_button.setProperty("text_key", "refresh")
        refresh_button.clicked.connect(self.main_window.refresh_repos_table)
        actions_layout.addWidget(refresh_button)

        layout.addLayout(actions_layout)

    def clone_repo(self):
        url, ok = QInputDialog.getText(self, tr("clone_repo"), tr("input_repo_url"))
        if ok and url:
            try:
                path = QFileDialog.getExistingDirectory(self, tr("select_workspace_directory"))
                if path:
                    repo_name = url.split("/")[-1].replace(".git", "")
                    self.main_window.cbox.clone_repo(self.main_window.current_workspace, url, repo_name, path)
                    self.main_window.refresh_repos_table()
                    QMessageBox.information(self, tr("success"), tr("repo_imported"))
            except Exception as e:
                QMessageBox.warning(self, tr("error"), str(e))

    def import_repo(self):
        path = QFileDialog.getExistingDirectory(self, tr("select_workspace_directory"))
        if path:
            try:
                repo_name = os.path.basename(path)
                self.main_window.cbox.import_repo(self.main_window.current_workspace, repo_name, path)
                self.main_window.refresh_repos_table()
                QMessageBox.information(self, tr("success"), tr("repo_imported"))
            except Exception as e:
                QMessageBox.warning(self, tr("error"), str(e))

    def batch_import_repos(self):
        path = QFileDialog.getExistingDirectory(self, tr("select_workspace_directory"))
        if path:
            try:
                count = self.main_window.cbox.batch_import_repos(self.main_window.current_workspace, path)
                self.main_window.refresh_repos_table()
                QMessageBox.information(self, tr("success"), 
                    f"{tr('batch_import_completed')}: {count} {tr('repo_name')}")
            except Exception as e:
                QMessageBox.warning(self, tr("error"), str(e))

    def remove_repos(self):
        selected = self.repos_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, tr("note"), tr("please_select_repo"))
            return

        repos = set()
        for item in selected:
            if item.column() == 0:  # 仓库名称列
                repos.add(item.text())

        if not repos:
            return

        msg = f"{tr('confirm_remove_repo')}:\n" + "\n".join(repos)
        msg += f"\n\n{tr('this_will_not_delete_actual_files')}"
        
        reply = QMessageBox.question(self, tr("confirm_remove"), msg,
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                for repo in repos:
                    self.main_window.cbox.remove_repo(self.main_window.current_workspace, repo)
                self.main_window.refresh_repos_table()
            except Exception as e:
                QMessageBox.warning(self, tr("error"), str(e))

    def show_branch_menu(self):
        if not self.main_window.current_workspace:
            QMessageBox.warning(self, tr("note"), tr("please_select_workspace"))
            return

        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 8px;
            }
            QMenu::item {
                padding: 8px 32px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #f3e5f5;
                color: #9c27b0;
            }
        """)

        create_action = menu.addAction(tr("create_branch"))
        switch_action = menu.addAction(tr("switch_branch"))
        merge_action = menu.addAction(tr("merge_branch"))

        action = menu.exec_(QCursor.pos())
        if not action:
            return

        try:
            if action == create_action:
                self.create_branch()
            elif action == switch_action:
                self.switch_branch()
            elif action == merge_action:
                self.merge_branch()

        except Exception as e:
            QMessageBox.warning(self, tr("error"), str(e))

    def create_branch(self):
        dialog = BranchDialog(self, "create")
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            # data 至少包含一个键为"name"的元素, 且 name 不能为空和 name 不为空字符串
            if "name" not in data or not data["name"] or data["name"].isspace():
                QMessageBox.warning(self, tr("error"), tr("branch name is required"))
                return
            # 从data中获取分支的名称和start_point
            # 然后调用self.main_window.cbox.create_branch()方法创建分支
            # 最后刷新仓库表格
            # 注意：这里需要判断start_point是否为空，如果为空则调用create_branch_without_start_point()方法
            # 如果不为空则调用create_branch_with_start_point()方法
            self.main_window.cbox.create_branch(self.main_window.current_workspace, data["name"], data["start_point"])
            self.main_window.refresh_repos_table()


    def switch_branch(self):
        dialog = BranchDialog(self, "switch")
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            # data 至少包含一个键为"name"的元素, 且 name 不能为空和 name 不为空字符串
            # 然后调用self.main_window.cbox.switch_branch()方法切换分支
            # 最后刷新仓库表格
            if "name" not in data or not data["name"] or data["name"].isspace():
                QMessageBox.warning(self, tr("error"), tr("branch name is required"))
                return
            self.main_window.cbox.switch_branch(self.main_window.current_workspace, data["name"])
            self.main_window.refresh_repos_table()
        
    def merge_branch(self):
        dialog = BranchDialog(self, "merge")
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            # data 至少包含一个键为"name"的元素, 且 name 不能为空和 name 不为空字符串
            # 然后调用self.main_window.cbox.merge_branch()方法合并分支
            # 最后刷新仓库表格
            if "name" not in data or not data["name"] or data["name"].isspace():
                QMessageBox.warning(self, tr("error"), tr("branch name is required"))
                return
            self.main_window.cbox.merge(self.main_window.current_workspace, data["name"])
            self.main_window.refresh_repos_table()
       
    def commit_changes(self):
        # 当前worskspace
        if not self.main_window.current_workspace:
            QMessageBox.warning(self, tr("note"), tr("please_select_workspace"))
            return
        dialog = CommitDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            message = dialog.get_message()
            if not message:
                QMessageBox.warning(self, tr("error"), tr("commit_msg_required"))
                return

            try:
                self.main_window.cbox.commit(self.main_window.current_workspace, message)
                self.main_window.refresh_repos_table()
                QMessageBox.information(self, tr("success"), tr("changes_committed"))
            except Exception as e:
                QMessageBox.warning(self, tr("error"), str(e))

    def push_changes(self):
        print("push_changes")
        if not self.main_window.current_workspace:
            QMessageBox.warning(self, tr("note"), tr("please_select_workspace"))
            return
        try:
            self.main_window.cbox.push(self.main_window.current_workspace)
            self.main_window.refresh_repos_table()
            QMessageBox.information(self, tr("success"), tr("changes_pushed"))
        except Exception as e:
            QMessageBox.warning(self, tr("error"), str(e))
        
    def pull_changes(self):
        if not self.main_window.current_workspace:
            QMessageBox.warning(self, tr("note"), tr("please_select_workspace"))
            return
        try:
            self.main_window.cbox.pull(self.main_window.current_workspace)
            self.main_window.refresh_repos_table()
            QMessageBox.information(self, tr("success"), tr("changes_pulled"))
        except Exception as e:
            QMessageBox.warning(self, tr("error"), str(e))
       
    def retranslate_ui(self):
        # 更新标题
        title = self.findChild(QLabel)
        if title:
            title.setText(tr("repo_name"))
        
        # 更新表格头
        self.repos_table.setHorizontalHeaderLabels([
            tr("repo_name"),
            tr("current_branch"),
            tr("status"),
            tr("untracked"),
            tr("last_commit")
        ])
        
        # 更新按钮文本
        for button in self.findChildren(StyledButton):
            if button.property("text_key"):
                button.setText(tr(button.property("text_key")))

class CBoxGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cbox = CBox()
        self.setup_ui()
        self.current_workspace = None
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_all_status)
        self.refresh_timer.start(30000)

    def change_language(self, language):
        from .i18n import LanguageManager
        LanguageManager.instance().set_language(language)
        self.retranslate_ui()

    def retranslate_ui(self):
        """更新所有界面文本"""
        # 更新窗口标题
        self.setWindowTitle(tr("cbox_manager"))
        
        # 更新工具栏
        for action in self.toolbar.actions():
            if action.data():
                action.setText(tr(action.data()))

        # 更新菜单
        for menu in self.menuBar().actions():
            if menu.data():
                menu.setText(tr(menu.data()))
            # 更新子菜单项
            if menu.menu():
                for action in menu.menu().actions():
                    if action.data():
                        action.setText(tr(action.data()))

        # 更新工作空间面板
        self.workspace_panel.retranslate_ui()
        
        # 更新仓库面板
        self.repo_panel.retranslate_ui()

        # 刷新表格以更新所有状态文本
        self.refresh_repos_table()

    def setup_ui(self):
        self.setWindowTitle(tr("cbox_manager"))
        self.setMinimumSize(1200, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
        """)

        # 创建工具栏
        self.toolbar = self.addToolBar("Main Toolbar")
        self.toolbar.setMovable(False)
        self.toolbar.setStyleSheet("""
            QToolBar {
                border: none;
                background-color: #f8f9fa;
                spacing: 10px;
                padding: 5px;
            }
        """)

        # 添加语言切换按钮
        lang_button = StyledButton(tr("language"))
        lang_menu = QMenu(lang_button)
        lang_menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 8px;
            }
            QMenu::item {
                padding: 8px 32px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
        """)
        
        english_action = lang_menu.addAction("English")
        english_action.setData("en")
        chinese_action = lang_menu.addAction("中文")
        chinese_action.setData("zh")
        
        lang_button.setMenu(lang_menu)
        
        english_action.triggered.connect(lambda: self.change_language("en"))
        chinese_action.triggered.connect(lambda: self.change_language("zh"))
        
        self.toolbar.addWidget(lang_button)

        # 创建主窗口布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 创建工作空间面板
        self.workspace_panel = WorkspacePanel(self)
        self.workspace_panel.workspace_list.currentItemChanged.connect(self.on_workspace_selected)
        main_layout.addWidget(self.workspace_panel, 1)

        # 创建仓库面板
        self.repo_panel = RepositoryPanel(self)
        main_layout.addWidget(self.repo_panel, 3)

        # 初始化工作空间列表
        self.refresh_workspaces_list()

    def refresh_repos_table(self):
        """刷新仓库表格，确保所有文本都使用当前语言"""
        if not self.current_workspace:
            self.repo_panel.repos_table.setRowCount(0)
            return

        try:
            repos = self.cbox.list_repos(self.current_workspace)
            self.repo_panel.repos_table.setRowCount(len(repos))
            
            for row, repo_name in enumerate(repos):
                # 仓库名称
                name_item = QTableWidgetItem(repo_name)
                
                try:
                    repo = self.cbox.get_repo(self.current_workspace, repo_name)
                    
                    # 当前分支
                    branch = repo.active_branch.name
                    branch_item = QTableWidgetItem(branch)
                    
                    # 状态
                    is_dirty = repo.is_dirty()
                    status = tr("has_changes") if is_dirty else tr("clean")
                    status_item = QTableWidgetItem(status)
                    if is_dirty:
                        status_item.setForeground(QBrush(QColor("#f44336")))
                    else:
                        status_item.setForeground(QBrush(QColor("#4caf50")))
                    
                    # 未跟踪文件
                    untracked = len(repo.untracked_files)
                    untracked_item = QTableWidgetItem(str(untracked))
                    if untracked > 0:
                        untracked_item.setForeground(QBrush(QColor("#ff9800")))
                    
                    # 最近提交
                    try:
                        last_commit = repo.head.commit
                        first_line = last_commit.message.split('\n')[0]
                        commit_msg = f"{first_line} ({last_commit.hexsha[:7]})"
                    except:
                        commit_msg = tr("no_commits")
                    commit_item = QTableWidgetItem(commit_msg)
                    
                except Exception as e:
                    branch_item = QTableWidgetItem(tr("error"))
                    status_item = QTableWidgetItem(str(e))
                    untracked_item = QTableWidgetItem("-")
                    commit_item = QTableWidgetItem("-")
                
                self.repo_panel.repos_table.setItem(row, 0, name_item)
                self.repo_panel.repos_table.setItem(row, 1, branch_item)
                self.repo_panel.repos_table.setItem(row, 2, status_item)
                self.repo_panel.repos_table.setItem(row, 3, untracked_item)
                self.repo_panel.repos_table.setItem(row, 4, commit_item)
                
        except Exception as e:
            QMessageBox.warning(self, tr("error"), str(e))

    def remove_workspace(self):
        if not self.current_workspace:
            QMessageBox.warning(self, tr("error"), tr("please_select_workspace"))
            return

        reply = QMessageBox.question(self, tr("confirm_delete"), 
                                   f"{tr('confirm_delete_workspace')} '{self.current_workspace}'?\n{tr('note')}: {tr('this_will_not_delete_actual_files')}",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                self.cbox.remove_workspace(self.current_workspace)
                self.current_workspace = None
                self.refresh_workspaces_list()
                self.repo_panel.repos_table.setRowCount(0)
            except Exception as e:
                QMessageBox.warning(self, tr("error"), str(e))

    def remove_repository(self):
        if not self.current_workspace:
            QMessageBox.warning(self, tr("error"), tr("please_select_workspace"))
            return

        selected_items = self.repo_panel.repos_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, tr("error"), tr("please_select_repo"))
            return

        repo_names = set()
        for item in selected_items:
            if item.column() == 0:  # 仓库名称列
                repo_names.add(item.text())

        if not repo_names:
            return

        repos_str = "\n".join(repo_names)
        reply = QMessageBox.question(self, tr("confirm_remove"), 
                                   f"{tr('confirm_remove_repo')}?\n{repos_str}\n{tr('note')}: {tr('this_will_not_delete_actual_files')}",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                for repo in repo_names:
                    self.cbox.remove_repo(self.current_workspace, repo)
                self.refresh_repos_table()
            except Exception as e:
                QMessageBox.warning(self, tr("error"), str(e))

    def commit_changes(self):
        if not self.current_workspace:
            QMessageBox.warning(self, tr("error"), tr("select_workspace"))
            return

        dialog = CommitDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            message = dialog.get_message()
            if not message:
                QMessageBox.warning(self, tr("error"), tr("commit_msg_required"))
                return
            try:
                self.cbox.commit(self.current_workspace, message)
                self.refresh_repos_table()
                QMessageBox.information(self, tr("success"), tr("changes_committed"))
            except Exception as e:
                QMessageBox.warning(self, tr("error"), str(e))

    def show_add_workspace_dialog(self):
        dialog = AddWorkspaceDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            try:
                self.cbox.add_workspace(data['name'], data['path'])
                self.refresh_workspaces_list()
            except ValueError as e:
                QMessageBox.warning(self, tr("error"), str(e))

    def import_repository(self):
        if not self.current_workspace:
            QMessageBox.warning(self, tr("error"), tr("please_select_workspace"))
            return
        
        repo_path = QFileDialog.getExistingDirectory(self, tr("select_repo_directory"))
        if repo_path:
            try:
                self.cbox.import_repo(self.current_workspace, repo_path)
                self.refresh_repos_table()
                QMessageBox.information(self, tr("success"), tr("repo_imported"))
            except Exception as e:
                QMessageBox.warning(self, tr("error"), str(e))

    def batch_import_repositories(self):
        if not self.current_workspace:
            QMessageBox.warning(self, tr("error"), tr("please_select_workspace"))
            return
        
        scan_path = QFileDialog.getExistingDirectory(self, tr("select_scan_directory"))
        if scan_path:
            try:
                self.cbox.scan_import(self.current_workspace, scan_path)
                self.refresh_repos_table()
                QMessageBox.information(self, tr("success"), tr("batch_import_completed"))
            except Exception as e:
                QMessageBox.warning(self, tr("error"), str(e))

        if not self.current_workspace:
            QMessageBox.warning(self, tr("error"), tr("please_select_workspace"))
            return

        if mode == "merge":
            branch_name, ok = QInputDialog.getText(self, tr("merge_branch"), tr("input_branch_name"))
            if ok and branch_name:
                try:
                    self.cbox.merge(self.current_workspace, branch_name)
                    self.refresh_repos_table()
                    QMessageBox.information(self, tr("success"), tr("branch_merged"))
                except Exception as e:
                    QMessageBox.warning(self, tr("error"), str(e))
            return

        dialog = BranchDialog(self, mode)
        if mode == "switch":
            # 获取当前仓库的分支列表
            repo_name = selected_items[0].text()
            try:
                branches = self.cbox.switch_branch(self.current_workspace, repo_name)
                dialog.set_branches(branches)
            except Exception as e:
                QMessageBox.warning(self, tr("error"), f"{tr('failed_to_get_branches')}: {str(e)}")
                return

        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            try:
                if mode == "create":
                    self.cbox.create_branch(self.current_workspace, data['name'], data['start_point'])
                else:  # switch
                    self.cbox.switch_branch(self.current_workspace, data['name'])
                self.refresh_repos_table()
                QMessageBox.information(self, tr("success"), 
                    tr("branch_created") if mode == "create" else tr("branch_switched"))
            except Exception as e:
                QMessageBox.warning(self, tr("error"), str(e))

    def refresh_workspaces_list(self):
        self.workspace_panel.workspace_list.clear()
        for name, path in self.cbox.workspaces.items():
            item = WorkspaceListItem(name, path)
            self.workspace_panel.workspace_list.addItem(item)

    def refresh_repos_table(self, workspace_name=None):
        if workspace_name is None and self.current_workspace:
            workspace_name = self.current_workspace
        if not workspace_name:
            return

        self.repo_panel.repos_table.setRowCount(0)
        try:
            repos = self.cbox._get_repos_in_workspace(workspace_name)
            changes_count = 0
            
            for repo in repos:
                row = self.repo_panel.repos_table.rowCount()
                self.repo_panel.repos_table.insertRow(row)
                
                # 仓库名称
                name = os.path.basename(repo.working_dir)
                name_item = QTableWidgetItem(name)
                name_item.setFlags(Qt.ItemIsEnabled)  # 禁止编辑
                
                # 当前分支
                branch = repo.active_branch.name
                branch_item = QTableWidgetItem(branch)
                branch_item.setFlags(Qt.ItemIsEnabled)  # 禁止编辑
                
                # 状态
                is_dirty = repo.is_dirty()
                status = tr("has_changes") if is_dirty else tr("clean")
                status_item = QTableWidgetItem(status)
                status_item.setFlags(Qt.ItemIsEnabled)  # 禁止编辑
                if is_dirty:
                    status_item.setForeground(QBrush(QColor("#f44336")))  # 红色
                    changes_count += 1
                else:
                    status_item.setForeground(QBrush(QColor("#4caf50")))  # 绿色
                
                # 未跟踪文件
                untracked = len(repo.untracked_files)
                untracked_item = QTableWidgetItem(str(untracked))
                untracked_item.setFlags(Qt.ItemIsEnabled)  # 禁止编辑
                if untracked > 0:
                    untracked_item.setForeground(QBrush(QColor("#ff9800")))  # 橙色
                
                # 最近提交
                try:
                    last_commit = repo.head.commit
                    first_line = last_commit.message.split('\n')[0]
                    commit_msg = f"{first_line} ({last_commit.hexsha[:7]})"
                except:
                    commit_msg = tr("no_commits")
                commit_item = QTableWidgetItem(commit_msg)
                commit_item.setFlags(Qt.ItemIsEnabled)  # 禁止编辑
                
                self.repo_panel.repos_table.setItem(row, 0, name_item)
                self.repo_panel.repos_table.setItem(row, 1, branch_item)
                self.repo_panel.repos_table.setItem(row, 2, status_item)
                self.repo_panel.repos_table.setItem(row, 3, untracked_item)
                self.repo_panel.repos_table.setItem(row, 4, commit_item)
            
            # 更新工作空间列表项的更改计数
            for i in range(self.workspace_panel.workspace_list.count()):
                item = self.workspace_panel.workspace_list.item(i)
                if item.name == workspace_name:
                    item.update_changes_count(changes_count)
                    break
                    
        except Exception as e:
            QMessageBox.warning(self, tr("error"), str(e))

    def on_workspace_selected(self, current, previous):
        if current:
            self.current_workspace = current.name
            self.refresh_repos_table(current.name)

    def refresh_all_status(self):
        """定期刷新所有状态"""
        if self.current_workspace:
            self.refresh_repos_table(self.current_workspace)

    def clone_repository(self):
        if not self.current_workspace:
            QMessageBox.warning(self, tr("error"), tr("please_select_workspace"))
            return

        repo_url, ok = QInputDialog.getText(self, tr("clone_repo"), tr("input_repo_url"))
        if ok and repo_url:
            try:
                self.cbox.clone(self.current_workspace, repo_url)
                self.refresh_repos_table()
            except Exception as e:
                QMessageBox.warning(self, tr("error"), str(e))

    def check_status(self):
        if not self.current_workspace:
            QMessageBox.warning(self, tr("error"), tr("please_select_workspace"))
            return
        self.refresh_repos_table()

    def pull_repositories(self):
        if not self.current_workspace:
            QMessageBox.warning(self, tr("error"), tr("please_select_workspace"))
            return

        try:
            self.cbox.pull(self.current_workspace)
            self.refresh_repos_table()
            QMessageBox.information(self, tr("success"), tr("all_repos_updated"))
        except Exception as e:
            QMessageBox.warning(self, tr("error"), str(e))

    def push_changes(self):
        if not self.current_workspace:
            QMessageBox.warning(self, tr("error"), tr("select_workspace"))
            return

        try:
            # 批量推送
            self.cbox.push(self.current_workspace)
            
            self.refresh_repos_table()
            QMessageBox.information(self, tr("success"), tr("changes_pushed"))
        except Exception as e:
            QMessageBox.warning(self, tr("error"), str(e))

def main():
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle("Fusion")
    
    window = CBoxGUI()
    window.show()
    sys.exit(app.exec())
