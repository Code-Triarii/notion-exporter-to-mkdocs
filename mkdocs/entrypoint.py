import argparse
import os
import subprocess
import yaml

def generate_nav_structure(start_path):
    """
    Generates a MkDocs navigation structure from the directory and files under start_path.
    The first .md file found is taken as the "Home" page.
    """
    nav_structure = []
    home_added = False
    for root, dirs, files in os.walk(start_path):
        # Sort directories and files to ensure consistent order
        dirs.sort()
        files.sort()
        # Ignore hidden files and directories
        files = [f for f in files if not f.startswith('.')]
        dirs = [d for d in dirs if not d.startswith('.')]
        # Construct relative paths for markdown files
        md_files = [os.path.join(root, f) for f in files if f.endswith('.md')]
        md_files_relative = [os.path.relpath(f, start_path) for f in md_files]
        if not home_added and md_files_relative:
            nav_structure.append({'Home': md_files_relative[0]})
            md_files_relative = md_files_relative[1:]
            home_added = True
        section_name = os.path.basename(root) if root != start_path else None
        if section_name:
            section = {section_name: md_files_relative}
            if md_files_relative:
                nav_structure.append(section)
    return nav_structure

def update_mkdocs_nav(mkdocs_yml_path, nav_structure):
    """
    Updates the mkdocs.yml file with the generated navigation structure.
    """
    with open(mkdocs_yml_path) as file:
        mkdocs_config = yaml.safe_load(file)
    
    mkdocs_config['nav'] = nav_structure
    
    with open(mkdocs_yml_path, 'w') as file:
        yaml.safe_dump(mkdocs_config, file, default_flow_style=False, sort_keys=False)

def main(mkdocs_yml_path, mkdocs_content_path, mkdocs_site_name, mkdocs_site, mkdocs_interface, mkdocs_port):
    # Generate navigation structure from content path
    nav_structure = generate_nav_structure(mkdocs_content_path)
    print(nav_structure)
    
    with open(mkdocs_yml_path, 'r') as file:
        mkdocs_yml_content = file.read()
    
    # Replace the placeholders with actual values
    mkdocs_yml_content = mkdocs_yml_content.replace('MKDOCS_SITE_NAME', mkdocs_site_name)
    mkdocs_yml_content = mkdocs_yml_content.replace('MKDOCS_SITE', mkdocs_site)
    mkdocs_yml_content = mkdocs_yml_content.replace('MKDOCS_INTERFACE', mkdocs_interface)
    mkdocs_yml_content = mkdocs_yml_content.replace('MKDOCS_PORT', mkdocs_port)
    
    # Write the updated content back to mkdocs.yml
    with open(mkdocs_yml_path, 'w') as file:
        file.write(mkdocs_yml_content)
    # Update mkdocs.yml with the navigation structure
    update_mkdocs_nav(mkdocs_yml_path, nav_structure)
    
    # Serve the MkDocs site
    subprocess.run(['mkdocs', 'serve'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process MkDocs environment variables.')
    parser.add_argument('--mkdocs_yml_path', '-p', default='/app/mkdocs.yml')
    parser.add_argument('--mkdocs_content_path', '-mp', default='/app/docs')
    parser.add_argument('--mkdocs_site_name', default=os.environ.get('MKDOCS_SITE_NAME', 'mkdocs'))
    parser.add_argument('--mkdocs_site', default=os.environ.get('MKDOCS_SITE', 'https://example.com'))
    parser.add_argument('--mkdocs_interface', default=os.environ.get('MKDOCS_INTERFACE', '0.0.0.0'))
    parser.add_argument('--mkdocs_port', default=os.environ.get('MKDOCS_PORT', '8000'))
    
    args = parser.parse_args()
    
    main(args.mkdocs_yml_path, args.mkdocs_content_path, args.mkdocs_site_name, args.mkdocs_site, args.mkdocs_interface, args.mkdocs_port)
