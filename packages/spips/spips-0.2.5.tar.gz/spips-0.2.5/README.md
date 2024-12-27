Installation

1. Install from PyPI

The Spips framework is available on PyPI. You can install it directly using pip:

pip install spips

> Note: Ensure that you have pip and Python 3.7 or higher installed.




---

2. Create a New Project

Once Spips is installed, you can set up a new project in a few steps:

1. Create a project folder:

mkdir my_spips_project
cd my_spips_project


2. Create the main entry point:
Create a Python file, for example main.py:

touch main.py


3. Add initial code to main.py:
Here is the minimal starter code for a Spips application:

from spips import Spips, Model, controler

# Initialize the app
app = Spips()
controller = controler(app)

# Define routing
@app.route("/", "get")
def home():
    app.render("home", title="Welcome", message="Spips application is ready!")

if __name__ == "__main__":
    app.serve(port=8000)


4. Create a template:
Add a views folder to store templates and create a home.part.spips file:

mkdir views
touch views/home.part.spips

Add the following content to views/home.part.spips:

<!DOCTYPE html>
<html>
<head>
    <title>{#title}</title>
</head>
<body>
    <h1>{#message}</h1>
</body>
</html>




---

3. Run the Server

Run the application with Python:

python main.py

Open your browser and navigate to http://localhost:8000. You should see the message "Spips application is ready!".


---

4. Verify Installation

To confirm that Spips is correctly installed, you can run:

pip show spips

This will display information such as the version, author, and location of the Spips package.


---

Requirements

Python 3.7+

Library dependency: colorama (installed automatically via pip).



---

Now you’re ready to build your web applications with Spips! 🚀

