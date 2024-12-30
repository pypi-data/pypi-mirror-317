Here’s the updated `README.md` with the new additions and functionality for **HarmonixPy**:

---

# **HarmonixPy**

**HarmonixPy** is a Python library designed to simplify the process of managing external files (e.g., HTML, CSS, JS, dependency files) in Python projects. It provides a seamless way to load and serve HTML files using Flask while automating the installation of dependencies from a `requirements.txt` file. It also allows you to customize the paths for HTML, CSS, and JS files for greater flexibility.

This library is ideal for developers working on lightweight backend projects or environments like **Pydroid**, which have limited support for external files.

---

## **Key Features**
- **File Management:** Load and serve external HTML, CSS, and JS files in your Python project with minimal effort.
- **Flask Integration:** Dynamically serve HTML files using Flask’s `render_template_string`.
- **Dependency Automation:** Automatically install required dependencies from a `requirements.txt` file using `subprocess`.
- **Customizable Paths:** Flexible configuration for specifying the paths of your HTML, CSS, and JS files.
- **Default File Creation:** Automatically creates default HTML, CSS, and JS files if not provided.

---

## **Installation**
Install **HarmonixPy** using pip:
```bash
pip install harmonixpy
```

---

## **Quick-Start Example**
Here’s how to use **HarmonixPy** in your project:

### **Step 1: Create Your HTML, CSS, and JS Files**
- Save your HTML file (e.g., `templates/index.html`).
- Save your CSS file (e.g., `static/styles.css`).
- Save your JavaScript file (e.g., `static/scripts.js`).
- Save your dependencies in a `requirements.txt` file, such as:
  ```
  flask
  requests
  beautifulsoup4
  ```

### **Step 2: Write Your Python Code**
```python
from harmonixpy import HarmonixPy

# Initialize the library with file paths
HarmonixPy(
    html_file="templates/custom_index.html",  # Path to the HTML file
    css_file="static/custom_styles.css",      # Path to the CSS file
    js_file="static/custom_scripts.js",       # Path to the JavaScript file
    requirements_file="custom_requirements.txt",  # Path to the requirements file
    static_folder="custom_static"             # Path to the static folder
)
```

### **Step 3: What Happens Under the Hood**
1. **HarmonixPy** reads the HTML file and dynamically renders it using Flask.  
2. It parses the `requirements.txt` file and installs missing dependencies automatically.  
3. The app creates default files (HTML, CSS, JS) if they don’t exist.
4. A Flask web server is launched to serve the HTML file.

### **Step 4: Running the App**
The app will automatically start and be accessible at `http://127.0.0.1:5000/`. Open this URL in your browser to see your HTML file rendered as a web page.

---

## **Requirements**
- Python 3.7 or higher.
- Flask (installed automatically via the library).

---

## **Functions**
**HarmonixPy** provides the following functions to manage the app configuration:
- `html(file_path)`: Sets the path to the HTML file.
- `css(file_path)`: Sets the path to the CSS file.
- `js(file_path)`: Sets the path to the JavaScript file.
- `dependency(file_path)`: Sets the path to the `requirements.txt` file.
- `create_default_files()`: Creates default HTML, CSS, and JS files if not already present.
- `run(host="127.0.0.1", port=5000)`: Runs the Flask app at the specified host and port.

### **Usage Example with Individual Functions:**
```python
import harmonixpy as hmnx

# Set custom paths for HTML, CSS, and JS files
hmnx.html("templates/custom_index.html")
hmnx.css("static/custom_styles.css")
hmnx.js("static/custom_scripts.js")

# Set the requirements file and static folder
hmnx.dependency("custom_requirements.txt")
hmnx.run()  # Start the Flask app
```

---

## **Contributing**
We welcome contributions! Please refer to the `contributing.md` file for guidelines on reporting issues, submitting pull requests, or participating in discussions.

---

## **License**
This project is licensed under the Apache License. See the `license.md` file for more details.

---

### **Changelog**
- **Version 0.0.2**: Added support for CSS and JS file paths in the `HarmonixPy` initialization.
- **Version 0.0.1**: Initial release with HTML and dependency file handling.

---

This updated `README.md` reflects the new functionality and flexibility introduced in **HarmonixPy**. It covers how to initialize the library with custom HTML, CSS, JS files, as well as the new, simplified usage patterns for users.