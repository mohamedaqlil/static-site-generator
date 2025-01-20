

class HTMLNode:
  def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

  def to_html(self):
      raise NotImplementedError("to_html method not implemented")
  
  def props_to_html(self):
      if not self.props:
          return ""
      html = []
      for key, value in self.props.items():
          html.append(f" {key}=\"{value}\"")
      return "".join(html)
  
  def __repr__(self):
      return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
  
class LeafNode(HTMLNode):
    def __init__(self, value, tag = None, props = None):
        if value is None:
            raise ValueError("A LeafNode must have a value")
        super().__init__(tag = tag, value = value, props = props)

    def to_html(self):
        if not self.value:
            raise ValueError("A LeafNode must have a value")
        elif not self.tag:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
class LeafNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        if tag or children is None:
            raise ValueError("A LeafNode must have a tag and children")
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("A LeafNode must have a tag")
        elif not self.tag:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"