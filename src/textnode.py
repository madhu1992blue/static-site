from enum import Enum
from typing import Optional

from htmlnode import HTMLNode, LeafNode
from markdown import extract_markdown_images, extract_markdown_links

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text:str, text_type:TextType, url: Optional[str]=None):
        self.text:str = text
        self.text_type:TextType = text_type
        self.url:Optional[str] = url

    def __eq__(self, other)->bool:
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text \
                and self.text_type == other.text_type \
                and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    

def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b",text_node.text)
        case TextType.ITALIC:
            return LeafNode("i",text_node.text)
        case TextType.CODE:
            return LeafNode("code",text_node.text)
        case TextType.LINK:
            if not text_node.url:
                raise ValueError("Invalid Link URL")
            return LeafNode("a",text_node.text,{"href": text_node.url})
        case TextType.IMAGE:
            if not text_node.url:
                raise ValueError("Invalid Image URL")
            props = { "src": text_node.url}
            if text_node.text:
                props["alt"] = text_node.text
            return LeafNode("img", "", props)
        case _:
            raise Exception("Unknown TextType")



def split_text_delimiter(node: TextNode, delimiter: str, text_type: TextType):
    nodes = []
    segment_start = 0
    segment_end = segment_start
    had_delimited_node_started = False
    while segment_end + len(delimiter) <= len(node.text):
        if node.text[segment_end: segment_end + len(delimiter)] == delimiter:
            if not had_delimited_node_started:
                if segment_start != segment_end:
                    nodes.append(TextNode(node.text[segment_start: segment_end], TextType.TEXT))
                had_delimited_node_started = True
            else:
                if segment_start != segment_end:
                    nodes.append(TextNode(node.text[segment_start: segment_end], text_type))
                had_delimited_node_started = False
            segment_start = segment_end + len(delimiter)
            segment_end = segment_start
        else:
            segment_end += 1
    if had_delimited_node_started:
        raise Exception("Delimiter not ended")
    if segment_start != segment_end:
        nodes.append(TextNode(node.text[segment_start: ], TextType.TEXT))
    return nodes

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter:str, text_type: TextType)->list[TextNode]:
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
            continue
        nodes.extend(split_text_delimiter(node, delimiter, text_type))
    return nodes


def split_nodes_image(old_nodes: list[TextNode]):
    nodes = []
    for node in old_nodes:
        text = node.text
        altTextImages = extract_markdown_images(text)
        for altText, imageUrl in altTextImages:
            imageInMD = f"![{altText}]({imageUrl})"
            text_parts = text.split(imageInMD,1)
            left = text_parts[0]
            if left:
                nodes.append(TextNode(left, TextType.TEXT))
            if imageInMD in text:
                nodes.append(TextNode(altText, TextType.IMAGE,imageUrl))
            text = text_parts[1]
    return nodes
    
def split_nodes_link(old_nodes: list[TextNode]):
    nodes = []
    for node in old_nodes:
        text = node.text
        valUrls = extract_markdown_links(text)
        for value, url in valUrls:
            urlInMD = f"[{value}]({url})"
            text_parts = text.split(urlInMD,1)
            left = text_parts[0]
            if left:
                nodes.append(TextNode(left, TextType.TEXT))
            if urlInMD in text:
                nodes.append(TextNode(value, TextType.LINK, url))
            text = text_parts[1]
    return nodes