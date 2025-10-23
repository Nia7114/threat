#!/usr/bin/env python3
"""
Fix CSS selectors in dashboard_window.py
"""

import re

def fix_css_selectors():
    """Fix CSS selectors that need double braces in f-strings"""
    
    with open('ui/dashboard_window.py', 'r') as f:
        content = f.read()
    
    # Find the apply_styles method
    start_marker = "def apply_styles(self):"
    end_marker = '        """)'
    
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("Could not find apply_styles method")
        return
    
    # Find the end of the method (next method definition)
    next_method_idx = content.find("\n    def ", start_idx + len(start_marker))
    if next_method_idx == -1:
        next_method_idx = len(content)
    
    # Extract the method content
    method_content = content[start_idx:next_method_idx]
    
    # Fix CSS selectors - only within the setStyleSheet f-string
    # Look for CSS selectors that need double braces
    css_patterns = [
        (r'(\s+)(#[a-zA-Z][a-zA-Z0-9_-]*)\s+\{([^{])', r'\1\2 {{\3'),
        (r'(\s+)(QPushButton#[a-zA-Z][a-zA-Z0-9_-]*)\s+\{([^{])', r'\1\2 {{\3'),
        (r'(\s+)(QPushButton#[a-zA-Z][a-zA-Z0-9_-]*:[a-zA-Z]+)\s+\{([^{])', r'\1\2 {{\3'),
        (r'(\s+)(QProgressBar#[a-zA-Z][a-zA-Z0-9_-]*)\s+\{([^{])', r'\1\2 {{\3'),
        (r'(\s+)(QProgressBar#[a-zA-Z][a-zA-Z0-9_-]*::[a-zA-Z]+)\s+\{([^{])', r'\1\2 {{\3'),
        (r'(\s+)(QCheckBox#[a-zA-Z][a-zA-Z0-9_-]*)\s+\{([^{])', r'\1\2 {{\3'),
    ]
    
    # Apply fixes
    fixed_method = method_content
    for pattern, replacement in css_patterns:
        fixed_method = re.sub(pattern, replacement, fixed_method)
    
    # Fix closing braces - only for CSS selectors
    # Look for lines that are just closing braces in CSS context
    lines = fixed_method.split('\n')
    fixed_lines = []
    in_css_block = False
    
    for line in lines:
        if 'setStyleSheet(f"""' in line:
            in_css_block = True
            fixed_lines.append(line)
        elif in_css_block and '        """)' in line:
            in_css_block = False
            fixed_lines.append(line)
        elif in_css_block and re.match(r'^\s+\}$', line):
            # This is a CSS closing brace, make it double
            fixed_lines.append(line.replace('}', '}}'))
        else:
            fixed_lines.append(line)
    
    fixed_method = '\n'.join(fixed_lines)
    
    # Replace the method in the original content
    new_content = content[:start_idx] + fixed_method + content[next_method_idx:]
    
    # Write back
    with open('ui/dashboard_window.py', 'w') as f:
        f.write(new_content)
    
    print("✅ Fixed CSS selectors in apply_styles method")

if __name__ == "__main__":
    fix_css_selectors()
