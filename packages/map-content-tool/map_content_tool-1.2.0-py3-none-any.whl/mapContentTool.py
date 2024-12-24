#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Map Content Tool
"""

import os
import json
import urwid
import logging
import sys
import argparse

# Set up logging
logging.basicConfig(
    filename="file_selector.log",  # Log filename
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,  # Default to INFO
)

# Global exception handler
def log_uncaught_exceptions(exc_type, exc_value, exc_traceback):
    """Log all uncaught exceptions to the error log."""
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    print("An error occurred. Check 'file_selector.log' for details.")
    sys.exit(1)

sys.excepthook = log_uncaught_exceptions

# Recursively get the folder structure excluding specified directories
def get_folder_structure(path, exclude_dirs=None):
    logging.info(f"Scanning folder structure at path: {path}")
    if exclude_dirs is None:
        exclude_dirs = []

    folder_structure = {}

    # Skip excluded directories
    if os.path.basename(path) in exclude_dirs:
        logging.info(f"Skipping excluded directory: {path}")
        return None

    if os.path.isdir(path):
        logging.info(f"Processing directory: {path}")
        folder_structure["name"] = os.path.basename(path)
        folder_structure["path"] = path
        folder_structure["type"] = "directory"
        folder_structure["items"] = []

        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            item_structure = get_folder_structure(item_path, exclude_dirs)
            if item_structure:
                folder_structure["items"].append(item_structure)
    else:
        logging.info(f"Processing file: {path}")
        folder_structure["name"] = os.path.basename(path)
        folder_structure["path"] = path
        folder_structure["type"] = "file"

    return folder_structure

# Write the selected file contents directly to the structure
def embed_selected_contents(folder_structure, selected_files):
    """
    Embed the contents of selected files into the folder structure.
    Recursively process selected folders to include their files.
    """
    if folder_structure["type"] == "file":
        if folder_structure in selected_files:
            try:
                logging.info(f"Reading content for file: {folder_structure['path']}")
                with open(folder_structure["path"], "r", encoding="utf-8") as f:
                    folder_structure["contents"] = f.read()
            except Exception as e:
                logging.error(f"Error reading file {folder_structure['name']}: {e}")
                folder_structure["contents"] = f"Error reading file: {e}"
    elif folder_structure["type"] == "directory":
        # Check if the folder itself is selected
        if folder_structure in selected_files:
            # Recursively mark all contents within the folder as selected
            for item in folder_structure.get("items", []):
                embed_selected_contents(item, selected_files)
        else:
            # Process only selected items within the folder
            for item in folder_structure.get("items", []):
                embed_selected_contents(item, selected_files)

# Save output to .json or .txt (both using JSON structure)
def save_output(folder_structure, output_file):
    try:
        content = json.dumps(folder_structure, indent=4)
        absolute_path = os.path.abspath(output_file)  # Get the absolute path
        if output_file.endswith(".json"):
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(content)
        elif output_file.endswith(".txt"):
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(content)
        else:
            # Default to TXT if no extension is given
            absolute_path += ".txt"
            with open(f"{output_file}.txt", "w", encoding="utf-8") as f:
                f.write(content)
        logging.info(f"Output successfully written to '{absolute_path}'")
        print(f"Output written to '{absolute_path}'.")
    except Exception as e:
        logging.error(f"Error writing to output file '{output_file}': {e}")


# Class representing a tree node (directory or file)
class TreeNode(urwid.WidgetWrap):
    def __init__(self, file, is_selected=False, depth=0):
        self.file = file
        self.depth = depth
        symbol = "+" if file["type"] == "directory" else "-"
        display_name = f"{'|   ' * depth}{symbol} {file['name']}"
        self.attr_map = urwid.AttrMap(
            urwid.Text(display_name),
            "selected" if is_selected else "normal",
            focus_map="focus",
        )
        super().__init__(self.attr_map)

    def selectable(self):
        return True

    def update_state(self, is_selected):
        logging.info(f"Updating state for: {self.file['name']} - {'Selected' if is_selected else 'Deselected'}")
        self.attr_map.set_attr_map({"normal": "selected" if is_selected else "normal"})

# Generate the tree structure recursively
def generate_tree_structure(folder_structure, selected_files, depth=0):
    logging.info(f"Generating tree structure at depth: {depth}")
    rows = []
    for item in folder_structure.get("items", []):
        rows.append(TreeNode(item, item in selected_files, depth))
        if item["type"] == "directory":
            rows.extend(generate_tree_structure(item, selected_files, depth + 1))
    return rows

# Interactive terminal UI using urwid
class FileSelector:
    def __init__(self, folder_structure):
        logging.info("Initializing FileSelector UI")
        self.folder_structure = folder_structure
        self.selected_files = []
        self.palette = [
            ("normal", "default", "default"),
            ("focus", "light gray", "dark blue"),
            ("selected", "light green", "default"),
        ]
        self.rows = generate_tree_structure(folder_structure, self.selected_files)
        self.walker = urwid.SimpleFocusListWalker(self.rows)
        self.listbox = urwid.ListBox(self.walker)
        self.view = urwid.Frame(
            self.listbox,
            footer=urwid.Text("Use arrow keys to navigate, Space or click to toggle, Enter to submit, Q to quit."),
        )

    def toggle_selection(self, index):
        """
        Toggle selection for the given row index.
        If it's a folder, select/deselect all items within it.
        """
        logging.info(f"Toggling selection for index: {index}")
        file = self.rows[index].file

        if file["type"] == "directory":
            # Select/deselect all items recursively in the directory
            if file in self.selected_files:
                self.deselect_all_in_folder(file)
            else:
                self.select_all_in_folder(file)
        else:
            # Toggle individual file selection
            if file in self.selected_files:
                self.selected_files.remove(file)
            else:
                self.selected_files.append(file)

        self.rows[index].update_state(file in self.selected_files)

    def select_all_in_folder(self, folder):
        """
        Select all files and subfolders within a folder recursively.
        """
        if folder not in self.selected_files:
            self.selected_files.append(folder)

        for item in folder.get("items", []):
            if item["type"] == "directory":
                self.select_all_in_folder(item)
            elif item not in self.selected_files:
                self.selected_files.append(item)

    def deselect_all_in_folder(self, folder):
        """
        Deselect all files and subfolders within a folder recursively.
        """
        if folder in self.selected_files:
            self.selected_files.remove(folder)

        for item in folder.get("items", []):
            if item["type"] == "directory":
                self.deselect_all_in_folder(item)
            elif item in self.selected_files:
                self.selected_files.remove(item)

    def main(self):
        logging.info("Starting the FileSelector UI main loop")

        def unhandled_input(key):
            logging.info(f"Unhandled input: {key}")
            if key in ("q", "Q"):
                logging.info("Quitting the application")
                raise urwid.ExitMainLoop()
            if key == " ":
                focus_widget, focus_index = self.listbox.get_focus()
                if focus_index is not None:
                    self.toggle_selection(focus_index)
                self.update_footer()
            elif key == "enter":
                logging.info("Submitting selected files")
                raise urwid.ExitMainLoop()

        urwid.MainLoop(self.view, self.palette, unhandled_input=unhandled_input).run()

    def update_footer(self):
        selected_names = ", ".join([file["name"] for file in self.selected_files])
        logging.info(f"Updating footer with selected files: {selected_names}")
        self.view.footer = urwid.Text(f"Selected: {selected_names}")


# Main function
def main():
    parser = argparse.ArgumentParser(description="Map directory contents and embed selected file content into JSON.")
    parser.add_argument(
        "-d", "--directory",
        default=os.getcwd(),  # Default to the current working directory
        help="The root directory to scan (default: current directory)."
    )
    parser.add_argument(
        "-o", "--output",
        default="output.txt",  # Default output format is .txt
        help="The output file (default: output.txt)."
    )
    parser.add_argument(
        "-e", "--exclude",
        nargs="*",
        default=["node_modules", ".git"],  # Default exclusions
        help="Directories to exclude from the scan (default: 'node_modules', '.git')."
    )
    args = parser.parse_args()

    try:
        logging.info("Application started")
        root_directory = args.directory
        logging.info(f"Target directory: {root_directory}")
        logging.info(f"Excluding directories: {args.exclude}")
        folder_structure = get_folder_structure(root_directory, args.exclude)
        if not folder_structure:
            logging.error("Error: Could not retrieve folder structure.")
            return

        selector = FileSelector(folder_structure)
        selector.main()

        if selector.selected_files:
            embed_selected_contents(folder_structure, selector.selected_files)
            save_output(folder_structure, args.output)
        else:
            logging.info("No files selected.")
            print("No files selected.")
    except Exception as e:
        logging.error(f"Unhandled exception: {e}", exc_info=True)
        print("An error occurred. Check 'file_selector.log' for details.")

if __name__ == "__main__":
    main()
