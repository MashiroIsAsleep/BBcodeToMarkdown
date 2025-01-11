import re
import sys
import os

def bbcode_to_markdown(bbcode_text):
    """
    Convert a BBCode string into a Markdown string.
    """

    # ------------------------------------------------------------------
    # 1) Convert [url=<LINK>]<TEXT>[/url] to [TEXT](LINK)
    #    Use a regex that captures:
    #       1) the URL in group(1)
    #       2) the link text in group(2)
    # ------------------------------------------------------------------
    pattern_url_with_text = re.compile(r'\[url=(.*?)\](.*?)\[/url\]', re.IGNORECASE | re.DOTALL)
    bbcode_text = pattern_url_with_text.sub(r'[\2](\1)', bbcode_text)

    # ------------------------------------------------------------------
    # 2) Convert [url]<LINK>[/url] to <LINK> or [LINK](LINK)
    #    For a pure link without description, you might want:
    #       - `<LINK>` (simple angle bracket)
    #       - or `[LINK](LINK)` (full Markdown link)
    # ------------------------------------------------------------------
    pattern_url_plain = re.compile(r'\[url\](.*?)\[/url\]', re.IGNORECASE | re.DOTALL)
    # Uncomment the style you prefer:
    #bbcode_text = pattern_url_plain.sub(r'<\1>', bbcode_text)          # e.g. <https://example.com>
    bbcode_text = pattern_url_plain.sub(r'[\1](\1)', bbcode_text)       # e.g. [https://example.com](https://example.com)

    # ------------------------------------------------------------------
    # 3) Convert [b]...[/b] to **...**
    # ------------------------------------------------------------------
    pattern_bold = re.compile(r'\[b\](.*?)\[/b\]', re.IGNORECASE | re.DOTALL)
    bbcode_text = pattern_bold.sub(r'**\1**', bbcode_text)

    # ------------------------------------------------------------------
    # 4) Convert [i]...[/i] to *...*
    # ------------------------------------------------------------------
    pattern_italic = re.compile(r'\[i\](.*?)\[/i\]', re.IGNORECASE | re.DOTALL)
    bbcode_text = pattern_italic.sub(r'*\1*', bbcode_text)

    # ------------------------------------------------------------------
    # 5) Convert [u]...[/u] to <u>...</u>
    #    Markdown doesn’t support underline natively, so we use HTML.
    # ------------------------------------------------------------------
    pattern_underline = re.compile(r'\[u\](.*?)\[/u\]', re.IGNORECASE | re.DOTALL)
    bbcode_text = pattern_underline.sub(r'<u>\1</u>', bbcode_text)

    # ------------------------------------------------------------------
    # 6) Convert [size=<SIZE>]...[/size] to <span style="font-size:SIZE;">...</span>
    #    Markdown has no built-in font size, so we use inline HTML/CSS.
    # ------------------------------------------------------------------
    pattern_size = re.compile(r'\[size=(.*?)\](.*?)\[/size\]', re.IGNORECASE | re.DOTALL)
    bbcode_text = pattern_size.sub(r'<span style="font-size:\1;">\2</span>', bbcode_text)

    # ------------------------------------------------------------------
    # 7) Convert [img]<LINK>[/img] to ![image](LINK)
    #    If you want a placeholder alt text, you can do: ![Alt Text](LINK)
    # ------------------------------------------------------------------
    pattern_img = re.compile(r'\[img\](.*?)\[/img\]', re.IGNORECASE | re.DOTALL)
    bbcode_text = pattern_img.sub(r'![image](\1)', bbcode_text)

    return bbcode_text


def main():
    if len(sys.argv) < 2:
        print("Usage: bbcode_to_md.py <path_to_bbcode_file>")
        sys.exit(1)

    input_path = sys.argv[1]

    if not os.path.isfile(input_path):
        print(f"Error: File '{input_path}' does not exist.")
        sys.exit(1)
    with open(input_path, 'r', encoding='utf-8') as f:
        bbcode_content = f.read()
    markdown_content = bbcode_to_markdown(bbcode_content)
    base_name, _ = os.path.splitext(input_path)
    output_path = base_name + ".md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"Conversion complete: '{output_path}'")


if __name__ == "__main__":
    main()
