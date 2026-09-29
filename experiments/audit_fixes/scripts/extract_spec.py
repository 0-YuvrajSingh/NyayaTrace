import sys
import docx
from docx.document import Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph

def iter_block_items(parent):
    if isinstance(parent, Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("Parent must be Document or _Cell")

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)

def main():
    doc = docx.Document("/repo/Indian_Legal_XAI.docx")
    with open("/repo/experiments/audit_fixes/spec_full_text.txt", "w", encoding="utf-8") as f:
        for block in iter_block_items(doc):
            if isinstance(block, Paragraph):
                text = block.text.strip()
                if text:
                    f.write(f"[PARAGRAPH] {text}\n")
            elif isinstance(block, Table):
                for row in block.rows:
                    row_data = []
                    for cell in row.cells:
                        row_data.append(cell.text.replace('\n', ' ').strip())
                    f.write(f"[TABLE] {' | '.join(row_data)}\n")

if __name__ == '__main__':
    main()
