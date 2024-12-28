import re
from enum import Enum
class BlockType(Enum):
    Heading = "heading"
    Paragraph = "paragraph"
    Code = "code"
    Quote = "quote"
    OrderedList = "orderedlist"
    UnorderedList = "unorderedlist"

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    res = []
    for block in blocks:
        trimmedBlock = block.strip()
        if trimmedBlock!= "":
            res.append(trimmedBlock)
    return res
    
def block_to_block_type(block: str)->BlockType:
    lines = block.split("\n")
    if len(lines)==1 and block.startswith(("# ","## ","### ", "#### ", "##### ", "###### ")):
        return BlockType.Heading
    
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.Code
    
    if lines[0].startswith(">"):
        isQuote = True
        for line in lines:
            if not line.startswith(">"):
                isQuote = False
        if isQuote:
            return BlockType.Quote
        else:
            return BlockType.Paragraph
    
    if lines[0].startswith("- "):
        isList = True
        for line in lines:
            if not line.startswith("- "):
                isList = False
        if isList:
            return BlockType.UnorderedList
        else:
            return BlockType.Paragraph
    
    if lines[0].startswith("* "):
        isList = True
        for line in lines:
            if not line.startswith("* "):
                isList = False
        if isList:
            return BlockType.UnorderedList
        else:
            return BlockType.Paragraph
        
    if lines[0].startswith("1. "):
        isList = True
        counter = 1
        for line in lines:
            if not line.startswith(f"{counter}. "):
                isList = False
            counter += 1
        if isList:
            return BlockType.OrderedList
        else:
            return BlockType.Paragraph
    return BlockType.Paragraph