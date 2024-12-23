from pathlib import Path
import shutil

from parser import markdown_to_html


def copy_dir(src, dest):
    src_path = Path(src)
    dest_path = Path(dest)

    if not src_path.exists() or not src_path.is_dir():
        raise ValueError(
            f"Source directory {src} does not exist or is not a directory."
        )

    if dest_path.exists():
        print(f"Clearing destination directory: {dest_path}")
        shutil.rmtree(dest_path)

    # Recreate the dest dir
    dest_path.mkdir(parents=True, exist_ok=True)
    print(f"Created destination directory: {dest_path}")

    def copy_rec(src: Path, dest: Path):
        for item in src.iterdir():
            src_item = src / item.name
            dest_item = dest / item.name

            if item.is_dir():
                print(f"Copying dir: {src_item} -> {dest_item}")
                dest_item.mkdir(parents=True, exist_ok=True)
                copy_rec(src_item, dest_item)
            else:
                print(f"Copying file: {src_item} -> {dest_item}")
                shutil.copy2(src_item, dest_item)

    copy_rec(src_path, dest_path)
    print("Copy complete!")


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found in markdown")


def generate_page(from_path, template_path, to_path):
    print(f"Generating page: {from_path} -> {to_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
        title = extract_title(markdown)
        print("title is ", title)
        with open(template_path, "r") as template:
            template_text = template.read()
            template_text = template_text.replace("{{ Title }}", title)
            template_text = template_text.replace(
                "{{ Content }}", markdown_to_html(markdown).to_html()
            )
            with open(to_path, "w") as out:
                out.write(template_text)


def main():
    copy_dir("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()
