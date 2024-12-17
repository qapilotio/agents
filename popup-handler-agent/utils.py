import xml.etree.ElementTree as ET
import base64
import os
import requests
from io import BytesIO

def extract_popup_details(xml_input):
    """
    Determines if the given XML represents a popup and extracts its content, actions, and images.
    
    Args:
    xml_input (str): XML file path, URL, or XML content representing the screen hierarchy
    
    Returns:
    dict: A dictionary containing popup details with keys:
        - 'is_popup': Boolean indicating if the layout is a popup
        - 'content': List of text elements within the popup
        - 'actions': List of interactive elements (buttons, clickable items)
        - 'images': List of image details found in the popup
        - 'details': Additional metadata about the popup
    """
    try:
        # Parse XML input
        if isinstance(xml_input, str):
            if xml_input.startswith('http://') or xml_input.startswith('https://'):
                response = requests.get(xml_input)
                response.raise_for_status()
                xml_content = response.text
                root = ET.fromstring(xml_content)
            elif os.path.isfile(xml_input):
                tree = ET.parse(xml_input)
                root = tree.getroot()
            else:
                root = ET.fromstring(xml_input)
        else:
            raise ValueError("Invalid XML input type.")
        
        # Extract screen dimensions
        screen_width = int(root.get('width', 0))
        screen_height = int(root.get('height', 0))
        
        # Find potential popup layouts
        popup_layouts = [
            './/android.widget.FrameLayout', 
            './/android.app.Dialog', 
            './/android.widget.PopupWindow',
            './/androidx.appcompat.app.AlertDialog'
        ]
        
        # Result dictionary
        popup_result = {
            'is_popup': False,
            'content': [],
            'interactable_elements': [],
            'images': [],
            'details': {}
        }
        
        # Try different layout searches
        for layout_xpath in popup_layouts:
            first_component = root.find(layout_xpath)
            if first_component is None:
                continue
            
            # Extract bounds
            bounds = first_component.get('bounds', '')
            try:
                bounds_parts = bounds.strip('[]').split('][')
                x1, y1 = map(int, bounds_parts[0].split(','))
                x2, y2 = map(int, bounds_parts[1].split(','))
            except (ValueError, IndexError):
                continue
            
            # Calculate dimensions and position
            component_width = x2 - x1
            component_height = y2 - y1
            component_center_x = (x1 + x2) / 2
            component_center_y = (y1 + y2) / 2
            
            # Popup criteria
            screen_area = screen_width * screen_height
            component_area = component_width * component_height
            area_ratio = component_area / screen_area
            
            is_centered_x = abs(component_center_x - screen_width/2) < screen_width * 0.2
            is_centered_y = abs(component_center_y - screen_height/2) < screen_height * 0.2
            
            # Check if it's a popup
            if area_ratio < 1:
                popup_result['is_popup'] = True
                popup_result['details'] = {
                    'width': component_width,
                    'height': component_height,
                    'center_x': component_center_x,
                    'center_y': component_center_y
                }
                
                # Extract text content
                def extract_text(element):
                    # Find all elements with text that are not clickable
                    for elem in element.findall('.//*[@text]'):
                        text = elem.get('text', '')
                        clickable = elem.get('clickable', 'false') == 'true'
                        
                        if text and not clickable:
                            popup_result['content'].append(text)
                
                def extract_actions(element):
                    clickable_elements = element.findall('.//*[@clickable="true"]')
                    
                    for action_elem in clickable_elements:
                        action_details = {
                            'text': action_elem.get('text', ''),
                            'id': action_elem.get('resource-id', ''),
                            'type': action_elem.tag.split('.')[-1],
                            'bounds': action_elem.get('bounds', ''),
                            'content_desc': action_elem.get('content-desc', ''),
                            'enabled': action_elem.get('enabled', 'true') == 'true',
                            'focused': action_elem.get('focused', 'false') == 'true',
                            'scrollable': action_elem.get('scrollable', 'false') == 'true',
                            'long_clickable': action_elem.get('long-clickable', 'false') == 'true',
                            'password': action_elem.get('password', 'false') == 'true',
                            'selected': action_elem.get('selected', 'false') == 'true'
                        }
                        popup_result['interactable_elements'].append(action_details)
                
                # Extract image details
                def extract_images(element):
                    # Image-related XML tags in Android
                    image_tags = [
                        './/android.widget.ImageView',
                        './/android.widget.ImageButton',
                        './/android.widget.Image'
                    ]
                    
                    for tag in image_tags:
                        for img_elem in element.findall(tag):
                            img_details = {
                                'resource_id': img_elem.get('resource-id', ''),
                                'content_desc': img_elem.get('content-desc', ''),
                                'bounds': img_elem.get('bounds', '')
                            }
                            
                            drawable = img_elem.get('src', '')
                            if drawable or img_details['resource_id'] or img_details['content_desc']:
                                popup_result['images'].append(img_details)
                
                # Apply extraction methods
                extract_text(first_component)
                extract_actions(first_component)
                extract_images(first_component)
                
                return popup_result
        
        return popup_result
    
    except ET.ParseError as e:
        print(f"XML Parse Error: {e}")
        return {
            'is_popup': False,
            'content': [],
            'actions': [],
            'images': [],
            'details': {}
        }
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {
            'is_popup': False,
            'content': [],
            'actions': [],
            'images': [],
            'details': {}
        }
    

def encode_image(input_source):
    """
    Encodes an image from a file path, file object, or URL into a base64 string.

    Args:
    input_source (str or file-like object): The image file path, file object, or URL.

    Returns:
    str: Base64 encoded string of the image.
    """
    try:
        if isinstance(input_source, str):
            # Check if it's a URL
            if input_source.startswith('http://') or input_source.startswith('https://'):
                response = requests.get(input_source)
                response.raise_for_status()
                image_data = response.content
            # Check if it's a file path
            elif os.path.isfile(input_source):
                with open(input_source, 'rb') as image_file:
                    image_data = image_file.read()
            else:
                raise ValueError("Invalid file path or URL.")
        else:
            # Assume it's a file-like object
            image_data = input_source.read()

        # Encode the image data
        encoded_image = base64.b64encode(image_data).decode()
        return encoded_image

    except Exception as e:
        print(f"Error encoding image: {e}")
        return None