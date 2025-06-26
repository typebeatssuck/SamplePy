"""
Minimal Text User Interface (TUI) for SamplePy
Simple, clean implementation focusing on core functionality
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Tree, Label, Button, Input
from textual.widgets.tree import TreeNode
from textual.reactive import reactive
from textual import work
from textual.binding import Binding
from pathlib import Path
from typing import List, Optional
import os
from textual.events import Key
from samplepy.core.file_utils import FileUtils
from textual import on

class FileTree(Tree):
    """Tree widget for displaying file system hierarchy"""
    
    def __init__(self, **kwargs):
        super().__init__("File System", **kwargs)
        self.root_path = Path.cwd()
        self.current_selection: Optional[Path] = None
        self.populated_nodes = set()  # Track which nodes have been populated
    
    def load_directory(self, path: Path):
        """Load and display the directory structure"""
        self.root_path = path
        self.clear()
        self.populated_nodes.clear()
        
        # Set the root label to the current directory name
        self.root.label = path.name or str(path)
        self.root.data = path
        
        try:
            self._populate_node(self.root, path)
            self.populated_nodes.add(self.root)
        except Exception as e:
            # Add error node if we can't access the directory
            error_node = self.root.add("Error accessing directory")
            error_node.data = None
        
        # Expand the root by default
        self.root.expand()
    
    def _populate_node(self, node: TreeNode, path: Path):
        """Recursively populate a tree node with directory contents"""
        try:
            # Get all items in the directory
            items = []
            for item in path.iterdir():
                items.append(item)
            
            # Sort: directories first, then files
            items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
            
            # Add items to the tree
            for item in items:
                child_node = node.add(item.name)
                child_node.data = item
                
                # Mark directories with a folder icon
                if item.is_dir():
                    child_node.label = f"\U0001F4C1 {item.name}"
                else:
                    child_node.label = f"\U0001F4C4 {item.name}"
        except PermissionError:
            # Add permission denied node
            node.add("\U0001F512 Permission Denied")
        except Exception:
            # Add error node
            node.add("\u274C Error")
    
    def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        """Handle node expansion - always reload children from disk."""
        node = event.node
        if node.data and isinstance(node.data, Path) and node.data.is_dir():
            # Remove all children before repopulating
            node.remove_children()
            self._populate_node(node, node.data)
            self.populated_nodes.add(node)
    
    def on_tree_node_highlighted(self, event: Tree.NodeHighlighted) -> None:
        """Update current_selection to the highlighted (cursor) node as the user moves."""
        if event.node.data and isinstance(event.node.data, Path):
            self.current_selection = event.node.data
            app = self.app
            if app:
                utility_panel = app.query_one("#utility-panel", UtilityPanel)
                utility_panel.clear_panel()  # Clear panel on focus change
    
    def get_selected_path(self) -> Optional[Path]:
        """Get the currently selected file/directory path"""
        return self.current_selection

    def get_node_for_path(self, path: Path):
        # Helper to find the TreeNode for a given path
        file_tree = self.app.query_one("#file-tree", FileTree) if self.app else None
        if not file_tree:
            return None
        def _find(node):
            if getattr(node, 'data', None) == path:
                return node
            for child in getattr(node, 'children', []):
                found = _find(child)
                if found:
                    return found
            return None
        return _find(self.root)


class UtilityPanel(Container):
    """Bottom utility panel for actions only (blank by default)"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_path = None
        self.action_index = 0
        self.actions: list[str] = []
        self.has_actions = False
        self.can_focus = True  # Make UtilityPanel focusable
        self._input_callback = None
        self._input_context = None
        self._input_prompt = None
    
    def compose(self) -> ComposeResult:
        """Create the utility panel content (blank by default)"""
        with Container(id="utility-content"):
            yield Container(id="utility-actions")

    def show_actions(self, path: Optional[Path]):
        """Show context-specific actions for the selected item in the actions panel."""
        actions_container = self.query_one("#utility-actions", Container)
        actions_container.remove_children()
        self.action_index = 0
        self.has_actions = False
        self.actions = []
        if path is None:
            return
        if path.is_dir():
            self.actions = [
                "[Enter] Open Directory",
                "[N] New File",
                "[F] New Folder",
                "[Del] Delete Directory",
                "[R] Rename Directory"
            ]
        else:
            self.actions = [
                "[Enter] Open File",
                "[Del] Delete File",
                "[R] Rename File"
            ]
        self.has_actions = bool(self.actions)
        self._render_actions()
        if self.app:
            self.app.set_focus(self)  # Explicitly move focus to UtilityPanel
        self.focus()  # Ensure focus is set to UtilityPanel

    def _render_actions(self):
        actions_container = self.query_one("#utility-actions", Container)
        actions_container.remove_children()
        for i, action in enumerate(self.actions):
            classes = "selected-action" if i == self.action_index else ""
            actions_container.mount(Label(action, classes=classes))

    def clear_panel(self):
        actions_container = self.query_one("#utility-actions", Container)
        actions_container.remove_children()
        self.actions = []
        self.action_index = 0
        self.has_actions = False

    def on_key(self, event: Key) -> None:
        if not self.has_actions:
            return
        action = self.actions[self.action_index] if self.actions else None
        file_tree = self.app.query_one("#file-tree", FileTree) if self.app else None
        selected_path = file_tree.get_selected_path() if file_tree else None
        app = self.app
        if event.key == "up":
            self.action_index = (self.action_index - 1) % len(self.actions)
            self._render_actions()
            event.stop()
        elif event.key == "down":
            self.action_index = (self.action_index + 1) % len(self.actions)
            self._render_actions()
            event.stop()
        elif event.key == "escape":
            if app:
                file_tree = app.query_one("#file-tree", FileTree)
                app.set_focus(file_tree)
                file_tree.focus()
            self.clear_panel()
            event.stop()
        elif event.key == "enter":
            if action and selected_path:
                if action.startswith("[Enter] Open Directory"):
                    # Expand/collapse the folder in the tree
                    if file_tree:
                        node = file_tree.get_node_for_path(selected_path)
                        if node:
                            node.toggle()
                        app.set_focus(file_tree)
                        file_tree.focus()
                        self.clear_panel()
                elif action.startswith("[N] New File"):
                    self._prompt_new_file(selected_path)
                elif action.startswith("[F] New Folder"):
                    self._prompt_new_folder(selected_path)
                elif action.startswith("[Del] Delete"):
                    self._delete_path(selected_path)
                elif action.startswith("[R] Rename"):
                    self._prompt_rename(selected_path)
                # [Enter] Open File is not implemented
            event.stop()
        # Optionally: handle N, F, Del, R as direct shortcuts
        elif event.key.lower() == "n" and any(a.startswith("[N] New File") for a in self.actions):
            if selected_path:
                self._prompt_new_file(selected_path)
            event.stop()
        elif event.key.lower() == "f" and any(a.startswith("[F] New Folder") for a in self.actions):
            if selected_path:
                self._prompt_new_folder(selected_path)
            event.stop()
        elif event.key.lower() == "r" and any(a.startswith("[R] Rename") for a in self.actions):
            if selected_path:
                self._prompt_rename(selected_path)
            event.stop()
        elif event.key.lower() == "delete" and any(a.startswith("[Del] Delete") for a in self.actions):
            if selected_path:
                self._delete_path(selected_path)
            event.stop()

    def _prompt_new_file(self, dir_path: Path):
        # Show input for new file name
        self._show_input("New file name:", lambda name: self._create_file(dir_path, name))

    def _prompt_new_folder(self, dir_path: Path):
        # Show input for new folder name
        self._show_input("New folder name:", lambda name: self._create_folder(dir_path, name))

    def _prompt_rename(self, path: Path):
        # Show input for new name
        self._show_input("Rename to:", lambda name: self._rename_path(path, name))

    def _show_input(self, prompt: str, callback):
        actions_container = self.query_one("#utility-actions", Container)
        actions_container.remove_children()  # Always clear before adding new input
        input_widget = Input(placeholder=prompt)
        actions_container.mount(input_widget)
        input_widget.focus()
        self._input_callback = callback
        self._input_context = input_widget
        self._input_prompt = prompt

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if self._input_context and event.input is self._input_context:
            value = event.value.strip()
            actions_container = self.query_one("#utility-actions", Container)
            # Remove previous error/success messages
            for child in list(actions_container.children)[1:]:
                child.remove()
            if not self._input_callback:
                actions_container.mount(Label("[ERROR] No callback set!"))
                self._input_context.focus()
                return
            if value:
                result = self._input_callback(value)
                if result:
                    self._refresh_and_clear()
                else:
                    actions_container.mount(Label("Error: Operation failed. Try again."))
                    self._input_context.focus()
            else:
                actions_container.mount(Label("Error: Invalid input. Try again."))
                self._input_context.focus()

    def _create_file(self, dir_path: Path, name: str):
        new_path = dir_path / name
        result = FileUtils.create_file(new_path)
        if result:
            self._refresh_and_clear()
        return result

    def _create_folder(self, dir_path: Path, name: str):
        new_path = dir_path / name
        result = FileUtils.create_folder(new_path)
        if result:
            self._refresh_and_clear()
        return result

    def _delete_path(self, path: Path):
        result = FileUtils.delete_path(path)
        if result:
            self._refresh_and_clear()
        return result

    def _rename_path(self, path: Path, new_name: str):
        new_path = path.parent / new_name
        result = FileUtils.rename_path(path, new_path)
        if result:
            self._refresh_and_clear()
        return result

    def _refresh_and_clear(self):
        # Refresh file tree and clear panel
        app = self.app
        if app:
            file_tree = app.query_one("#file-tree", FileTree)
            app.set_focus(file_tree)
            file_tree.focus()
            app.load_current_directory()
        self.clear_panel()

    def _show_message(self, message: str):
        actions_container = self.query_one("#utility-actions", Container)
        actions_container.remove_children()
        actions_container.mount(Label(message))
        # Clear all input state after error
        self._input_callback = None
        self._input_context = None
        self._input_prompt = None


class SamplePyTUI(App):
    """Simple TUI application for SamplePy"""
    
    CSS = """
    App {
        background: black;
        color: white;
    }
    
    #main-container {
        height: 100%;
        width: 100%;
    }
    
    #header {
        height: 3;
        border-bottom: solid white;
        padding: 1;
    }
    
    #content {
        height: 1fr;
    }
    
    #file-panel {
        height: 70%;
        border-bottom: solid white;
    }
    
    #file-tree {
        height: 1fr;
        border: solid white;
    }
    
    #utility-panel {
        height: 30%;
        border: solid white;
    }
    
    #utility-content {
        height: 100%;
        /* padding: 1; */
    }
    
    #utility-title {
        text-align: center;
        border-bottom: solid white;
        /* padding: 1; */
    }
    
    #utility-info {
        /* padding: 1; */
        text-align: center;
    }
    
    #utility-actions {
        height: 1fr;
        /* padding: 1; */
    }
    
    #nav-info, #help-info {
        text-align: center;
        /* padding: 1; */
    }
    
    Tree {
        border: solid white;
    }
    
    Label {
        color: white;
    }
    
    .selected-action {
        background: white;
        color: black;
        text-style: bold;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("enter", "open_selected", "Open"),
        Binding("backspace", "go_back", "Back"),
        Binding("a", "show_actions", "Actions"),
    ]
    
    def __init__(self):
        super().__init__()
        self.current_path = Path.cwd()
        self.path_history = []
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app"""
        with Container(id="main-container"):
            yield Label(f"Current: {self.current_path}", id="header")
            
            with Container(id="content"):
                with Container(id="file-panel"):
                    yield FileTree(id="file-tree")
                
                yield UtilityPanel(id="utility-panel")
    
    def on_mount(self) -> None:
        """Called when the app is mounted"""
        self.load_current_directory()
    
    def load_current_directory(self):
        """Load the current directory into the tree"""
        file_tree = self.query_one("#file-tree", FileTree)
        file_tree.load_directory(self.current_path)
    
    def action_quit(self) -> None:
        """Quit the application"""
        self.exit()
    
    def action_refresh(self) -> None:
        """Refresh the file tree"""
        self.load_current_directory()
    
    def action_open_selected(self) -> None:
        """Open selected file or directory"""
        file_tree = self.query_one("#file-tree", FileTree)
        selected_path = file_tree.get_selected_path()
        
        if selected_path:
            if selected_path.is_dir():
                # Navigate to directory
                self.path_history.append(self.current_path)
                self.current_path = selected_path
                self.load_current_directory()
                # Clear utility panel selection
                utility_panel = self.query_one("#utility-panel", UtilityPanel)
                utility_panel.clear_panel()
            else:
                # File selected - update utility panel
                utility_panel = self.query_one("#utility-panel", UtilityPanel)
                # No info or status update
    
    def action_go_back(self) -> None:
        """Go back to previous directory"""
        if self.path_history:
            self.current_path = self.path_history.pop()
            self.load_current_directory()
            
            # Clear utility panel selection
            utility_panel = self.query_one("#utility-panel", UtilityPanel)
            utility_panel.clear_panel()
    
    def action_show_actions(self) -> None:
        """Show actions for the currently highlighted item in the file tree and focus the panel."""
        file_tree = self.query_one("#file-tree", FileTree)
        utility_panel = self.query_one("#utility-panel", UtilityPanel)
        selected_path = file_tree.get_selected_path()
        utility_panel.show_actions(selected_path)
        # Focus is now handled in show_actions


def run_minimal_tui():
    """Run the minimal TUI"""
    app = SamplePyTUI()
    app.run() 