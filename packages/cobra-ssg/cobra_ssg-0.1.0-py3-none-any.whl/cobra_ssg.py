import os
import markdown
import frontmatter
import shutil
from cobra_utils import get_file_list, get_folder_list

def cobra_render(source_folder = 'content', build_folder = 'build'):
    layouts_folder = 'layouts'
    css_folder_source = f"{source_folder}/{layouts_folder}/css"
    css_folder_target = f"{build_folder}/css"
    js_folder_source = f"{source_folder}/{layouts_folder}/js"
    js_folder_target = f"{build_folder}/js"
    layouts_full_path = os.path.join(source_folder, layouts_folder)
    blocks_full_path = os.path.join(layouts_full_path, 'blocks')
    content_tag = '<cobra_ssg_content>'

    # Create the folder structure
    os.mkdir(build_folder)
    folders_to_copy = get_folder_list(path=source_folder, ignore_folders=[layouts_folder])
    for folder in folders_to_copy:
        os.mkdir(build_folder+folder)

    # Copy the css files
    shutil.copytree(css_folder_source, css_folder_target)

    # Copy the js files
    shutil.copytree(js_folder_source, js_folder_target)

    # Load layouts
    layouts = []
    layouts_to_load = [layout for layout in get_file_list(path=layouts_full_path, ignore_folders=["blocks"]) if os.path.splitext(layout)[1] != '.css']
    if not len(layouts_to_load):
        raise Exception(f"No layouts found in {layouts_full_path}")
    for layout in layouts_to_load:
        with open(layouts_full_path+layout, 'r', encoding='utf-8') as layout_content:
            name = os.path.splitext(layout)[0].lstrip('/')
            layouts.append({'name': name, 'content': layout_content.read()})

    # Load blocks
    blocks = []
    blocks_to_load = [block for block in get_file_list(path=blocks_full_path)]
    for block in blocks_to_load:
        with open(blocks_full_path+block, 'r', encoding='utf-8') as block_content:
            tag = f"<block_{os.path.splitext(block)[0].lstrip('/')}>"
            blocks.append({'tag': tag, 'content': block_content.read()})

    # insert the blocks into the layouts
    for layout in layouts:
        for block in blocks:
            if block["tag"] in layout["content"]:
                layout["content"] = layout["content"].replace(block["tag"], block["content"])

    # Convert markdown to html and copies the file in the build folder
    content_files_to_copy = get_file_list(path=source_folder, ignore_folders=[layouts_folder, "css", "blocks", "js"])
    if not len(content_files_to_copy):
        raise Exception(f"No files found in {source_folder}")
    for file in content_files_to_copy:
        html_file_content = ''
        backtracks = max(file.count("/") - 1, 0)
        global_css_string = f"<link rel=\"stylesheet\" href=\"{backtracks*'../'}css/global.css\">"
        global_js_string = f"<script src=\"{backtracks*'../'}js/global.js\" defer></script>"
        with open(source_folder+file, 'r', encoding='utf-8') as f:
            try:
                file_content_raw = f.read()
                page_frontmatter, file_content = frontmatter.parse(file_content_raw)
                layout_name = page_frontmatter.get("layout", "default")
                layout = next((layout for layout in layouts if layout["name"] == layout_name), None)
                html_page_content = markdown.markdown(file_content)
                html_file_content = layout['content'].replace(content_tag, html_page_content)
                # Insert global css path
                if "</head>" in html_file_content:
                    html_file_content = html_file_content.replace('</head>', f'\n{global_css_string}\n{global_js_string}\n</head>')
            except Exception as e:
                print(f"Error converting to html: {str(e)}")

        file_without_ext = os.path.splitext(build_folder+file)[0]
        with open(file_without_ext, 'w', encoding="utf-8", errors="xmlcharrefreplace") as f:
            f.write(html_file_content)

