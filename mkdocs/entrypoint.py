import argparse
import os
import subprocess
import yaml

def generate_nav_structure(start_path, parent_path=None):
    """
    Recursively generates a MkDocs navigation structure from the directory and files under start_path.
    """
    nav_structure = []
    if parent_path is None:
        parent_path = start_path

    dirs = [d for d in os.listdir(start_path) if os.path.isdir(os.path.join(start_path, d)) and not d.startswith('.')]
    md_files = [f for f in os.listdir(start_path) if os.path.isfile(os.path.join(start_path, f)) and f.endswith('.md') and not f.startswith('.')]

    md_files.sort()
    dirs.sort()

    for md_file in md_files:
        relative_path = os.path.relpath(os.path.join(start_path, md_file), parent_path)
        if 'Home' not in [list(item.keys())[0] for item in nav_structure]:
            nav_structure.append({relative_path.split("/")[-1].split(".")[0]: relative_path})
        else:
            nav_structure.append({md_file.replace('.md', ''): relative_path})

    for dir in dirs:
        dir_path = os.path.join(start_path, dir)
        dir_nav = generate_nav_structure(dir_path, parent_path)
        if dir_nav:
            nav_structure.append({dir: dir_nav})

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
