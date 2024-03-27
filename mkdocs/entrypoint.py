import argparse
import os
import re
import subprocess  # nosec B404

import yaml


def read_header(markdown_file_path):
    """Reads the first header of a Markdown file and returns its content.

    Parameters:
    - markdown_file_path (str): The path to the Markdown file.

    Returns:
    - str: The content of the first header found in the file. If no header is found,
           an empty string is returned.
    """
    header_pattern = re.compile(r"^\s*#\s*(.+)", re.MULTILINE)

    try:
        with open(markdown_file_path, encoding="utf-8") as md_file:
            file_content = md_file.read()
            match = header_pattern.search(file_content)
            if match:
                return match.group(1).strip()
    except FileNotFoundError:
        print(f"The file {markdown_file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while reading the file {markdown_file_path}: {e}")

    return ""


def generate_nav_structure(start_path, parent_path=None, is_root=True):
    """Recursively generates a MkDocs navigation structure from the directory and files under
    start_path."""
    nav_structure = []
    if parent_path is None:
        parent_path = start_path
    dirs = [
        d
        for d in os.listdir(start_path)
        if os.path.isdir(os.path.join(start_path, d)) and not d.startswith(".")
    ]
    md_files = [
        f
        for f in os.listdir(start_path)
        if os.path.isfile(os.path.join(start_path, f))
        and f.endswith(".md")
        and not f.startswith(".")
    ]
    md_files.sort()
    dirs.sort()

    # Handle the Home page differently by checking if it's the root call
    if is_root and md_files:
        home_file = md_files.pop(0)  # Remove and return the first markdown file to use as "Home"
        relative_path = os.path.relpath(os.path.join(start_path, home_file), parent_path)
        nav_structure.append({"Home": relative_path})
        is_root = False

    for md_file in md_files:
        relative_path = os.path.relpath(os.path.join(start_path, md_file), parent_path)
        file_without_ext = md_file.replace(".md", "")
        # Only add as dict if filename does not match dirname
        if file_without_ext != os.path.basename(start_path):
            nav_structure.append({file_without_ext: relative_path})
        else:
            nav_structure.append({"index": relative_path})

    for dir in dirs:
        dir_path = os.path.join(start_path, dir)
        header = read_header(os.path.join(start_path, dir, f"{dir.split('/')[-1]}.md"))
        dir_nav = generate_nav_structure(dir_path, parent_path, is_root=False)
        if dir_nav:
            if header != "":
                nav_structure.append({f"'{header}'": dir_nav})
            else:
                nav_structure.append({dir: dir_nav})

    return nav_structure


def update_mkdocs_nav(mkdocs_yml_path, nav_structure):
    """Updates the mkdocs.yml file with the generated navigation structure."""
    with open(mkdocs_yml_path) as file:
        mkdocs_config = yaml.safe_load(file)

    mkdocs_config["theme"]["nav"] = nav_structure

    with open(mkdocs_yml_path, "w") as file:
        yaml.safe_dump(mkdocs_config, file, default_flow_style=False, sort_keys=False)


def main(
    mkdocs_yml_path,
    mkdocs_content_path,
    mkdocs_site_name,
    mkdocs_site,
    mkdocs_interface,
    mkdocs_port,
    generate,
):
    if generate:
        # Generate navigation structure from content path
        nav_structure = generate_nav_structure(mkdocs_content_path)
        print(nav_structure)

        with open(mkdocs_yml_path) as file:
            mkdocs_yml_content = file.read()
        # Replace the placeholders with actual values
        mkdocs_yml_content = mkdocs_yml_content.replace("MKDOCS_SITE_NAME", mkdocs_site_name)
        mkdocs_yml_content = mkdocs_yml_content.replace("MKDOCS_SITE", mkdocs_site)
        mkdocs_yml_content = mkdocs_yml_content.replace("MKDOCS_INTERFACE", mkdocs_interface)
        mkdocs_yml_content = mkdocs_yml_content.replace("MKDOCS_PORT", mkdocs_port)

        # Write the updated content back to mkdocs.yml
        with open(mkdocs_yml_path, "w") as file:
            file.write(mkdocs_yml_content)
        # Update mkdocs.yml with the navigation structure
        update_mkdocs_nav(mkdocs_yml_path, nav_structure)

    # Serve the MkDocs site
    subprocess.run(["mkdocs", "serve"], check=True)  # nosec B603, B607


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process MkDocs environment variables.")
    parser.add_argument("--mkdocs_yml_path", "-p", default="/app/mkdocs.yml")
    parser.add_argument("--mkdocs_content_path", "-mp", default="/app/docs")
    parser.add_argument(
        "--mkdocs_author", "-ma", default=os.environ.get("MKDOCS_AUTHOR", "CodeTriarii")
    )
    parser.add_argument("--mkdocs_site_name", default=os.environ.get("MKDOCS_SITE_NAME", "mkdocs"))
    parser.add_argument(
        "--mkdocs_site", default=os.environ.get("MKDOCS_SITE", "https://example.com")
    )
    parser.add_argument(
        "--mkdocs_interface", default=os.environ.get("MKDOCS_INTERFACE", "127.0.0.1")
    )
    parser.add_argument("--mkdocs_port", default=os.environ.get("MKDOCS_PORT", "8000"))
    parser.add_argument("--generate", "-g", default=True, type=bool)

    args = parser.parse_args()

    main(
        args.mkdocs_yml_path,
        args.mkdocs_content_path,
        args.mkdocs_site_name,
        args.mkdocs_site,
        args.mkdocs_interface,
        args.mkdocs_port,
        args.generate,
    )
