"""
Minimal Text User Interface (TUI) for SamplePy
Simple, clean implementation focusing on core functionality
"""

from pathlib import Path
from typing import Optional, List, Callable

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Tree, Label, Input
from textual.widgets.tree import TreeNode
from textual.message import Message
from textual.binding import Binding
from textual.events import Key

from samplepy.core.file_utils import FileUtils


class FileTree(Tree[Path]):
    """Tree widget for displaying file system hierarchy"""

    def __init__(self, path: Path, **kwargs):
        super().__init__(path.name or str(path), data=path, **kwargs)
        self.root_path = path

    def reload(self, new_path: Optional[Path] = None) -> None:
        """Reload the tree view from the specified path or the current root."""
        if new_path:
            self.root_path = new_path
            self.root.data = new_path
            self.root.label = new_path.name or str(new_path)

        self.clear()
        self._populate_node(self.root)

    def _populate_node(self, node: TreeNode[Path]):
        """Populate a tree node with directory contents"""
        if not node.data or not node.data.is_dir():
            return

        try:
            items = sorted(
                node.data.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())
            )
            for item in items:
                node.add(
                    f"📁 {item.name}" if item.is_dir() else f"📄 {item.name}",
                    data=item,
                    allow_expand=item.is_dir(),
                )
        except PermissionError:
            node.add("🚫 Permission Denied", allow_expand=False)
        except Exception:
            node.add("❌ Error", allow_expand=False)

    def on_mount(self) -> None:
        """When the tree is mounted, populate the root."""
        self._populate_node(self.root)
        self.root.expand()

    def on_tree_node_expanded(self, event: Tree.NodeExpanded[Path]) -> None:
        """Handle node expansion - load children from disk."""
        # Clear existing children before populating
        event.node.remove_children()
        self._populate_node(event.node)


class UtilityPanel(Container):
    """Bottom utility panel for actions and user input."""

    class ActionMessage(Message):
        """Message to signal an action was requested."""
        def __init__(self, path: Path, action: str) -> None:
            self.path = path
            self.action = action
            super().__init__()

    class InputMessage(Message):
        """Message to signal input was submitted."""
        def __init__(self, value: str, action: str, path: Path) -> None:
            self.value = value
            self.action = action
            self.path = path
            super().__init__()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.can_focus = True
        self._selected_path: Optional[Path] = None
        self._current_actions: List[str] = []
        self._input_widget: Optional[Input] = None
        self._pending_action: Optional[str] = None
        self._action_index = 0

    def compose(self) -> ComposeResult:
        yield Container(id="utility-content")

    def show_actions_for(self, path: Optional[Path]) -> None:
        """Show context-specific actions for the selected item."""
        self._selected_path = path
        self._current_actions = []
        if path:
            if path.is_dir():
                self._current_actions = ["New File", "New Folder", "Rename", "Delete"]
            else:
                self._current_actions = ["Rename", "Delete"]
        self._render_actions()

    def _render_actions(self) -> None:
        """Render the action labels and ensure the panel has focus."""
        container = self.query_one("#utility-content", Container)
        container.remove_children()
        self._input_widget = None
        for i, action in enumerate(self._current_actions):
            label = Label(f"▸ {action}" if i == self._action_index else f"  {action}")
            container.mount(label)

        if self._current_actions:
            self.focus()

    def clear_panel(self) -> None:
        """Clear the panel and reset state."""
        self.query_one("#utility-content", Container).remove_children()
        self._selected_path = None
        self._current_actions = []
        self._input_widget = None
        self._pending_action = None
        self._action_index = 0

    def show_input_prompt(self, prompt: str, action: str) -> None:
        """Display an input field for an action."""
        self._pending_action = action
        container = self.query_one("#utility-content", Container)
        container.remove_children()
        self._input_widget = Input(placeholder=prompt)
        container.mount(self._input_widget)
        self._input_widget.focus()

    def on_key(self, event: Key) -> None:
        """Handle key presses for navigating actions."""
        if self._input_widget or not self._current_actions:
            return

        if event.key == "up":
            self._action_index = (self._action_index - 1) % len(self._current_actions)
            self._render_actions()
            event.stop()
        elif event.key == "down":
            self._action_index = (self._action_index + 1) % len(self._current_actions)
            self._render_actions()
            event.stop()
        elif event.key == "enter":
            action = self._current_actions[self._action_index]
            if self._selected_path:
                self.post_message(self.ActionMessage(self._selected_path, action))
            event.stop()

    @on(Input.Submitted)
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle when the user submits text."""
        value = event.value.strip()
        if value and self._pending_action and self._selected_path:
            self.post_message(self.InputMessage(value, self._pending_action, self._selected_path))
        else:
            self.post_message(self.ActionMessage(Path.cwd(), "clear_and_focus_tree"))


class SamplePyTUI(App):
    """Simple TUI application for SamplePy"""

    CSS_PATH = "main.css"

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh_tree", "Refresh"),
        Binding("backspace", "go_back", "Back"),
        ("a", "show_actions", "Actions"),
    ]

    def __init__(self):
        super().__init__()
        self.current_path = Path.cwd()
        self.path_history: List[Path] = []

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Container(
            FileTree(self.current_path, id="file-tree"),
            UtilityPanel(id="utility-panel"),
            id="main-container"
        )

    def _get_tree(self) -> FileTree:
        """Helper to get the file tree widget."""
        return self.query_one(FileTree)

    def _get_utility_panel(self) -> UtilityPanel:
        """Helper to get the utility panel widget."""
        return self.query_one(UtilityPanel)

    def _refresh_ui(self, focus_tree: bool = True) -> None:
        """Refreshes the UI by reloading the tree and clearing the panel."""
        self._get_tree().reload()
        self._get_utility_panel().clear_panel()
        if focus_tree:
            self._get_tree().focus()

    # --- Action Handlers ---

    def action_quit(self) -> None:
        self.exit()

    def action_refresh_tree(self) -> None:
        self._refresh_ui()

    def action_go_back(self) -> None:
        if self.path_history:
            self.current_path = self.path_history.pop()
            self.sub_title = str(self.current_path)
            self._get_tree().reload(self.current_path)
            self._get_utility_panel().clear_panel()

    def action_show_actions(self) -> None:
        tree = self._get_tree()
        if tree.cursor_node and tree.cursor_node.data:
            self._get_utility_panel().show_actions_for(tree.cursor_node.data)

    # --- Event Handlers (@on decorator) ---

    @on(Tree.NodeSelected)
    def on_tree_node_selected(self, event: Tree.NodeSelected[Path]) -> None:
        path = event.node.data
        if path and path.is_dir():
            self.path_history.append(self.current_path)
            self.current_path = path
            self.sub_title = str(self.current_path)
            self._get_tree().reload(self.current_path)
            self._get_utility_panel().clear_panel()
        elif path:
            self.action_show_actions()

    @on(UtilityPanel.ActionMessage)
    async def handle_utility_action(self, message: UtilityPanel.ActionMessage) -> None:
        utility_panel = self._get_utility_panel()
        
        if message.action == "clear_and_focus_tree":
            utility_panel.clear_panel()
            self._get_tree().focus()
            return
            
        action_prompts = {
            "New File": "Enter name for new file:",
            "New Folder": "Enter name for new folder:",
            "Rename": "Enter new name:",
        }
        
        if message.action in action_prompts:
            utility_panel.show_input_prompt(action_prompts[message.action], message.action)
        elif message.action == "Delete":
            success = FileUtils.delete_path(message.path)
            if success:
                self._refresh_ui()
            else:
                self.bell()

    @on(UtilityPanel.InputMessage)
    async def handle_utility_input(self, message: UtilityPanel.InputMessage) -> None:
        path = message.path
        new_name = message.value

        if message.action == "New File":
            success = FileUtils.create_file(path / new_name)
        elif message.action == "New Folder":
            success = FileUtils.create_folder(path / new_name)
        elif message.action == "Rename":
            success = FileUtils.rename_path(path, path.with_name(new_name))
        else:
            return

        if success:
            self._refresh_ui()
        else:
            self.bell()

    def _create_file(self, dir_path: Path, name: str):
        new_path = dir_path / name
        return FileUtils.create_file(new_path)

    def _create_folder(self, dir_path: Path, name: str):
        new_path = dir_path / name
        return FileUtils.create_folder(new_path)

    def _delete_path(self, path: Path):
        return FileUtils.delete_path(path)

    def _rename_path(self, path: Path, new_name: str):
        new_path = path.parent / new_name
        return FileUtils.rename_path(path, new_path)


def run_minimal_tui():
    """Run the minimal TUI."""
    app = SamplePyTUI()
    app.run()

if __name__ == "__main__":
    run_minimal_tui()