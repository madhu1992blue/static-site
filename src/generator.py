import os
import shutil

from markdown import markdown_to_html_node, extract_title
from pathlib import Path
def removeRecurse(path: str):
    print("Removing: ",path)
    if not os.path.exists(path):
        return
    if os.path.isfile(path):
        os.remove(path)
        return
    for e in os.listdir(path):
        removeRecurse(path + "/" + e)
    shutil.rmtree(path)
    


def copy(src: str, dest: str):
    for sc in os.listdir(src):
        if os.path.isdir(src+"/"+sc):
            os.mkdir(dest+"/"+sc)
            print("Copying Dir: ",src+"/"+sc, dest + "/"+sc)
            copy(src+"/"+sc, dest + "/"+sc)
        else:
            print("Copying: ",src+"/"+sc, dest + "/"+sc)
            shutil.copy(src+"/"+sc, dest+"/"+sc)
                
        
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path,"r") as md_file:
        md_contents = md_file.read()
    with open(template_path,"r") as template_file:
        template_contents = template_file.read()
    markdown_html = markdown_to_html_node(md_contents).to_html()
    title = extract_title(md_contents)

    rendered_html = template_contents.replace("{{ Title }}", title).replace("{{ Content }}", markdown_html)
    out_file_path = Path(dest_path)
    out_file_path.parent.mkdir(exist_ok=True, parents=True)
    out_file_path.write_text(rendered_html)
    
def generate_pages_recursive(dir_path_content:str, template_path: str, dest_dir_path: str):
    for path in os.listdir(dir_path_content):
        srcRelPath = dir_path_content+"/"+path
        destRelPath = dest_dir_path +"/"+path
        if os.path.isdir(srcRelPath):
            generate_pages_recursive(srcRelPath, template_path, destRelPath)
        else:
            if srcRelPath.endswith(".md"):
                destRelPath = destRelPath[:-2]+"html"
            generate_page(srcRelPath, template_path,destRelPath)