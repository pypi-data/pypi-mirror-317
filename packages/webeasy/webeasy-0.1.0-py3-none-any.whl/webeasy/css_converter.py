import re
from copy import deepcopy

def parse_variable_file(variable_content):
    """
    Parses SCSS variable content and returns color name to value mapping.
    
    Args:
        variable_content (str): SCSS variable content
        
    Returns:
        dict: Mapping of color values to variable names
    """
    variables = {}
    temp_references = {}
    
    color_pattern = re.compile(r'^\s*\$([\w-]+):\s*(#[a-fA-F0-9]{3,6}|rgba?\([^)]+\))\s*(!default)?\s*;')
    reference_pattern = re.compile(r'^\s*\$([\w-]+):\s*\$([\w-]+)\s*(!default)?\s*;')
    
    lines = variable_content.splitlines()
    for line in lines:
        if not line.strip() or line.strip().startswith('//') or 'map-merge' in line:
            continue
            
        color_match = color_pattern.match(line)
        if color_match:
            var_name = color_match.group(1)
            color_value = color_match.group(2)
            variables[color_value] = f"${var_name}"
            continue
            
        ref_match = reference_pattern.match(line)
        if ref_match:
            referencing_var = ref_match.group(1)
            referenced_var = ref_match.group(2)
            temp_references[referencing_var] = referenced_var
    
    final_variables = deepcopy(variables)
    
    for referencing_var, referenced_var in temp_references.items():
        for color, var_name in variables.items():
            if var_name == f"${referenced_var}":
                final_variables[color] = f"${referencing_var}"
                break
    
    return final_variables

def convert_css_to_scss(css_content, variable_mapping):
    """
    Converts CSS content to SCSS by replacing color values with variables.
    
    Args:
        css_content (str): CSS content to convert
        variable_mapping (dict): Mapping of color values to variable names
        
    Returns:
        str: Converted SCSS content
    """
    replacements = sorted(
        list(variable_mapping.items()),
        key=lambda x: len(x[0]) if not x[0].startswith('$') else 0,
        reverse=True
    )
    
    result_lines = []
    for line in css_content.splitlines():
        processed_line = line
        
        if '/*' in line and '*/' in line:
            comment_start = line.index('/*')
            comment_end = line.index('*/') + 2
            before_comment = line[:comment_start]
            comment = line[comment_start:comment_end]
            after_comment = line[comment_end:]
            
            for color, variable in replacements:
                if not color.startswith('$'):
                    before_comment = before_comment.replace(color, variable)
                    after_comment = after_comment.replace(color, variable)
            
            processed_line = before_comment + comment + after_comment
        else:
            for color, variable in replacements:
                if not color.startswith('$'):
                    processed_line = processed_line.replace(color, variable)
        
        result_lines.append(processed_line)
    
    return '\n'.join(result_lines)
