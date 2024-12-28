import re
from enum import Enum
from htmlnode import ParentNode, HTMLNode, LeafNode
from textnode import text_node_to_html_node, text_to_textnodes
class BlockType(Enum):
    Heading = "heading"
    Paragraph = "paragraph"
    Code = "code"
    Quote = "quote"
    OrderedList = "orderedlist"
    UnorderedList = "unorderedlist"




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

def get_heading_level(heading:str) -> int:
    return len(heading.split(" ",1)[0])

def get_heading_val(heading:str) -> str:
    return heading.split(" ",1)[1]

def get_code_val(codeBlock:str) -> str:
    return codeBlock.strip("```")


def get_quote_val(quoteBlock:str) -> str:
    res = []
    for line in quoteBlock.split("\n"):
        res.append(line[1:])
    return "\n".join(res)


def get_li_html_node(block:str)->list[HTMLNode]:
    lines = block.split("\n")
    nodes = []
    for line in lines:
        nodes.append(LeafNode("li", line[2:]))
    return nodes


def text_to_children(text:str)->list[HTMLNode]:
    text_nodes = []
    for l in text.split("\n"):
        text_nodes.extend(text_to_textnodes(l))
    return [text_node_to_html_node(tn) for tn in text_nodes]


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.Heading:
            return LeafNode(f"h{get_heading_level(block)}", get_heading_val(block))
        case BlockType.Code:
            return ParentNode("pre", [LeafNode("code", get_code_val(block) )])
        case BlockType.Quote:
            return LeafNode("blockquote",get_quote_val(block))
        case BlockType.UnorderedList:
            return ParentNode("ul", get_li_html_node(block))
        case BlockType.OrderedList:
            return ParentNode("ol", get_li_html_node(block))
        case BlockType.Paragraph:
            return ParentNode("p", text_to_children(block))
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_htmls: list[HTMLNode] = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", block_htmls)

        