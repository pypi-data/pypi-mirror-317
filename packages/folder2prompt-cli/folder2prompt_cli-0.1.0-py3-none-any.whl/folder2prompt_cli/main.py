#!/usr/bin/env python

import os
import argparse
import fnmatch
from collections import defaultdict
import re

def is_ignored(filepath, gitignore_rules):
    """
    Checks if a filepath should be ignored based on gitignore-style rules.
    """
    for rule in gitignore_rules:
         try:
            # Convert gitignore rule to regex
            pattern = rule.replace(r'.', r'\.')  # Escape dots
            pattern = pattern.replace(r'*', '.*')   # Convert * to .*
            pattern = pattern.replace(r'?', '.')    # Convert ? to .
            pattern = pattern.replace(r'/$', r'(/.*)?$')  # Handle directory matches
            pattern = pattern.replace(r'^/', '^')   # Handle root-level matches

            # If the rule doesn't start with ^, it can match anywhere in the path
            if not pattern.startswith('^'):
               pattern = f'(^|/){pattern}'
            regex = re.compile(pattern)
            if regex.search(filepath):
                 return True
         except Exception:
             print(f"Error processing rule {rule} for path {filepath}. skipping")
             continue
    return False

def get_file_contents(filepath):
    """
    Reads and returns the content of a text file.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
         print(f"Error reading {filepath}: {e}")
         return None

def format_repo_contents(contents):
    """
    Formats the content of files into a structured string including a directory tree.
    """
    if not contents:
        return ""
    
    # Ensure contents is a list
    contents = list(contents)
    contents.sort(key=lambda item: item['path'])
    
    
    # Build a nested dictionary representing the directory structure
    tree = {}
    for item in contents:
      
      path_parts = item['path'].split(os.sep)
      current_level = tree
      for part_index, part in enumerate(path_parts):
          if part_index == 0 and part == '':
              part = './'
          if part not in current_level:
              current_level[part] = {} if part_index < len(path_parts) -1 else None
          current_level = current_level[part]

    # Format the directory tree recursively
    def format_directory_tree(node, prefix=''):
        output = ''
        items = list(node.items())
        for index, (name, child_node) in enumerate(items):
            is_last_item = index == len(items) - 1
            line_prefix = '└── ' if is_last_item else '├── '
            child_prefix = '    ' if is_last_item else '│   '
            output += f'{prefix}{line_prefix}{name}\n'
            if isinstance(child_node, dict):
                output += format_directory_tree(child_node, f'{prefix}{child_prefix}')
        return output
    
    index_output = format_directory_tree(tree)
    text = ""
    for item in contents:
        text += f"\n\n---\nFile: {item['path']}\n---\n\n{item['content']}\n"

    return f"Directory Structure:\n\n{index_output}\n{text}"

def process_directory(directory_path, exclude_patterns, exclude_recursive_patterns, all_files=False, tree_only=False):
    """
    Processes all files in the given directory and its subdirectories.
    """
    all_contents = []
    gitignore_content = ['.git/**']
    for root, dirs, files in os.walk(directory_path):
        # Check and filter directories before processing files
        dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), exclude_recursive_patterns)]
        
        for file in files:
            filepath = os.path.join(root, file)
            relative_path = os.path.relpath(filepath, directory_path)

            if is_ignored(relative_path, gitignore_content):
                 continue
          
            if any(fnmatch.fnmatch(relative_path, pattern) for pattern in exclude_patterns):
                continue

            is_dir = os.path.isdir(filepath)
            
            if is_dir is False and any(fnmatch.fnmatch(relative_path, pattern) for pattern in exclude_recursive_patterns):
                continue
            if relative_path.endswith(".gitignore"):
                content = get_file_contents(filepath)
                if content:
                    lines = content.split('\n')
                    gitignore_path = relative_path.split(os.sep)[:-1]
                    gitignore_path = "/".join(gitignore_path) if gitignore_path else ""

                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if gitignore_path:
                                gitignore_content.append(f"{gitignore_path}/{line}")
                            else:
                              gitignore_content.append(line)
            elif is_dir is False or all_files is True:
                if not tree_only: # only read files if the tree option is not set.
                    content = get_file_contents(filepath)
                    if content is not None:
                        all_contents.append({
                        'path': relative_path,
                        'content': content
                    })
                else:
                  all_contents.append({'path':relative_path,'content': ""}) # this will just keep the path without reading its content.

    return all_contents


def main():
    parser = argparse.ArgumentParser(description='Convert files in a directory to a text output')
    parser.add_argument('directory', type=str, help='Path to the directory')
    parser.add_argument('--all', action='store_true', help='Include files within subdirectories regardless of exclusion')
    parser.add_argument('--exclude', type=str, default='[]', help='Exclude patterns from root, comma separated')
    parser.add_argument('--exclude-recursive', type=str, default='[]', help='Exclude patterns from subfolders, comma separated')
    parser.add_argument('--output', type=str, default='prompt.txt', help='Output file name (default: prompt.txt)')
    parser.add_argument('--tree', action='store_true', help='Output only the directory tree')


    args = parser.parse_args()

    exclude_patterns = eval(args.exclude)
    exclude_recursive_patterns = eval(args.exclude_recursive)
    directory_path = args.directory
    all_files = args.all
    output_file = args.output
    tree_only = args.tree

    if not isinstance(exclude_patterns, list) or not isinstance(exclude_recursive_patterns, list):
       print("Exclude options must be list.")
       return

    if not os.path.isdir(directory_path):
        print(f"Error: '{directory_path}' is not a valid directory path.")
        return
    
    print(f"Processing '{directory_path}'...")
    contents = process_directory(directory_path, exclude_patterns, exclude_recursive_patterns, all_files, tree_only)
    formatted_text = format_repo_contents(contents)
    
    if formatted_text:
      try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(formatted_text)
            print(f"Successfully written to {output_file}")
      except Exception as e:
        print(f"Error writing output to file {output_file}: {e}")


if __name__ == "__main__":
    main()