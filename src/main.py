from textnode import TextType, TextNode
from htmlnode import HTMLNode
def main():
    print(TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev"))
    print(HTMLNode("body",None, [HTMLNode("a", "Haha", None, {"href": "http://example.com"})]))

if __name__ == "__main__":
    main()
    
    
