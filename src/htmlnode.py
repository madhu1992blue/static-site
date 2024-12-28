from typing import Optional
class HTMLNode:
    def __init__(self, tag:Optional[str] = None, value:Optional[str]=None, children:Optional[list['HTMLNode']]=None, props: Optional[dict[str, str]]=None):
        self.tag: Optional[str] = tag
        self.value: Optional[str] = value
        self.children: Optional[list['HTMLNode']] = children
        self.props: Optional[dict[str, str]] = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self) -> str:
        if not self.props:
            return ""
        html = ""
        for k, v in self.props.items():
            html += f' {k}="{v}"'
        return html
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag:Optional[str], value:str , props: Optional[dict[str, str]]=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("value is null")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag:Optional[str], children: Optional[list['HTMLNode']], props: Optional[dict[str, str]]=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("tag is null")
        if self.children is None:
            raise ValueError("children missing")
        return f"<{self.tag}>{"".join(child.to_html() for child in self.children)}</{self.tag}>"
