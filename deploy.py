import os
import subprocess
import shutil
import re
from urllib.parse import urlparse

# Page title from action input
PAGE_TITLE = os.getenv('INPUT_PAGE_TITLE', 'Documentation')

BASE_DIR = os.path.abspath(".")              # 源码根目录
SITE_DIR = os.path.join(BASE_DIR, "_site")   # 站点根目录

# 支持 action.yml 中的输入参数
IMAGE_SRC = os.path.join(BASE_DIR, os.getenv('INPUT_IMAGE_SRC', "Images"))
image_dst_input = os.getenv('INPUT_IMAGE_DST', "Images")
IMAGE_DST = os.path.join(BASE_DIR, image_dst_input) if not os.path.isabs(image_dst_input) else image_dst_input

ROBOT_SRC = os.path.join(BASE_DIR, os.getenv('INPUT_ROBOT_SRC', "robots.txt"))
ROBOT_DST = os.path.join(SITE_DIR, "robots.txt")
ICONS_SRC = os.path.join(BASE_DIR, os.getenv('INPUT_ICONS_SRC', "favicon.jpg"))
ICONS_DST = os.path.join(SITE_DIR, "favicon.jpg")
ICONS_LNK = "favicon.jpg"
INDEX_SRC = os.path.join(BASE_DIR, "index.html")
INDEX_DST = os.path.join(SITE_DIR, "index.html")

# EX_DIR 处理
EX_DIRS = ['_site', '.git', '.github']
ex_dir_input = os.getenv('INPUT_EX_DIR', '')
if ex_dir_input:
    EX_DIRS.extend([d.strip() for d in ex_dir_input.split(',') if d.strip()])

def init_site_dir():
    if os.path.exists(SITE_DIR):
        shutil.rmtree(SITE_DIR)
    os.makedirs(SITE_DIR, exist_ok=True)

def copy_images():
    if os.path.exists(IMAGE_SRC):
        shutil.copytree(IMAGE_SRC, IMAGE_DST, dirs_exist_ok=True)
        print("[INFO] Images copied successfully.")

def copy_robot():
    if os.path.exists(ROBOT_SRC):
        shutil.copy(ROBOT_SRC, ROBOT_DST)
        print("[INFO] <robots.txt> copied successfully.")

def copy_icons():
    if os.path.exists(ICONS_SRC):
        shutil.copy(ICONS_SRC, ICONS_DST)
        print("[INFO] <favicon.jpg> copied successfully.")

def copy_index():
    if os.path.exists(INDEX_SRC):
        shutil.copy(INDEX_SRC, INDEX_DST)
        print("[INFO] <index.html> copied successfully.")

def mk_parent(filename):
    parent_dir = os.path.dirname(filename)
    os.makedirs(parent_dir, exist_ok=True)

def modify_links(html_content):
    pattern = r'href=(["\'])([^"\']+?)\.md(?:([?#][^"\']*))?\1'
    
    def replacer(match):
        quote = match.group(1)
        path = match.group(2)
        suffix = match.group(3) or ''
        
        parsed = urlparse(path)
        if parsed.scheme or parsed.netloc:
            return match.group(0)
            
        return f'href={quote}{path}.html{suffix}{quote}'

    updated = re.sub(pattern, replacer, html_content, flags=re.IGNORECASE)
    return updated

def main():
    init_site_dir()

    copy_images()
    copy_robot()
    copy_icons()
    copy_index()

    print("[INFO] START CONVERSION")
    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if d not in EX_DIRS]
        
        for file in files:
            if file.endswith(".md"):
                md_path = os.path.join(root, file)
                
                rel_path = os.path.relpath(md_path, start=BASE_DIR)
                rel_no_ext = os.path.splitext(rel_path)[0]                
                dest_html = os.path.join(SITE_DIR, rel_no_ext + ".html")
                
                mk_parent(dest_html)
                print(f"[INFO] Processing: {rel_path} -> {os.path.relpath(dest_html, BASE_DIR)}")
                
                subprocess.run([
                    "pandoc", md_path, 
                    "-s", "--metadata", 
                    f"title={PAGE_TITLE}", 
                    "-o", dest_html], 
                    check=True)
                
                with open(dest_html, "r", encoding="utf-8") as f:
                    content = f.read()
                updated_content = modify_links(content)
                with open(dest_html, "w", encoding="utf-8") as f:
                    f.write(updated_content)

    print("[INFO] CONVERSION END")

if __name__ == "__main__":
    main()