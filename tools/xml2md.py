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
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional, List


def convert_text(text):
    """Convert text content, handling special characters."""
    if not text:
        return ""
    # Keep entities as-is since they're already resolved by the parser
    return text


def process_inline(elem):
    """Process inline elements."""
    result = []
    tag = elem.tag
    
    if tag == "literal":
        text = elem.text or ""
        text = convert_text(text).strip()
        result.append(f"`{text}`")
    
    elif tag == "command":
        text = elem.text or ""
        text = convert_text(text).strip()
        result.append(f"`{text}`")
    
    elif tag == "path":
        text = elem.text or ""
        text = convert_text(text).strip()
        result.append(f"`{text}`")
    
    elif tag == "value":
        text = elem.text or ""
        text = convert_text(text).strip()
        result.append(f"`{text}`")
    
    elif tag == "var":
        text = elem.text or ""
        text = convert_text(text).strip()
        result.append(f"`{text}`")
    
    elif tag == "link":
        text = elem.text or ""
        text = convert_text(text).strip()
        
        # If no direct text, check for child elements
        if not text and len(elem) > 0:
            text_parts = []
            for child in elem:
                text_parts.extend(process_inline(child))
                if child.tail:
                    text_parts.append(convert_text(child.tail.strip()))
            text = "".join(text_parts)
        
        # If still no text, try to use the id attribute as text
        if not text:
            text = elem.get("id", "")
        
        url = elem.get("url", elem.get("doc", ""))
        link_id = elem.get("id", "")
        
        # Build URL with fragment if id is present
        if url and link_id and not url.endswith(f"#{link_id}"):
            url = f"{url}#{link_id}"
        elif not url and link_id:
            # Internal reference
            url = f"#{link_id}"
        
        if url and text:
            result.append(f"[{text}]({url})")
        elif text:
            result.append(f"`{text}`")
        else:
            result.append("")
    
    elif tag == "header":
        text = elem.text or ""
        text = convert_text(text).strip()
        result.append(f"`{text}`")
    
    elif tag == "c-func":
        text = elem.text or ""
        text = convert_text(text).strip()
        result.append(f"`{text}()`")
    
    elif tag == "emphasis" or tag == "i":
        text = elem.text or ""
        text = convert_text(text).strip()
        result.append(f"*{text}*")
    
    elif tag == "b":
        text = elem.text or ""
        text = convert_text(text).strip()
        result.append(f"**{text}**")
    
    elif tag == "nobr":
        text_parts = []
        if elem.text:
            text_parts.append(convert_text(elem.text))
        for child in elem:
            text_parts.extend(process_inline(child))
            if child.tail:
                text_parts.append(convert_text(child.tail))
        result.append("".join(text_parts))
    
    elif tag == "commercial_version":
        text = elem.text or "commercial subscription"
        text = convert_text(text).strip()
        result.append(f"[{text}](https://nginx.com/products/)")
    
    elif tag == "http-status":
        code = elem.get("code", "")
        text = elem.get("text", elem.text or "")
        if code and text:
            result.append(f"{code} {text}")
        elif code:
            result.append(code)
        elif text:
            result.append(text)
    
    elif tag == "registered":
        text = elem.text or ""
        result.append(f"{text}®")
    
    elif tag == "para":
        # Nested paragraph (inline)
        text_parts = []
        if elem.text and elem.text.strip():
            text_parts.append(convert_text(elem.text.strip()))
        
        for child in elem:
            text_parts.extend(process_inline(child))
            if child.tail and child.tail.strip():
                text_parts.append(convert_text(child.tail.strip()))
        
        result.append(" ".join(text_parts))
    
    elif tag == "list":
        # Handle nested lists inline
        result.append("\n")
        for item in process_element(elem, 0, set()):
            result.append(item)
    
    else:
        # Unknown inline element, just get text
        text = elem.text or ""
        text = convert_text(text)
        if text:
            result.append(text)
    
    return result


def process_element(elem, level=0, processed_inline=None):
    """Recursively process XML elements and convert to Markdown."""
    if processed_inline is None:
        processed_inline = set()
    
    result = []
    tag = elem.tag
    
    if tag in ["article", "module"]:
        # Article or module title
        name = elem.get("name", "")
        if name:
            result.append(f"# {name}\n\n")
        
        # Add metadata if present
        metadata = []
        author = elem.get("author")
        editor = elem.get("editor")
        translator = elem.get("translator")
        rev = elem.get("rev")
        lang = elem.get("lang")
        
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
            result.append("  \n".join(metadata))
            result.append("\n\n")
        
        for child in elem:
            result.extend(process_element(child, level, processed_inline))
    
    elif tag == "section":
        # Section heading
        name = elem.get("name", "")
        section_id = elem.get("id", "")
        heading_level = level + 1
        if heading_level > 6:
            heading_level = 6
        
        if name:
            header = "#" * heading_level + f" {name}"
            if section_id:
                header += f" {{#{section_id}}}"
            result.append(header + "\n\n")
        
        # Process section content - handle text and children together
        for child in elem:
            result.extend(process_element(child, heading_level, processed_inline))
    
    elif tag == "para":
        # Paragraph - may contain mixed content: text, inline elements, block elements
        children_list = list(elem)
        has_block_children = any(child.tag in ["list", "programlisting", "example", "note"] for child in children_list)
        
        if has_block_children:
            # Mixed content paragraph - process in order, tracking which elements are block vs inline
            # Collect inline content before first block element
            text_parts = []
            if elem.text and elem.text.strip():
                text_parts.append(convert_text(elem.text.strip()))
            
            i = 0
            while i < len(children_list):
                child = children_list[i]
                
                if child.tag in ["list", "programlisting", "example", "note"]:
                    # Before processing block element, collect any preceding inline elements
                    # (this handles inline elements that come before the first block)
                    if i == 0 or (i > 0 and children_list[i-1].tag not in ["list", "programlisting", "example", "note"]):
                        # Find all inline elements before this block
                        j = 0
                        while j < i:
                            if children_list[j].tag not in ["list", "programlisting", "example", "note"]:
                                # Only process if we haven't already
                                if id(children_list[j]) not in processed_inline:
                                    inline_parts = process_inline(children_list[j])
                                    text_parts.extend(inline_parts)
                                    if children_list[j].tail and children_list[j].tail.strip():
                                        text_parts.append(convert_text(children_list[j].tail.strip()))
                                    processed_inline.add(id(children_list[j]))
                            j += 1
                    
                    # Output accumulated text before block element
                    if text_parts:
                        para_text = " ".join(text_parts)
                        para_text = re.sub(r'\s+', ' ', para_text)
                        result.append(f"{para_text}\n\n")
                        text_parts = []
                    
                    # Process block element
                    result.extend(process_element(child, level, processed_inline))
                    
                    # After block element, collect following inline content until next block
                    if child.tail and child.tail.strip():
                        text_parts.append(convert_text(child.tail.strip()))
                    
                    # Collect inline siblings
                    j = i + 1
                    while j < len(children_list) and children_list[j].tag not in ["list", "programlisting", "example", "note"]:
                        inline_child = children_list[j]
                        inline_parts = process_inline(inline_child)
                        text_parts.extend(inline_parts)
                        if inline_child.tail and inline_child.tail.strip():
                            text_parts.append(convert_text(inline_child.tail.strip()))
                        processed_inline.add(id(inline_child))
                        j += 1
                    
                    # Output collected inline content as paragraph (if any)
                    if text_parts:
                        para_text = " ".join(text_parts)
                        para_text = re.sub(r'\s+', ' ', para_text)
                        result.append(f"{para_text}\n\n")
                        text_parts = []
                    
                    # Skip to after the inline elements we just processed
                    i = j
                else:
                    # Inline element - will be processed when we hit the next block
                    i += 1
        else:
            # Regular paragraph with only inline content
            text_parts = []
            if elem.text:
                text = elem.text.strip()
                if text:
                    text_parts.append(convert_text(text))
            
            for child in children_list:
                inline_parts = process_inline(child)
                text_parts.extend(inline_parts)
                if child.tail:
                    tail = child.tail.strip()
                    if tail:
                        text_parts.append(convert_text(tail))
            
            if text_parts:
                # Join parts with single space and normalize whitespace
                para_text = " ".join(text_parts)
                para_text = re.sub(r'\s+', ' ', para_text)
                result.append(f"{para_text}\n\n")
    
    elif tag == "list":
        # List
        list_type = elem.get("type", "bullet")
        counter = 1
        
        # Handle tag lists (definition lists with tag-name and tag-desc)
        if list_type == "tag":
            for child in elem:
                if child.tag == "tag-name":
                    # Process tag-name as a subheading or bold text
                    result.extend(process_element(child, level, processed_inline))
                elif child.tag == "tag-desc":
                    # Process tag-desc content
                    result.extend(process_element(child, level, processed_inline))
            return result
        
        for child in elem:
            if child.tag == "listitem":
                item_parts = []
                if child.text and child.text.strip():
                    item_parts.append(convert_text(child.text.strip()))
                
                for subchild in child:
                    if subchild.tag in ["literal", "link", "header", "c-func", "var", "path", "value", "command", "i", "b", "nobr"]:
                        item_parts.extend(process_inline(subchild))
                    else:
                        # Handle nested elements
                        nested = process_element(subchild, level + 1, processed_inline)
                        if nested:
                            # If we have item text already, add newline
                            if item_parts:
                                result.append(f"- {' '.join(item_parts)}\n")
                                item_parts = []
                            # Add nested content with indentation
                            for line in nested:
                                result.append(f"  {line}")
                    
                    if subchild.tail and subchild.tail.strip():
                        item_parts.append(convert_text(subchild.tail.strip()))
                
                if item_parts:
                    if list_type == "bullet":
                        result.append(f"- {' '.join(item_parts)}\n")
                    else:
                        result.append(f"{counter}. {' '.join(item_parts)}\n")
                        counter += 1
        
        result.append("\n")
    
    elif tag in ["programlisting", "example"]:
        # Code block - may contain inline elements like emphasis
        code_parts = []
        if elem.text:
            code_parts.append(convert_text(elem.text))
        
        # Process inline children (like emphasis)
        for child in elem:
            if child.text:
                code_parts.append(convert_text(child.text))
            if child.tail:
                code_parts.append(convert_text(child.tail))
        
        code = "".join(code_parts)
        
        # Remove leading/trailing blank lines but preserve indentation
        lines = code.split("\n")
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        code = "\n".join(lines)
        
        result.append(f"```\n{code}\n```\n\n")
        
        # Note: tail text is handled by parent para element, not here
    
    elif tag == "note":
        # Note block
        text_parts = []
        if elem.text and elem.text.strip():
            text_parts.append(convert_text(elem.text.strip()))
        
        for child in elem:
            # Handle block children in notes
            if child.tag in ["list", "programlisting", "para"]:
                if text_parts:
                    result.append(f"> **Note:** {' '.join(text_parts)}\n>\n")
                    text_parts = []
                nested = process_element(child, level, processed_inline)
                for line in nested:
                    if line.strip():
                        result.append(f"> {line}")
            else:
                text_parts.extend(process_inline(child))
            
            if child.tail and child.tail.strip():
                text_parts.append(convert_text(child.tail.strip()))
        
        if text_parts:
            result.append(f"> **Note:** {' '.join(text_parts)}\n\n")
    
    elif tag == "tag-name":
        # Tag name in a tag list (usually parameter names)
        text_parts = []
        if elem.text and elem.text.strip():
            text_parts.append(convert_text(elem.text.strip()))
        
        for child in elem:
            text_parts.extend(process_inline(child))
            if child.tail and child.tail.strip():
                text_parts.append(convert_text(child.tail.strip()))
        
        tag_text = " ".join(text_parts)
        result.append(f"**{tag_text}**  \n")
    
    elif tag == "tag-desc":
        # Tag description - process text and children in order
        text_parts = []
        if elem.text and elem.text.strip():
            text_parts.append(convert_text(elem.text.strip()))
        
        for child in elem:
            # Check if it's a block element
            if child.tag in ["list", "programlisting", "example", "para", "note"]:
                # Output accumulated text first
                if text_parts:
                    result.append("  " + " ".join(text_parts) + "\n\n")
                    text_parts = []
                # Process block element
                result.extend(process_element(child, level, processed_inline))
                # Get tail text
                if child.tail and child.tail.strip():
                    text_parts.append(convert_text(child.tail.strip()))
            else:
                # Inline element
                text_parts.extend(process_inline(child))
                if child.tail and child.tail.strip():
                    text_parts.append(convert_text(child.tail.strip()))
        
        # Output remaining text
        if text_parts:
            result.append("  " + " ".join(text_parts) + "\n\n")
    
    elif tag == "directive":
        # Directive documentation
        name = elem.get("name", "")
        heading_level = level + 1
        if heading_level > 6:
            heading_level = 6
        
        result.append(f"{'#' * heading_level} {name}\n\n")
        
        # Collect syntax, default, context, and appeared-in for structured format
        directive_info = {}
        other_content = []
        
        for child in elem:
            if child.tag == "syntax":
                directive_info['syntax'] = child
            elif child.tag == "default":
                directive_info['default'] = child
            elif child.tag == "context":
                contexts = [child]
                # Collect all context elements
                for sibling in elem:
                    if sibling.tag == "context" and sibling != child:
                        contexts.append(sibling)
                directive_info['context'] = contexts
            elif child.tag == "appeared-in":
                directive_info['appeared-in'] = child
            elif child.tag != "context":  # Skip extra context elements as we collected them above
                other_content.append(child)
        
        # Output directive info in code block format
        if directive_info:
            result.append("```\n")
            
            if 'syntax' in directive_info:
                text_parts = []
                elem_syntax = directive_info['syntax']
                is_block = elem_syntax.get('block') == 'yes'
                
                if elem_syntax.text:
                    text_parts.append(convert_text(elem_syntax.text))
                for child in elem_syntax:
                    # Get plain text without markdown formatting for syntax display
                    if child.text:
                        text_parts.append(convert_text(child.text))
                    if child.tail:
                        text_parts.append(convert_text(child.tail))
                syntax_text = "".join(text_parts).strip()
                syntax_text = " ".join(syntax_text.split())
                
                # Add directive name and appropriate ending (block or semicolon)
                if is_block:
                    if syntax_text:
                        result.append(f"Syntax:  {name} {syntax_text} {{ ... }}\n")
                    else:
                        result.append(f"Syntax:  {name} {{ ... }}\n")
                else:
                    if syntax_text:
                        result.append(f"Syntax:  {name} {syntax_text};\n")
                    else:
                        result.append(f"Syntax:  {name};\n")
            
            if 'default' in directive_info:
                elem_default = directive_info['default']
                if elem_default.text and elem_default.text.strip():
                    text_parts = [convert_text(elem_default.text.strip())]
                    for child in elem_default:
                        if child.text:
                            text_parts.append(convert_text(child.text))
                        if child.tail:
                            text_parts.append(convert_text(child.tail.strip()))
                    default_text = " ".join(text_parts) if text_parts else ""
                else:
                    default_text = ""
                result.append(f"Default: {default_text}\n")
            else:
                result.append(f"Default: —\n")
            
            if 'context' in directive_info:
                context_texts = []
                for elem_context in directive_info['context']:
                    context_text = (elem_context.text or "").strip()
                    if context_text:
                        context_texts.append(context_text)
                result.append(f"Context: {', '.join(context_texts)}\n")
            
            result.append("```\n\n")
            
            if 'appeared-in' in directive_info:
                elem_appeared = directive_info['appeared-in']
                version_text = (elem_appeared.text or "").strip()
                result.append(f"*This directive appeared in version {version_text}.*\n\n")
        
        # Process other directive content
        for child in other_content:
            result.extend(process_element(child, heading_level, processed_inline))
    
    elif tag == "table":
        # Basic table support
        rows = []
        max_cols = 0
        
        for tr in elem.findall('.//tr'):
            cells = []
            for td in tr.findall('td'):
                cell_parts = []
                if td.text:
                    cell_parts.append(convert_text(td.text).strip())
                for child in td:
                    cell_parts.extend(process_inline(child))
                    if child.tail:
                        cell_parts.append(convert_text(child.tail).strip())
                cell_text = " ".join(cell_parts)
                cells.append(cell_text)
            if cells:
                rows.append("| " + " | ".join(cells) + " |")
                max_cols = max(max_cols, len(cells))
        
        if len(rows) > 0 and max_cols > 0:
            # Add header separator after first row
            separator = "| " + " | ".join(["---"] * max_cols) + " |"
            rows.insert(1, separator)
        
        if rows:
            result.append("\n".join(rows) + "\n\n")
    
    else:
        # For other elements, try to extract text
        if elem.text:
            result.append(convert_text(elem.text))
        for child in elem:
            result.extend(process_element(child, level, processed_inline))
            if child.tail:
                result.append(convert_text(child.tail))
    
    return result


def convert_file(xml_path: Path, output_path: Optional[Path] = None) -> str:
    """Convert a single XML file to Markdown."""
    try:
        # Read and preprocess XML to handle HTML entities
        xml_content = xml_path.read_text()
        
        # Replace common HTML entities with their Unicode equivalents
        entity_map = {
            '&mdash;': '—',
            '&ndash;': '–',
            '&nbsp;': ' ',
            '&ldquo;': '"',
            '&rdquo;': '"',
            '&lsquo;': ''',
            '&rsquo;': ''',
            '&hellip;': '…',
            '&times;': '×',
            '&copy;': '©',
            '&reg;': '®',
            '&trade;': '™',
            '&laquo;': '«',
            '&raquo;': '»',
        }
        
        for entity, replacement in entity_map.items():
            xml_content = xml_content.replace(entity, replacement)
        
        # Parse XML from string
        root = ET.fromstring(xml_content)
        
        # Convert to markdown
        markdown_lines = process_element(root)
        markdown = "".join(markdown_lines)
        
        # Clean up excessive blank lines
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)
        
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
    
    # Handle single file conversion
    if input_path.is_file():
        if args.output:
            output_path = Path(args.output)
            convert_file(input_path, output_path)
        else:
            # Print to stdout
            markdown = convert_file(input_path)
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
            
            convert_file(xml_file, output_path)
        
        print(f"\n✓ Conversion complete! Output written to: {output_dir}")
    
    else:
        print(f"Error: '{input_path}' is neither a file nor a directory", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
