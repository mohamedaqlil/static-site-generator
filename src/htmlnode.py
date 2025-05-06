
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
    def __init__(self, tag=None, value="", props=None):
        super().__init__(tag=tag, value=value, props=props)
    
    def to_html(self):
        if self.tag is None:
            return self.value
        
        # Handle self-closing tags like img
        if self.tag in ["img", "br", "hr"] and not self.value:
            return f"<{self.tag}{self.props_to_html()} />"
        
        # For other tags, check if value exists
        if not self.value and self.tag not in ["img", "br", "hr"]:
            raise ValueError("A LeafNode must have a value")
            
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        if tag is None or children is None:
            raise ValueError("A ParentNode must have a tag and children")
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("A ParentNode must have a tag")
        elif self.children == None:
            raise ValueError("children is a missing value")
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.children_to_html()}</{self.tag}>"
        
    def children_to_html(self):
        results = []
        for child in self.children:
            result = child.to_html()
            results.append(result)
        return "".join(results)
    
        