import os, subprocess, shutil, re
from urllib.parse import urlparse
from jinja2 import Template

#region Global Variables
PAGE_TITLE = ""                                    # 页面标题
BASE_DIR = "";   SITE_DIR = ""                     # 源码根目录，站点根目录
IMAGE_SRC = "";  IMAGE_DST = ""                    # 图片 源目录、目标目录
INDEX_SRC = "";  INDEX_DST = "";  INDEX_TGT = ""   # index.html 源文件、目标文件、跳转文件
ROBOT_SRC = "";  ROBOT_DST = ""                    # robots.txt 源文件、目标文件            
ICONS_SRC = "";  ICONS_DST = "";  ICONS_LNK = ""   # 图标 源文件、目标文件、链接文件名
EX_DIRS = ['_site', '.git', '.github']             # 排除目录列表
NOJEKLLY = "";   ACTION_DIR = ""                   # .nojekyll 文件路径、Action根目录
MD_PATH = "";    DEST_HTML = ""                    # 处理过程中间变量
REL_PATH = "";   REL_NO_EXT = ""                   # 处理过程中间变量
#endregion

#region Prepare Resource
def init_path():
    global PAGE_TITLE
    PAGE_TITLE = os.getenv('INPUT_PAGE_TITLE', 'Documentation')

    global ACTION_DIR, BASE_DIR, SITE_DIR
    ACTION_DIR = os.getenv('GITHUB_ACTION_PATH', os.path.dirname(os.path.abspath(__file__)))
    BASE_DIR = os.path.abspath(".") 
    SITE_DIR = os.path.join(BASE_DIR, "_site")
    if os.path.exists(SITE_DIR): shutil.rmtree(SITE_DIR)
    os.makedirs(SITE_DIR, exist_ok=True)

    global IMAGE_SRC, IMAGE_DST
    IMAGE_SRC = os.path.join(BASE_DIR, os.getenv('INPUT_IMAGE_SRC', "Images"))
    IMAGE_DST = os.path.join(SITE_DIR, os.getenv('INPUT_IMAGE_DST', "Images"))

    global INDEX_SRC, INDEX_DST, INDEX_TGT
    INDEX_SRC = os.path.join(ACTION_DIR, "index.j2")
    INDEX_DST = os.path.join(SITE_DIR, "index.html")
    INDEX_TGT = os.getenv('INPUT_HOME_SRC', "./README.html")

    global ROBOT_SRC, ROBOT_DST
    ROBOT_SRC = os.path.join(BASE_DIR, os.getenv('INPUT_ROBOT_SRC', "robots.txt"))
    ROBOT_DST = os.path.join(SITE_DIR, "robots.txt")

    global ICONS_SRC, ICONS_DST, ICONS_LNK
    ICONS_SRC = os.path.join(BASE_DIR, os.getenv('INPUT_ICONS_SRC', "favicon.jpg"))
    ICONS_DST = os.path.join(SITE_DIR, "favicon.jpg")
    ICONS_LNK = os.path.basename(ICONS_DST)

    global NOJEKLLY
    NOJEKLLY = os.path.join(SITE_DIR, ".nojekyll") 

    global EX_DIRS
    ex_input = os.getenv('INPUT_EX_DIR', '')
    if ex_input: EX_DIRS.extend([d.strip() for d in ex_input.split(',') if d.strip()])

def copy_images():
    if os.path.exists(IMAGE_SRC):
        shutil.copytree(IMAGE_SRC, IMAGE_DST, dirs_exist_ok=True)
        print("[INFO] Images Copied Successfully.")
    else:
        print(f"[INFO] No {os.path.basename(IMAGE_SRC)} Directory Found to Copy.")

def copy_robot():
    if os.path.exists(ROBOT_SRC):
        shutil.copy(ROBOT_SRC, ROBOT_DST)
        print("[INFO] <robots.txt> Copied Successfully.")
    else:
        print(f"[INFO] No {os.path.basename(ROBOT_DST)} File Found to Copy.")

def copy_icons():
    if os.path.exists(ICONS_SRC):
        shutil.copy(ICONS_SRC, ICONS_DST)
        print("[INFO] <favicon.jpg> Copied Successfully.")
    else:
        print(f"[INFO] No {os.path.basename(ICONS_SRC)} File Found to Copy.")

def copy_index():
    if not os.path.exists(INDEX_SRC):
        print(f"[INFO] No {os.path.basename(INDEX_SRC)} Template Found.")
        return
    with open(INDEX_SRC, "r", encoding="utf-8") as f:
        template_content = f.read()
    template = Template(template_content)
    rendered = template.render(J2_TITLE=PAGE_TITLE, J2_INDEX=INDEX_TGT)
    os.makedirs(os.path.dirname(INDEX_DST), exist_ok=True)
    with open(INDEX_DST, "w", encoding="utf-8") as f:
        f.write(rendered)
    print("[INFO] <index.html> Rendered Successfully.")
#endregion

#region Process Markdown
def prepare_path(root, file):
    global MD_PATH, REL_PATH, REL_NO_EXT, DEST_HTML
    MD_PATH = os.path.join(root, file)
    REL_PATH = os.path.relpath(MD_PATH, start=BASE_DIR)
    REL_NO_EXT = os.path.splitext(REL_PATH)[0]
    DEST_HTML = os.path.join(SITE_DIR, REL_NO_EXT + ".html")

def mk_parent():
    parent_dir = os.path.dirname(DEST_HTML)
    os.makedirs(parent_dir, exist_ok=True)

def run_pandoc():
    subprocess.run(["pandoc", MD_PATH, "-s", "--metadata",
        f"title={PAGE_TITLE}", "-o", DEST_HTML], check=True)
    print(f"[INFO] Processed: {MD_PATH} -> {DEST_HTML}")

STYLE_CSS = ' alt="Logo" style="height: 1.5em; vertical-align: middle; margin-right: 10px;"'
def add_header_icon(html_content):    
    pattern = r'(<h1[^>]*class="title"[^>]*>)(.*?)(</h1>)'
    replacement = r'\1<img src="' + ICONS_LNK + '"' + STYLE_CSS + r'>\2\3'
    updated = re.sub(pattern, replacement, html_content, count=1, flags=re.IGNORECASE | re.DOTALL)
    return updated

def modify_links(html_content): 
    pattern = r'href=(["\'])([^"\']+?)\.md(?:([?#][^"\']*))?\1'
    def replacer(match):
        quote = match.group(1)          # 引号 (" 或 ')
        path = match.group(2)           # 路径主干 (filename)
        suffix = match.group(3) or ''   # 锚点或参数 (如 #header)，没有则为空字符串

        # 排除外部绝对链接（例如 http://github.com/xxx/file.md 不应该被修改）
        parsed = urlparse(path)
        if parsed.scheme or parsed.netloc:
            return match.group(0) # 原样返回，不作修改            
        return f'href={quote}{path}.html{suffix}{quote}'
    return re.sub(pattern, replacer, html_content, flags=re.IGNORECASE)

def add_favicon(html_content): 
    LINK_LINE = f'<link rel="icon" href="{ICONS_LNK}" type="image/jpeg">'
    if '<head>' in html_content:
        return re.sub(r'<head>', f'<head>\n    {LINK_LINE}',
            html_content, count=1, flags=re.IGNORECASE)
    else:
        return re.sub(r'<html[^>]*>', 
            lambda m: m.group(0) + f'\n<head>\n    {LINK_LINE}\n</head>',
            html_content, count=1, flags=re.IGNORECASE)
#endregion

def process_md(root, file):
    prepare_path(root, file)
    mk_parent()
    run_pandoc()
    content = open(DEST_HTML, "r", encoding="utf-8").read()
    content = add_header_icon(content)
    content = modify_links(content)
    content = add_favicon(content)
    open(DEST_HTML, "w", encoding="utf-8").write(content)

def walk_mdfile():
    print("[INFO] START CONVERTING ...")
    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if d not in EX_DIRS]
        [process_md(root, file) for file in files if file.endswith(".md")]
    print("[INFO] CONVERSION END")

def prepare_resource():
    copy_images()
    copy_robot()
    copy_icons()
    copy_index()

if __name__ == "__main__":
    init_path()
    prepare_resource()
    walk_mdfile()
    open(NOJEKLLY, "w").write("")
