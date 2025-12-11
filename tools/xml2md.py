#!/usr/bin/env python3

# Copyright (C) Nginx, Inc.

"""
XML to Markdown converter for nginx.org documentation.

This script converts nginx.org XML documentation files to Markdown format,
preserving the document structure and making the content more accessible
for various uses (GitHub, static site generators, etc.).
"""

import sys
import os
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional, List, TextIO


class XML2MarkdownConverter:
    """Converts nginx.org XML documentation to Markdown format."""
    
    def __init__(self):
        self.in_list = False
        self.list_level = 0
        self.current_indent = ""
        
    def convert_file(self, xml_path: Path, output_path: Optional[Path] = None) -> str:
        """Convert a single XML file to Markdown."""
        try:
            # Parse XML file with entity resolution
            parser = ET.XMLParser()
            # Define common HTML entities used in nginx.org docs
            parser.entity['mdash'] = '—'
            parser.entity['nbsp'] = ' '
            parser.entity['rsquo'] = "'"
            parser.entity['ldquo'] = '"'
            parser.entity['rdquo'] = '"'
            parser.entity['laquo'] = '«'
            parser.entity['raquo'] = '»'
            parser.entity['ndash'] = '–'
            parser.entity['copy'] = '©'
            parser.entity['reg'] = '®'
            parser.entity['trade'] = '™'
            parser.entity['hellip'] = '…'
            parser.entity['times'] = '×'
            parser.entity['gt'] = '>'
            parser.entity['lt'] = '<'
            parser.entity['amp'] = '&'
            parser.entity['quot'] = '"'
            parser.entity['apos'] = "'"
            
            tree = ET.parse(xml_path, parser=parser)
            root = tree.getroot()
            
            # Generate markdown content
            markdown = self._convert_root(root)
            
            # Write to output file if specified
            if output_path:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(markdown)
                print(f"✓ Converted: {xml_path} -> {output_path}")
            
            return markdown
            
        except ET.ParseError as e:
            print(f"✗ Error parsing {xml_path}: {e}", file=sys.stderr)
            return ""
        except Exception as e:
            print(f"✗ Error converting {xml_path}: {e}", file=sys.stderr)
            return ""
    
    def _convert_root(self, root: ET.Element) -> str:
        """Convert the root element (article or module)."""
        output = []
        
        # Extract metadata
        title = root.get('name', 'Untitled')
        lang = root.get('lang', 'en')
        author = root.get('author')
        editor = root.get('editor')
        translator = root.get('translator')
        rev = root.get('rev')
        
        # Add title
        output.append(f"# {title}\n")
        
        # Add metadata
        metadata = []
        if author:
            metadata.append(f"**Author:** {author}")
        if editor:
            metadata.append(f"**Editor:** {editor}")
        if translator:
            metadata.append(f"**Translator:** {translator}")
        if rev:
            metadata.append(f"**Revision:** {rev}")
        if lang:
            metadata.append(f"**Language:** {lang}")
        
        if metadata:
            output.append("  \n".join(metadata))
            output.append("\n")
        
        # Convert sections
        for element in root:
            output.append(self._convert_element(element, level=2))
        
        return "\n".join(output)
    
    def _convert_element(self, element: ET.Element, level: int = 2) -> str:
        """Convert an XML element to Markdown."""
        tag = element.tag
        
        if tag == 'section':
            return self._convert_section(element, level)
        elif tag == 'para':
            return self._convert_para(element)
        elif tag == 'list':
            return self._convert_list(element)
        elif tag == 'programlisting':
            return self._convert_programlisting(element)
        elif tag == 'example':
            return self._convert_example(element)
        elif tag == 'note':
            return self._convert_note(element)
        elif tag == 'table':
            return self._convert_table(element)
        else:
            # For unhandled elements, try to extract text
            return self._extract_text(element)
    
    def _convert_section(self, element: ET.Element, level: int) -> str:
        """Convert a section element."""
        output = []
        
        # Add section header
        section_name = element.get('name')
        section_id = element.get('id')
        
        if section_name:
            header = "#" * level + f" {section_name}"
            if section_id:
                header += f" {{#{section_id}}}"
            output.append(header + "\n")
        
        # Convert section content
        for child in element:
            output.append(self._convert_element(child, level + 1))
        
        return "\n".join(output)
    
    def _convert_para(self, element: ET.Element) -> str:
        """Convert a paragraph element."""
        text = self._process_inline_elements(element)
        return text.strip() + "\n" if text.strip() else ""
    
    def _process_inline_elements(self, element: ET.Element) -> str:
        """Process inline elements and text within a parent element."""
        result = []
        
        # Add element's text
        if element.text:
            result.append(element.text)
        
        # Process children
        for child in element:
            if child.tag == 'link':
                result.append(self._convert_link(child))
            elif child.tag == 'literal':
                text = self._get_text(child)
                result.append(f"`{text}`")
            elif child.tag == 'command':
                text = self._get_text(child)
                result.append(f"`{text}`")
            elif child.tag == 'path':
                text = self._get_text(child)
                result.append(f"`{text}`")
            elif child.tag == 'value':
                text = self._get_text(child)
                result.append(f"*{text}*")
            elif child.tag == 'var':
                text = self._get_text(child)
                result.append(f"*{text}*")
            elif child.tag == 'i':
                text = self._get_text(child)
                result.append(f"*{text}*")
            elif child.tag == 'b':
                text = self._get_text(child)
                result.append(f"**{text}**")
            elif child.tag == 'nobr':
                result.append(self._get_text(child))
            elif child.tag == 'br':
                result.append("  \n")
            elif child.tag == 'list':
                result.append("\n" + self._convert_list(child))
            elif child.tag == 'programlisting':
                result.append("\n" + self._convert_programlisting(child))
            elif child.tag == 'example':
                result.append("\n" + self._convert_example(child))
            elif child.tag == 'note':
                result.append("\n" + self._convert_note(child))
            elif child.tag == 'table':
                result.append("\n" + self._convert_table(child))
            elif child.tag == 'header':
                text = self._get_text(child)
                result.append(f"**{text}**")
            elif child.tag == 'registered':
                text = self._get_text(child)
                result.append(f"{text}®")
            elif child.tag == 'http-status':
                code = child.get('code', '')
                text = child.get('text', '')
                if text:
                    result.append(f"{code} {text}")
                else:
                    result.append(code)
            else:
                # Generic text extraction
                result.append(self._get_text(child))
            
            # Add tail text
            if child.tail:
                result.append(child.tail)
        
        return "".join(result)
    
    def _convert_link(self, element: ET.Element) -> str:
        """Convert a link element."""
        text = self._get_text(element) or ""
        url = element.get('url')
        doc = element.get('doc')
        link_id = element.get('id')
        
        if url:
            return f"[{text}]({url})"
        elif doc:
            # Convert doc reference to relative link
            if link_id:
                return f"[{text}]({doc}#{link_id})"
            else:
                # Convert .xml to .html or .md depending on context
                doc_link = doc.replace('.xml', '.html')
                if text:
                    return f"[{text}]({doc_link})"
                else:
                    return f"[{doc_link}]({doc_link})"
        else:
            # Just text, no actual link
            return text if text else ""
    
    def _convert_list(self, element: ET.Element) -> str:
        """Convert a list element."""
        list_type = element.get('type', 'bullet')
        output = []
        
        if list_type == 'bullet':
            for i, item in enumerate(element.findall('listitem')):
                text = self._process_inline_elements(item).strip()
                output.append(f"- {text}")
        elif list_type == 'enum':
            for i, item in enumerate(element.findall('listitem'), 1):
                text = self._process_inline_elements(item).strip()
                output.append(f"{i}. {text}")
        elif list_type == 'tag':
            # Definition list
            for i in range(0, len(element), 2):
                if i + 1 < len(element):
                    tag_name = element[i]
                    tag_desc = element[i + 1]
                    
                    if tag_name.tag == 'tag-name':
                        name_text = self._process_inline_elements(tag_name).strip()
                        desc_text = self._process_inline_elements(tag_desc).strip()
                        output.append(f"**{name_text}**  ")
                        output.append(f"  {desc_text}")
        
        return "\n".join(output) + "\n"
    
    def _convert_programlisting(self, element: ET.Element) -> str:
        """Convert a programlisting element (code block)."""
        text = self._get_text(element).strip()
        return f"```\n{text}\n```\n"
    
    def _convert_example(self, element: ET.Element) -> str:
        """Convert an example element (code block)."""
        text = self._get_text(element).strip()
        return f"```\n{text}\n```\n"
    
    def _convert_note(self, element: ET.Element) -> str:
        """Convert a note element."""
        text = self._process_inline_elements(element).strip()
        return f"> **Note:** {text}\n"
    
    def _convert_table(self, element: ET.Element) -> str:
        """Convert a table element."""
        # Basic table support - may need enhancement
        rows = []
        max_cols = 0
        
        for tr in element.findall('.//tr'):
            cells = []
            for td in tr.findall('td'):
                cell_text = self._process_inline_elements(td).strip()
                cells.append(cell_text)
            if cells:
                rows.append("| " + " | ".join(cells) + " |")
                max_cols = max(max_cols, len(cells))
        
        if len(rows) > 0 and max_cols > 0:
            # Add header separator after first row
            separator = "| " + " | ".join(["---"] * max_cols) + " |"
            rows.insert(1, separator)
        
        return "\n".join(rows) + "\n" if rows else ""
    
    def _get_text(self, element: ET.Element) -> str:
        """Extract all text from an element and its children."""
        return "".join(element.itertext())
    
    def _extract_text(self, element: ET.Element) -> str:
        """Extract text from an unknown element."""
        return self._process_inline_elements(element)


def find_xml_files(directory: Path, lang: Optional[str] = None) -> List[Path]:
    """Find all XML files in a directory."""
    pattern = "*.xml"
    
    if lang:
        # Filter by language in path
        all_files = list(directory.rglob(pattern))
        # Only keep files that have the language code in their path
        filtered_files = [f for f in all_files if f'/{lang}/' in str(f) or f'\\{lang}\\' in str(f)]
        return filtered_files
    else:
        # Search all XML files
        return list(directory.rglob(pattern))


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Convert nginx.org XML documentation to Markdown format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert a single file
  %(prog)s xml/en/index.xml -o output/index.md
  
  # Convert all files in a directory
  %(prog)s xml/en/docs/ -o output/docs/
  
  # Convert all English documentation
  %(prog)s xml/ -o output/ --lang en
  
  # Convert and print to stdout
  %(prog)s xml/en/index.xml
        """
    )
    
    parser.add_argument(
        'input',
        type=str,
        help='Input XML file or directory'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output file or directory (default: stdout for single file, ./markdown/ for directories)'
    )
    
    parser.add_argument(
        '--lang',
        type=str,
        help='Filter by language (e.g., en, ru, cn)'
    )
    
    parser.add_argument(
        '--preserve-structure',
        action='store_true',
        help='Preserve directory structure in output'
    )
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"Error: Input path '{input_path}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    converter = XML2MarkdownConverter()
    
    # Handle single file conversion
    if input_path.is_file():
        if args.output:
            output_path = Path(args.output)
            converter.convert_file(input_path, output_path)
        else:
            # Print to stdout
            markdown = converter.convert_file(input_path)
            print(markdown)
    
    # Handle directory conversion
    elif input_path.is_dir():
        xml_files = find_xml_files(input_path, args.lang)
        
        if not xml_files:
            print("No XML files found", file=sys.stderr)
            sys.exit(1)
        
        output_dir = Path(args.output) if args.output else Path("markdown")
        
        print(f"Found {len(xml_files)} XML files to convert")
        
        for xml_file in xml_files:
            # Determine output path
            if args.preserve_structure:
                # Preserve relative directory structure
                rel_path = xml_file.relative_to(input_path)
                output_path = output_dir / rel_path.with_suffix('.md')
            else:
                # Flatten structure
                output_path = output_dir / xml_file.with_suffix('.md').name
            
            converter.convert_file(xml_file, output_path)
        
        print(f"\n✓ Conversion complete! Output written to: {output_dir}")
    
    else:
        print(f"Error: '{input_path}' is neither a file nor a directory", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
