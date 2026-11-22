# test2doc.misc

Miscellaneous functions for test2doc.

### Functions

| [`add_toc_to_markdown`](#test2doc.misc.add_toc_to_markdown)(md_text)                   | This function takes markdown text as input and returns markdown text with a clickable table of contents based on the headers in the text.   |
|-------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| [`markdown_to_pdf`](#test2doc.misc.markdown_to_pdf)(markdown_text)                 | This function takes a markdown text and converts it to a PDF.                                                                               |
| [`rename_file`](#test2doc.misc.rename_file)(file, renamer_function, \*[, ...]) | This function takes a list of files and renames them using the provided renamer function.                                                   |
| `renamer_function`(filepath)                                                                    |                                                                                                                                             |

### test2doc.misc.add_toc_to_markdown(md_text)

This function takes markdown text as input and returns markdown text
with a clickable table of contents based on the headers in the text.

#### NOTE
In some cases, the function screws up the markdown.
So whatever you do, make a backup if replacing the original.
For more robust solutions, seach a more complete package, or use a service
(for example, [https://derlin.github.io/bitdowntoc/](https://derlin.github.io/bitdowntoc/))

### test2doc.misc.markdown_to_pdf(markdown_text)

This function takes a markdown text and converts it to a PDF.

This is a very basic function. For more, look for a more complete package or use
a service (e.g. [https://www.pdfforge.org/online/en/markdown-to-pdf](https://www.pdfforge.org/online/en/markdown-to-pdf))

### test2doc.misc.rename_file(file, renamer_function, , dry_run=True, verbose=True)

This function takes a list of files and renames them using the provided renamer function.
