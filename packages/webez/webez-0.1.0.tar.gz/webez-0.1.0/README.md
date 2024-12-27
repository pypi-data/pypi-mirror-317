# webez

**A versatile tool to convert HTML to Twig and CSS to SCSS**

---

## Overview
webez simplifies the conversion of HTML content to Twig templates and CSS stylesheets to SCSS formats. By leveraging this tool, developers can accelerate their workflow when working with modern templating systems and SCSS frameworks.

---

## Features
- **HTML to Twig Conversion**: Quickly convert HTML files into Twig template format with appropriate variable mappings.
- **CSS to SCSS Conversion**: Replace CSS color values with predefined SCSS variables to streamline your styling workflow.

---

## Installation
```bash
pip install webez
```

---

## Usage
webez provides a command-line interface for converting files. Below are the available commands and their usage.

### HTML to Twig
Convert an HTML file to a Twig file:
```bash
python <script_name>.py html2twig <html_file> <output_file>
```
**Example**:
```bash
python <script_name>.py html2twig input.html output.twig
```

### CSS to SCSS
Convert a CSS file to SCSS format using variable mappings from an SCSS variables file:
```bash
python <script_name>.py css2scss <css_file> <variables_file> <output_file>
```
**Example**:
```bash
python <script_name>.py css2scss styles.css variables.scss output.scss
```

---

## Example Code
### Convert HTML to Twig using Python
```python
# Import required modules
from webez.html_converter import convert_html_to_twig
from IPython.display import HTML, display

# Sample HTML content
sample_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <h1>Welcome</h1>
    <div class="container">
        <p>This is a test paragraph</p>
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
        </ul>
    </div>
</body>
</html>
"""

# Convert HTML to Twig
twig_output = convert_html_to_twig(sample_html)

# Display original HTML
print("Original HTML:")
print("-" * 50)
display(HTML(sample_html))

# Display converted Twig
print("\nConverted Twig:")
print("-" * 50)
print(twig_output)
```

---

## Code Explanation
webez consists of two main converters:

### HTML Converter
The `html_converter.py` module leverages `BeautifulSoup` to parse and modify HTML content into Twig templates. This includes converting text and attributes into Twig variable placeholders.

### CSS Converter
The `css_converter.py` module reads an SCSS variable file, creates a mapping of color values to variables, and replaces corresponding CSS values with SCSS variables.

---

## Example Input and Output
### HTML to Twig
**Input HTML**:
```html
<div class="example">Welcome</div>
```
**Output Twig**:
```twig
<!-- `{{ div_content }}`: Content for <div> -->
<div class="{{ class_div }}">{{ div_content }}</div>
```

### CSS to SCSS
**Input CSS**:
```css
body {
  background-color: #ffffff;
  color: #333333;
}
```
**Variable File (variables.scss)**:
```scss
$white: #ffffff;
$gray-dark: #333333;
```
**Output SCSS**:
```scss
body {
  background-color: $white;
  color: $gray-dark;
}
```

---

## License
This project is licensed under the MIT License.

---

## Author
- **Akshay Chame**
  - Email: akshaychame2@gmail.com
  - GitHub: [akshayram1](https://github.com/akshayram1/webez)

---

## Contributing
Contributions, issues, and feature requests are welcome! Feel free to fork the repository and submit pull requests on GitHub.

---

## Additional Information
### Package Metadata
- **Name**: webez
- **Description**: A tool to convert HTML to Twig and CSS to SCSS.
- **Long Description**: `file: README.md`
- **Content Type**: `text/markdown`
- **Author**: Akshay Chame
- **Email**: akshaychame2@gmail.com
- **URL**: [https://github.com/akshayram1/webez](https://github.com/akshayram1/webez)
- **License**: MIT

