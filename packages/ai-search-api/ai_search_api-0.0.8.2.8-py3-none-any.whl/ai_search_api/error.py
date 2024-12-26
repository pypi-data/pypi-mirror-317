from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    error_message = """
    <html>
        <head>
            <title>Page Not Found</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    color: #333;
                    margin: 0;
                    padding: 0;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    display: flex;
                }
                .container {
                    text-align: center;
                    background-color: #ffffff;
                    border-radius: 10px;
                    padding: 30px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    max-width: 600px;
                    width: 100%;
                }
                h2 {
                    font-size: 2.5em;
                    color: #e74c3c;
                    margin-bottom: 20px;
                }
                h1 {
                    font-size: 10em;
                    color: #e74c3c;
                    margin-bottom: 20px;
                    text-align: center;
                    margin-top: -100px;
                }
                p {
                    font-size: 1.2em;
                    line-height: 1.6;
                    margin: 10px 0;
                    color: #555;
                }
                a {
                    text-decoration: none;
                    color: #3498db;
                    font-weight: bold;
                    transition: color 0.3s;
                }
                a:hover {
                    color: #e74c3c;
                }
                .button {
                    display: inline-block;
                    padding: 10px 20px;
                    font-size: 1.2em;
                    background-color: #3498db;
                    color: white;
                    text-align: center;
                    border-radius: 5px;
                    margin-top: 20px;
                    text-decoration: none;
                    transition: background-color 0.3s;
                }
                .button:hover {
                    background-color: #2980b9;
                }

                .center {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
            </style>
        </head>
        <body>
        <div>
        <h1>404</h1>
        <div class="center">
            <div class="container">
                <h2>Oops! An unexpected error occurred.</h2>
                <p>The page you are looking for was not loaded correctly. It might have been deleted, removed, or the link could be broken.</p>
                <p>We suggest you go back to the home page</p>
                <p>If the problem persists, please contact technical support.</p>
            </div>
        </div>
        </div>
        </body>
    </html>
    """
    print(error_message, 404)

    return error_message, 404

@app.route("/404/local")
def local_page_not_found():
    error_message = """
    <html>
    <head>
        <title>Page Not Found</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                color: #333;
                margin: 0;
                padding: 0;
                justify-content: center;
                align-items: center;
                height: 100vh;
                display: flex;
            }
            .container {
                text-align: center;
                background-color: #ffffff;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                max-width: 600px;
                width: 100%;
            }
            h2 {
                font-size: 2.5em;
                color: #e74c3c;
                margin-bottom: 20px;
            }
            h1 {
                font-size: 10em;
                color: #e74c3c;
                margin-bottom: 20px;
                text-align: center;
                margin-top: -100px;
            }
            p {
                font-size: 1.2em;
                line-height: 1.6;
                margin: 10px 0;
                color: #555;
            }
            a {
                text-decoration: none;
                color: #3498db;
                font-weight: bold;
                transition: color 0.3s;
            }
            a:hover {
                color: #e74c3c;
            }
            .button {
                display: inline-block;
                padding: 10px 20px;
                font-size: 1.2em;
                background-color: #3498db;
                color: white;
                text-align: center;
                border-radius: 5px;
                margin-top: 20px;
                text-decoration: none;
                transition: background-color 0.3s;
            }
            .button:hover {
                background-color: #2980b9;
            }

            .center {
                display: flex;
                justify-content: center;
                align-items: center;
            }
        </style>
    </head>
   <body>
<div>
<h1>404</h1>
<div class="center">
<div class="container">
<h2>Oops! An unexpected error occurred.</h2>
<p>The "local" page has been removed due to a technical issue that we are trying to resolve as soon as possible.</p>
<p>We apologize for the inconvenience and thank you for your understanding.</p>
<p>Please return to the home page in the meantime.</p>
<p>If the problem persists, please feel free to contact technical support.</p>
</div>
</div>
</div>
</body>
</html>

    """
    print(error_message, 404)
    return error_message, 404

print("for more information about the error go to this page:")
app.run(debug=True)