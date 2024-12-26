from reactpy import component, html
from pathlib import Path

_pathway = None

def static(path_to_static_content):
    """
    Set the static directory path relative to the package's parent folder.
    """
    global _pathway  
    folder = Path(__file__).parent.parent.resolve()
    path = (folder / path_to_static_content).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Static content path {path} does not exist.")
    _pathway = path

@component
def use_CSS(css_file):
    """
    ReactPy component to load CSS content into a <style> tag.
    """
    global _pathway
    if _pathway is None:
        raise ValueError("Static path is not set. Call static() first.")
    
    css_path = _pathway / css_file
    if not css_path.exists():
        raise FileNotFoundError(f"CSS file {css_path} does not exist.")
    
    with open(css_path, 'r') as file:
        css_content = file.read()
    
    return html.style(css_content)

@component
def use_JS(js_file, module=False):
    """
    ReactPy component to load JS content into a <script> tag.
    """
    global _pathway
    if _pathway is None:
        raise ValueError("Static path is not set. Call static() first.")
    
    js_path = _pathway / js_file
    if not js_path.exists():
        raise FileNotFoundError(f"JS file {js_path} does not exist.")
    
    with open(js_path, 'r') as file:
        js_content = file.read()
    
    script_attrs = {"type": "module"} if module else {}
    
    return html.script(script_attrs, js_content)

@component
def use_media(media_file, alt_text="", autoplay=False, controls=True, loop=False):
    """
    ReactPy component to handle media files (images or videos).
    
    Parameters:
        media_file (str): The name of the media file (image or video).
        alt_text (str): Alt text for image files.
        autoplay (bool): Whether to autoplay video files (default: False).
        controls (bool): Whether to show controls for video files (default: True).
        loop (bool): Whether to loop the video (default: False).
    """
    global _pathway
    if _pathway is None:
        raise ValueError("Static path is not set. Call static() first.")
    
    media_path = _pathway / media_file
    if not media_path.exists():
        raise FileNotFoundError(f"Media file {media_path} does not exist.")
    
    file_extension = media_path.suffix.lower()
    
    if file_extension in [".png", ".jpg", ".jpeg", ".gif"]:
        
        return html.img({"src": str(media_path), "alt": alt_text})
    
    elif file_extension in [".mp4", ".webm", ".ogg"]:
        
        video_attrs = {
            "src": str(media_path),
            "autoplay": autoplay,
            "controls": controls,
            "loop": loop,
        }
        return html.video(video_attrs)
    
    else:
        raise ValueError(f"Unsupported media file type: {file_extension}")