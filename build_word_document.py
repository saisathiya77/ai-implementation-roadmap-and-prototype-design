# build_word_document.py
"""
Builds a professional, enterprise-grade Word Document (.docx and .doc)
from AI_Implementation_Roadmap_and_Prototype_Design.md
using python-docx with full styling, tables, borders, and typography.
"""

import sys
import os
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, color_hex):
    """Sets background shading of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets internal padding (in twips) for a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tc_pr.append(tcMar)

def set_table_borders(table, color="CBD5E1", sz="4", val="single"):
    """Applies subtle borders to a table."""
    tbl_pr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
            <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        </w:tblBorders>
    ''')
    tbl_pr.append(borders)

def add_callout(doc, text, title="STRATEGIC DIRECTIVE"):
    """Adds a stylish callout box with a colored left border and light shading."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=140)
    
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="1E3A8A"/>
            <w:top w:val="none"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    tc_pr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r_title = p.add_run(f"[{title}] ")
    r_title.bold = True
    r_title.font.size = Pt(9.5)
    r_title.font.color.rgb = RGBColor(30, 58, 138)
    
    r_text = p.add_run(text)
    r_text.font.size = Pt(9.5)
    r_text.font.color.rgb = RGBColor(30, 41, 59)
    
    doc.add_paragraph() # Spacing

def create_document():
    doc = Document()
    
    # Page Setup: Normal 1-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Header & Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Enterprise Cognitive Intelligence Platform (ECIP) | Architecture & Implementation Roadmap")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(148, 163, 184)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("CONFIDENTIAL - FOR INTERNAL STEERING COMMITTEE USE ONLY")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(148, 163, 184)
    
    # Read Markdown
    md_file = "AI_Implementation_Roadmap_and_Prototype_Design.md"
    if not os.path.exists(md_file):
        print(f"Error: {md_file} not found.")
        sys.exit(1)
        
    with open(md_file, "r", encoding="utf-8") as f:
        md_text = f.read()

    lines = md_text.splitlines()
    
    in_code = False
    code_lines = []
    in_table = False
    table_rows = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Code block handler
        if line.startswith("```"):
            if in_code:
                # Flush code block
                p = doc.add_paragraph()
                p.paragraph_format.space_before = Pt(4)
                p.paragraph_format.space_after = Pt(6)
                p.paragraph_format.line_spacing = 1.05
                
                # Container table for code block with shading
                tbl = doc.add_table(rows=1, cols=1)
                tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
                cell = tbl.cell(0, 0)
                cell.width = Inches(6.5)
                set_cell_background(cell, "F8FAFC")
                set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
                set_table_borders(tbl, color="CBD5E1", sz="4", val="single")
                
                cp = cell.paragraphs[0]
                cp.paragraph_format.space_before = Pt(2)
                cp.paragraph_format.space_after = Pt(2)
                cp.paragraph_format.line_spacing = 1.0
                
                code_text = "\n".join(code_lines)
                c_run = cp.add_run(code_text)
                c_run.font.name = "Consolas"
                c_run.font.size = Pt(8.0)
                c_run.font.color.rgb = RGBColor(15, 23, 42)
                
                doc.add_paragraph() # Spacing
                in_code = False
                code_lines = []
            else:
                in_code = True
                code_lines = []
            i += 1
            continue
            
        if in_code:
            code_lines.append(line)
            i += 1
            continue
            
        # Table handler
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            # Check if separator
            if all(re.match(r'^:?-+:?$', c) for c in cells if c):
                i += 1
                continue
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(cells)
            i += 1
            continue
        else:
            if in_table:
                # Render table
                if table_rows:
                    num_cols = max(len(r) for r in table_rows)
                    num_rows = len(table_rows)
                    tbl = doc.add_table(rows=num_rows, cols=num_cols)
                    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
                    set_table_borders(tbl, color="CBD5E1", sz="4", val="single")
                    
                    for r_idx, row in enumerate(table_rows):
                        for c_idx in range(num_cols):
                            cell = tbl.cell(r_idx, c_idx)
                            set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
                            cell_text = row[c_idx] if c_idx < len(row) else ""
                            
                            p = cell.paragraphs[0]
                            p.paragraph_format.space_before = Pt(1)
                            p.paragraph_format.space_after = Pt(1)
                            p.paragraph_format.line_spacing = 1.15
                            
                            run = p.add_run(cell_text)
                            run.font.name = "Calibri"
                            run.font.size = Pt(8.5)
                            
                            if r_idx == 0:
                                set_cell_background(cell, "1E3A8A")
                                run.font.color.rgb = RGBColor(255, 255, 255)
                                run.bold = True
                            else:
                                bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
                                set_cell_background(cell, bg_color)
                                # Color tags
                                if any(w in cell_text for w in ["HIGH", "CRITICAL"]):
                                    run.font.color.rgb = RGBColor(185, 28, 28)
                                    run.bold = True
                                elif any(w in cell_text for w in ["MED", "MEDIUM"]):
                                    run.font.color.rgb = RGBColor(217, 119, 6)
                                    run.bold = True
                                elif "LOW" in cell_text:
                                    run.font.color.rgb = RGBColor(5, 150, 105)
                                    run.bold = True
                                else:
                                    run.font.color.rgb = RGBColor(30, 41, 59)
                    
                    doc.add_paragraph() # Spacing
                in_table = False
                table_rows = []
                
        # Empty line
        if not stripped:
            i += 1
            continue
            
        # Horizontal Rule
        if re.match(r'^---+$', stripped):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
            # Add bottom border as divider
            pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="6" w:space="1" w:color="CBD5E1"/></w:pBdr>')
            p._p.get_or_add_pPr().append(pBdr)
            i += 1
            continue
            
        # Headings
        if stripped.startswith("# "):
            title_text = stripped[2:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run(title_text)
            run.font.name = "Calibri"
            run.font.size = Pt(20)
            run.font.bold = True
            run.font.color.rgb = RGBColor(15, 23, 42)
            i += 1
            continue
            
        if stripped.startswith("## "):
            h2_text = stripped[3:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="2" w:color="93C5FD"/></w:pBdr>')
            p._p.get_or_add_pPr().append(pBdr)
            run = p.add_run(h2_text)
            run.font.name = "Calibri"
            run.font.size = Pt(15)
            run.font.bold = True
            run.font.color.rgb = RGBColor(30, 58, 138)
            i += 1
            continue
            
        if stripped.startswith("### "):
            h3_text = stripped[4:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(3)
            run = p.add_run(h3_text)
            run.font.name = "Calibri"
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = RGBColor(3, 105, 161)
            i += 1
            continue
            
        if stripped.startswith("#### "):
            h4_text = stripped[5:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(h4_text)
            run.font.name = "Calibri"
            run.font.size = Pt(10.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(51, 65, 85)
            i += 1
            continue
            
        # Bullet list
        if stripped.startswith("* ") or stripped.startswith("- "):
            item_text = stripped[2:].strip()
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            
            # Parse formatting (bold/italic)
            parts = re.split(r'(\*\*.*?\*\*|\*.*?\*)', item_text)
            for part in parts:
                if part.startswith("**") and part.endswith("**"):
                    r = p.add_run(part[2:-2])
                    r.bold = True
                elif part.startswith("*") and part.endswith("*"):
                    r = p.add_run(part[1:-1])
                    r.italic = True
                else:
                    r = p.add_run(part)
                r.font.name = "Calibri"
                r.font.size = Pt(10)
                r.font.color.rgb = RGBColor(30, 41, 59)
            i += 1
            continue
            
        # Numbered list
        m_num = re.match(r'^(\d+)\.\s+(.+)$', stripped)
        if m_num:
            item_text = m_num.group(2).strip()
            p = doc.add_paragraph(style='List Number')
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            
            parts = re.split(r'(\*\*.*?\*\*|\*.*?\*)', item_text)
            for part in parts:
                if part.startswith("**") and part.endswith("**"):
                    r = p.add_run(part[2:-2])
                    r.bold = True
                elif part.startswith("*") and part.endswith("*"):
                    r = p.add_run(part[1:-1])
                    r.italic = True
                else:
                    r = p.add_run(part)
                r.font.name = "Calibri"
                r.font.size = Pt(10)
                r.font.color.rgb = RGBColor(30, 41, 59)
            i += 1
            continue

        # Regular paragraph
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        
        parts = re.split(r'(\*\*.*?\*\*|\*.*?\*|`.*?`)', stripped)
        for part in parts:
            if part.startswith("**") and part.endswith("**"):
                r = p.add_run(part[2:-2])
                r.bold = True
            elif part.startswith("*") and part.endswith("*"):
                r = p.add_run(part[1:-1])
                r.italic = True
            elif part.startswith("`") and part.endswith("`"):
                r = p.add_run(part[1:-1])
                r.font.name = "Consolas"
                r.font.size = Pt(9.0)
                r.font.color.rgb = RGBColor(15, 23, 42)
                continue
            else:
                r = p.add_run(part)
            r.font.name = "Calibri"
            r.font.size = Pt(10)
            r.font.color.rgb = RGBColor(30, 41, 59)
            
        i += 1

    # Save DOCX
    docx_out = "AI_Implementation_Roadmap_and_Prototype_Design.docx"
    doc.save(docx_out)
    print(f"Successfully generated {docx_out} ({os.path.getsize(docx_out)} bytes)")
    
    # Save DOC (copy as .doc format which Word opens natively)
    doc_out = "AI_Implementation_Roadmap_and_Prototype_Design.doc"
    import shutil
    shutil.copyfile(docx_out, doc_out)
    print(f"Successfully generated {doc_out} ({os.path.getsize(doc_out)} bytes)")

if __name__ == "__main__":
    create_document()
