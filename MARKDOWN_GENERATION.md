# Markdown Generation Guide

This document describes how to generate Markdown documentation from nginx.org XML sources.

## Overview

The nginx.org repository includes a Python-based tool (`tools/xml2md.py`) that converts XML documentation to Markdown format. This makes the documentation more accessible for:

- GitHub repositories and wikis
- Static site generators (Jekyll, Hugo, MkDocs, etc.)
- Documentation platforms (GitBook, Read the Docs, etc.)
- Easy reading and editing in text editors
- Version control diffs that are easier to read

## Quick Start

### Generate English Documentation

```bash
make markdown
```

This will create a `markdown/` directory with all English documentation converted to Markdown format.

### Generate All Documentation

```bash
make markdown-all
```

This converts documentation from all languages.

## Make Targets

The following Make targets are available:

| Target | Description |
|--------|-------------|
| `make markdown` | Generate English documentation (default) |
| `make markdown-en` | Generate English documentation |
| `make markdown-ru` | Generate Russian documentation |
| `make markdown-all` | Generate all documentation (all languages) |
| `make markdown-clean` | Remove generated markdown files |
| `make help-markdown` | Show markdown generation help |

## Using xml2md.py Directly

For more control, you can use the `xml2md.py` tool directly:

### Convert a Single File

```bash
# Print to stdout
python3 tools/xml2md.py xml/en/index.xml

# Save to a file
python3 tools/xml2md.py xml/en/index.xml -o output/index.md
```

### Convert a Directory

```bash
# Convert all XML files in a directory, preserving structure
python3 tools/xml2md.py xml/en/docs/ -o markdown/docs/ --preserve-structure

# Convert without preserving structure (flatten)
python3 tools/xml2md.py xml/en/docs/ -o markdown/docs/
```

### Filter by Language

```bash
# Convert only English documentation
python3 tools/xml2md.py xml/ -o markdown/ --lang en --preserve-structure
```

## Command-Line Options

```
usage: xml2md.py [-h] [-o OUTPUT] [--lang LANG] [--preserve-structure] input

Convert nginx.org XML documentation to Markdown format

positional arguments:
  input                 Input XML file or directory

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file or directory (default: stdout for single
                        file, ./markdown/ for directories)
  --lang LANG           Filter by language (e.g., en, ru, cn)
  --preserve-structure  Preserve directory structure in output
```

## Supported XML Elements

The converter supports all major nginx.org XML elements:

### Structure Elements
- `<article>`, `<module>` - Document root elements
- `<section>` - Document sections with headings
- `<para>` - Paragraphs

### Text Formatting
- `<literal>`, `<command>`, `<path>` - Inline code
- `<value>`, `<var>`, `<i>` - Italic text
- `<b>`, `<header>` - Bold text
- `<br>` - Line breaks
- `<nobr>` - No-break text

### Lists
- `<list type="bullet">` - Bullet lists
- `<list type="enum">` - Numbered lists
- `<list type="tag">` - Definition lists

### Code and Examples
- `<programlisting>` - Code blocks
- `<example>` - Example code blocks

### Links
- `<link url="...">` - External links
- `<link doc="...">` - Internal document links

### Other Elements
- `<note>` - Note blocks (rendered as blockquotes)
- `<table>` - Tables (basic support)

### HTML Entities

Common HTML entities are supported:
- `&mdash;` (—), `&ndash;` (–)
- `&nbsp;` (non-breaking space)
- `&times;` (×)
- `&copy;` (©), `&reg;` (®), `&trade;` (™)
- `&hellip;` (…)
- Standard entities: `&lt;`, `&gt;`, `&amp;`, `&quot;`, `&apos;`

## Examples

### Example 1: Convert Main Documentation

```bash
# Convert all English documentation
make markdown-en

# Result: markdown/en/ contains all converted files
ls markdown/en/
# index.md  download.md  docs/  ...
```

### Example 2: Convert Single Article

```bash
# Convert the beginner's guide
python3 tools/xml2md.py xml/en/docs/beginners_guide.xml -o beginners_guide.md

# View the result
cat beginners_guide.md
```

### Example 3: Convert Module Documentation

```bash
# Convert HTTP module documentation
python3 tools/xml2md.py xml/en/docs/http/ -o markdown/http/ --preserve-structure

# Result: markdown/http/ contains all HTTP module docs
ls markdown/http/
# ngx_http_core_module.md  ngx_http_proxy_module.md  ...
```

## Output Quality

The converter produces high-quality Markdown that:

- Preserves document structure with proper heading levels
- Maintains code blocks with syntax highlighting support
- Converts links appropriately (internal and external)
- Handles complex nested structures
- Preserves metadata (author, editor, revision, language)
- Maintains lists (bullet, numbered, definition)
- Properly formats inline code and emphasis

## Troubleshooting

### Missing Entities

If you encounter errors about undefined entities, the converter may need to be updated to include additional HTML entities. The entity definitions are in the `convert_file()` method in `tools/xml2md.py`.

### Conversion Errors

If a file fails to convert, the error will be displayed but other files will continue to be processed. Check the error message for details.

### Empty Links

Some internal document references may appear as empty links `[]()` if they don't have link text in the XML. This is typically for cross-references where the link text is implied.

## Integration with Other Tools

### Using with Static Site Generators

The generated Markdown can be used with popular static site generators:

#### Jekyll
```bash
make markdown-en
cp -r markdown/en/* _posts/
bundle exec jekyll serve
```

#### Hugo
```bash
make markdown-en
cp -r markdown/en/* content/
hugo server
```

#### MkDocs
```bash
make markdown-en
# Add files to mkdocs.yml navigation
mkdocs serve
```

### Using with Documentation Platforms

The Markdown files can be imported into:
- GitBook
- Read the Docs (with Sphinx + recommonmark)
- Docusaurus
- VuePress

## Development

### Adding Support for New Elements

To add support for a new XML element:

1. Add a handler method in the `XML2MarkdownConverter` class
2. Call the handler from `_convert_element()` or `_process_inline_elements()`
3. Test with documents that use the element

### Adding New Entities

To support additional HTML entities:

1. Add the entity to the parser configuration in `convert_file()`
2. Format: `parser.entity['entityname'] = 'character'`

## Contributing

Improvements to the XML to Markdown converter are welcome! Consider:

- Better table support (column alignment, complex tables)
- Support for additional XML elements
- Output format options (GitHub-flavored Markdown, CommonMark, etc.)
- Integration with CI/CD pipelines
- Automated testing of conversion quality

## See Also

- [README.md](README.md) - Main repository documentation
- [xml/en/docs/](xml/en/docs/) - Source XML documentation
- [dtd/](dtd/) - Document Type Definitions
