from bs4 import BeautifulSoup

def convert_html_to_twig(html_content):
    """
    Converts HTML content to Twig format.
    
    Args:
        html_content (str): HTML content to convert
        
    Returns:
        str: Converted Twig content or None if conversion fails
    
    Raises:
        Exception: If conversion fails
    """
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        
        # First pass: collect all tags that will need variables
        tags_with_content = set()
        for tag in soup.find_all():
            if tag.string and tag.string.strip():
                tags_with_content.add(tag.name)
        
        # Second pass: replace content and attributes
        for tag in soup.find_all():
            # Replace text content with Twig variables
            if tag.string and tag.string.strip():
                tag.string = f"{{{{ {tag.name}_content }}}}"
            
            # Replace attributes with Twig variables
            for attr, value in list(tag.attrs.items()):
                tag[attr] = f"{{{{ {attr}_{tag.name} }}}}"
        
        # Generate comments for Twig variables
        twig_comments = []
        for tag_name in sorted(tags_with_content):
            twig_comments.append(
                f"<!-- `{{{{ {tag_name}_content }}}}`: Content for <{tag_name}> -->"
            )
        
        return f"{chr(10).join(twig_comments)}\n{soup.prettify()}"
    except Exception as e:
        raise Exception(f"Error converting HTML to Twig: {e}")