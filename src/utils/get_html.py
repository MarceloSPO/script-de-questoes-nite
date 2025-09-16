from pathlib import Path

def get_html_page():
    src_path = Path(__file__).resolve().parent.parent    
    html_file_path = src_path / "templates" / "index.html"

    with open(html_file_path, "r", encoding="utf-8") as f:
        html = f.read()
    return html