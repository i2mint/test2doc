"""Miscellaneous functions for test2doc."""

from typing import Callable
import os
import json
from pathlib import Path
from dol import Pipe


load_json = Pipe(Path, lambda x: x.read_text(), json.loads)

Filepath = str


def rename_file(
    file: Filepath,
    renamer_function: Callable[[Filepath], Filepath],
    *,
    dry_run: bool = True,
    verbose: bool = True,
):
    """
    This function takes a list of files and renames them using the provided renamer function.
    """
    if not isinstance(file, str):
        files = file
        for file in files:
            rename_file(file, renamer_function, dry_run=dry_run, verbose=verbose)

    new_name = renamer_function(file)
    if verbose:
        print(f"Renaming {file} to {new_name}")
    if not dry_run:
        os.rename(file, new_name)


def renamer_function(filepath: Filepath) -> Filepath:
    d = load_json(filepath)
    title = d['title']
    # separate folder and filename
    folder, filename = os.path.split(filepath)
    # separate filename and extension
    name, ext = os.path.splitext(filename)
    # add title at the end of filenmae
    new_filename = f"{name} -- {title}{ext}"
    # return the new filepath
    return os.path.join(folder, new_filename)


import re
from collections import Counter
from typing import Callable


def _header_to_anchor_base(header):
    from hashlib import md5

    # Normalize the header to generate a consistent anchor
    normalized = re.sub(r'\s+', '-', header.lower().strip())
    # Hash the normalized header for a short and unique anchor
    return md5(normalized.encode()).hexdigest()[:8]


def _generate_anchor_name(
    header,
    existing_anchors,
    *,
    header_to_anchor_base: Callable = _header_to_anchor_base,
):
    """
    Generates a unique anchor name by hashing the header text.
    If the anchor already exists, append a number to ensure uniqueness.
    """
    anchor_base = header_to_anchor_base(header)

    # If this base is already used, append a number to make it unique
    i = existing_anchors.get(anchor_base, 0)
    existing_anchors[anchor_base] = i + 1
    anchor_name = f"{anchor_base}-{i}" if i > 0 else anchor_base

    return anchor_name


def add_toc_to_markdown(md_text):
    """
    This function takes markdown text as input and returns markdown text
    with a clickable table of contents based on the headers in the text.

    Note: In some cases, the function screws up the markdown.
    So whatever you do, make a backup if replacing the original.
    For more robust solutions, seach a more complete package, or use a service
    (for example, https://derlin.github.io/bitdowntoc/)

    """
    # Find existing anchors to avoid duplicates
    existing_anchors = Counter(re.findall(r'<a name="(.+?)"></a>', md_text))

    # Find all headers in the markdown text
    headers = re.findall(r'^(#+) (.+)$', md_text, re.MULTILINE)

    # Generate table of contents
    toc = ['# Table of contents']
    anchors = {}
    for header_level, header_text in headers:
        level = len(header_level)  # Determine the header level by count of #
        anchor_name = _generate_anchor_name(header_text, anchors)

        # Add the header with its anchor link to the TOC
        toc.append(f"{'    ' * (level - 1)}- [{header_text}](#{anchor_name})")

        # Add the anchor to the markdown text if not already present
        anchor_tag = f'<a name="{anchor_name}"></a>'
        if anchor_tag not in md_text:
            md_text = md_text.replace(
                f'{header_level} {header_text}',
                f'{header_level} {header_text} {anchor_tag}',
                1,
            )

        # Track the anchor names
        anchors[anchor_name] = True

    # Insert the table of contents after the first header (usually the title)
    toc_str = '\n'.join(toc) + '\n\n'
    split_md_text = re.split(r'(#+ .+)', md_text, 1)
    md_text_with_toc = split_md_text[0] + toc_str + ''.join(split_md_text[1:])

    return md_text_with_toc


def markdown_to_pdf(markdown_text):
    """
    This function takes a markdown text and converts it to a PDF.

    This is a very basic function. For more, look for a more complete package or use
    a service (e.g. https://www.pdfforge.org/online/en/markdown-to-pdf)
    """
    import markdown2
    from weasyprint import HTML

    html_text = markdown2.markdown(markdown_text)
    pdf_bytes = HTML(string=html_text).write_pdf()
    return pdf_bytes
