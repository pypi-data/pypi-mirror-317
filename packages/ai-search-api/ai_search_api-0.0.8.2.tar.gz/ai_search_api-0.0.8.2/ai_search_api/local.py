from flask import Flask, request, jsonify, render_template_string
import ai_search_api.ai_search as ai

app = Flask(__name__)

def search(text):
    ai.req = text
    ai.run()
    results = ai.result
    result_two = results
    results = []
    return result_two

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/start')
def start():
    return render_template_string(HTML_START_TEMPLATE)

@app.route('/start/update')
def update():
    import ai_search_api.update
    import ai_search_api.database as db
    return "Ai-search successful update! <a href='http://127.0.0.1:5000/start'>go to chat</a><br>to update the software write this command in the terminal of this folder: <code style='background: black; color: white; padding: 10px; border-radius: 10px;'>python update.py</code><br>Make sure you have deleted the temp repo folder before upgrading<hr>database content: <br>" + str(db.search) + "<hr><br><h3><a href='https://https://www.gitlab.com/neopad/'>@Neopad</a><br><hr><p>Thanks for your support!</p>"

@app.route('/api/search', methods=['POST'])
def api_search():
    text = request.json.get('text', '')
    result = search(text)
    return jsonify({'result': result})


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ai-search - NeopadAI</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.11.4/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.11.4/ScrollTrigger.min.js"></script>
    <style>
        :root {
            --primary-color: #3e95e0;
            --background-color: #202123;
            --secondary-background: #343541;
            --text-color: #ececf1;
            --secondary-text-color: #c5c5d2;
            --accent-color: #10a37f;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.5;
            color: var(--text-color);
            background-color: var(--background-color);
            overflow-x: hidden;
        }

        .container {
            width: 100%;
            max-width: 1200px;
            margin: auto;
            padding: 0 20px;
        }

        header {
            background: rgba(32, 33, 35, 0.8);
            backdrop-filter: blur(20px);
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            transition: all 0.3s ease;
        }

        header .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 60px;
        }

        header a {
            color: var(--text-color);
            text-decoration: none;
            font-weight: 400;
            font-size: 16px;
            transition: color 0.3s ease;
        }

        header nav a {
            margin-left: 30px;
            position: relative;
        }

        header nav a::after {
            content: '';
            position: absolute;
            width: 100%;
            height: 2px;
            bottom: -5px;
            left: 0;
            background-color: var(--primary-color);
            visibility: hidden;
            transform: scaleX(0);
            transition: all 0.3s ease-in-out;
        }

        header nav a:hover::after {
            visibility: visible;
            transform: scaleX(1);
        }

        header #branding {
            font-size: 24px;
            font-weight: 600;
            color: var(--primary-color);
        }

        #showcase {
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            background: var(--secondary-background);
            position: relative;
            overflow: hidden;
        }

        #showcase .content {
            max-width: 800px;
            position: relative;
            z-index: 1;
        }

        #showcase h1 {
            font-size: 48px;
            font-weight: 700;
            margin-bottom: 20px;
            color: var(--primary-color);
        }

        #showcase p {
            font-size: 20px;
            color: var(--secondary-text-color);
            margin-bottom: 30px;
        }

        .btn {
            display: inline-block;
            background-color: var(--primary-color);
            color: var(--text-color);
            padding: 12px 30px;
            border-radius: 4px;
            text-decoration: none;
            font-weight: 500;
            border: none;
            cursor: pointer;
            font-size: 16px;
        }

        .btn:hover {
            background-color: #3078b8;
        }

        #features {
            padding: 100px 0;
            background-color: var(--background-color);
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 40px;
        }

        .feature {
            background-color: var(--secondary-background);
            border-radius: 8px;
            padding: 30px;
            transition: all 0.3s ease;
        }

        .feature:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        }

        .feature img {
            width: 60px;
            height: 60px;
            margin-bottom: 20px;
        }

        .feature h3 {
            margin-bottom: 15px;
            font-weight: 600;
            font-size: 20px;
            color: var(--primary-color);
        }

        .feature p {
            color: var(--secondary-text-color);
            font-size: 16px;
        }

        #demo {
            padding: 100px 0;
            background-color: var(--secondary-background);
        }

        #demo h2 {
            text-align: center;
            font-size: 32px;
            margin-bottom: 40px;
            color: var(--primary-color);
        }

        .demo-window {
            background-color: var(--background-color);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }

        .demo-toolbar {
            background-color: #2d2d30;
            padding: 10px;
            display: flex;
            justify-content: flex-start;
        }

        .demo-button {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }

        .demo-button.red { background-color: #ff5f56; }
        .demo-button.yellow { background-color: #ffbd2e; }
        .demo-button.green { background-color: #27c93f; }

        .demo-content {
            padding: 20px;
            color: var(--text-color);
            font-family: 'Courier New', Courier, monospace;
            font-size: 14px;
            line-height: 1.5;
        }

        footer {
            background-color: var(--background-color);
            color: var(--secondary-text-color);
            text-align: center;
            padding: 40px 0;
            font-size: 14px;
        }

        footer .social-links {
            margin-top: 20px;
        }

        footer .social-links a {
            color: var(--secondary-text-color);
            margin: 0 10px;
            font-size: 20px;
            transition: color 0.3s ease;
        }

        footer .social-links a:hover {
            color: var(--primary-color);
        }

        @media (max-width: 768px) {
            header nav {
                display: none;
            }

            #showcase h1 {
                font-size: 36px;
            }

            #showcase p {
                font-size: 18px;
            }

            .feature-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div id="branding">NeopadAI</div>
        </div>
    </header>

    <section id="showcase">
        <div class="content">
            <h1>Test the new ai-search</h1>
            <p>Discover a new way to search. Efficient. Intuitive. Revolutionary.</p>
            <a href="/start" class="btn">Start Now</a>
            <a href="/start/update" class="btn">Update Now</a>
        </div>
    </section>

    <section id="demo">
        <div class="container">
            <h2>See NeopadAI in action</h2>
            <div class="demo-window">
                <div class="demo-toolbar">
                    <div class="demo-button red"></div>
                    <div class="demo-button yellow"></div>
                    <div class="demo-button green"></div>
                </div>
                <div class="demo-content">
                    <pre><code>
# request
import ai_search.main as ai

# set the request
ai.req = input('ai-search: ')
ai.run()
results = ai.result

# print the results
print('results: ')
for result in results:
    print(result)
    print()
                    </code></pre>
                </div>
            </div>
        </div>
    </section>

    <footer>
        <div class="container">
            <p>NeopadAI &copy; 2024 - Redefining the Future of Fast and Easy Search</p>
            <div class="social-links">
                <a href="#" aria-label="Facebook">&#xf39e;</a>
                <a href="#" aria-label="Twitter">&#xf099;</a>
                <a href="#" aria-label="LinkedIn">&#xf0e1;</a>
                <a href="#" aria-label="GitHub">&#xf09b;</a>
            </div>
        </div>
    </footer>

    <script>
        gsap.registerPlugin(ScrollTrigger);

        document.addEventListener('DOMContentLoaded', (event) => {
            gsap.from("header", {duration: 1, y: -60, opacity: 0, ease: "power3.out"});
            
            gsap.from("#showcase h1", {
                duration: 1,
                y: 50,
                opacity: 0,
                ease: "power3.out",
                delay: 0.5
            });
            
            gsap.from("#showcase p", {
                duration: 1,
                y: 50,
                opacity: 0,
                ease: "power3.out",
                delay: 0.7
            });
            
            gsap.from("#showcase .btn", {
                duration: 1,
                y: 50,
                opacity: 0,
                ease: "power3.out",
                delay: 0.9
            });

            gsap.from(".feature", {
                duration: 1,
                opacity: 0,
                y: 50,
                stagger: 0.2,
                ease: "power3.out",
                scrollTrigger: {
                    trigger: "#features",
                    start: "top 80%",
                }
            });

            gsap.from(".demo-window", {
                duration: 1,
                opacity: 0,
                y: 50,
                ease: "power3.out",
                scrollTrigger: {
                    trigger: "#demo",
                    start: "top 80%",
                }
            });

            // Shrink header on scroll
            ScrollTrigger.create({
                start: "top -80",
                end: 99999,
                toggleClass: {className: 'smaller', targets: 'header'}
            });
        });
    </script>
</body>
</html>
"""

HTML_START_TEMPLATE = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ai-search Chat - NeopadAI</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/axios/0.21.1/axios.min.js"></script>
    <style>
        :root {
            --primary-color: #2d8fd5;
            --background-color: #343541;
            --text-color: #ececf1;
            --border-color: #565869;
            --sidebar-color: #202123;
            --input-background: #40414f;
            --result-background: #444654;
        }
        body {
            font-family: 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
            background-color: var(--background-color);
            color: var(--text-color);
            display: flex;
            margin: 0;
            padding: 0;
            height: 100vh;
            transition: background-color 0.3s, color 0.3s;
        }
        .sidebar {
            width: 260px;
            background-color: var(--sidebar-color);
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
        }
        .main-content {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            padding: 20px;
            overflow-y: auto;
        }
        .search-container {
            max-width: 800px;
            margin: 0 auto;
            width: 100%;
        }
        h1 {
            color: var(--primary-color);
            margin-bottom: 1.5rem;
            font-size: 2rem;
            text-align: center;
        }
        .search-box {
            display: flex;
            margin-bottom: 1rem;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }
        #searchInput {
            flex-grow: 1;
            padding: 0.8rem;
            font-size: 1rem;
            border: 1px solid var(--border-color);
            border-radius: 4px 0 0 4px;
            outline: none;
            background-color: var(--input-background);
            color: var(--text-color);
        }
        #searchButton {
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 0.8rem 1.5rem;
            font-size: 1rem;
            cursor: pointer;
            border-radius: 0 4px 4px 0;
            transition: background-color 0.3s;
        }
        #searchButton:hover {
            background-color: #256aa8;
        }
        #result {
            background-color: var(--result-background);
            padding: 1.5rem;
            border-radius: 8px;
            white-space: pre-wrap;
            word-break: break-word;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
            margin-top: 1.5rem;
        }
        .loading {
            text-align: center;
            color: var(--primary-color);
            font-style: italic;
        }
        .history-item {
            cursor: pointer;
            padding: 10px;
            margin-bottom: 5px;
            background-color: var(--input-background);
            border-radius: 4px;
            transition: background-color 0.3s;
        }
        .history-item:hover {
            background-color: var(--border-color);
        }
        #themeToggle {
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 10px;
            margin-top: auto;
            cursor: pointer;
            border-radius: 4px;
            transition: background-color 0.3s;
        }
        #themeToggle:hover {
            background-color: #256aa8;
        }
        body.light-theme {
            --background-color: #f7f7f8;
            --text-color: #343541;
            --border-color: #d9d9e3;
            --sidebar-color: #f7f7f8;
            --input-background: #ffffff;
            --result-background: #ffffff;
        }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>Research History</h2>
        <div id="searchHistory"></div>
    </div>
    <div class="main-content">
        <div class="search-container">
            <h1>ai-search NeopadAI</h1>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="Enter your prompt...">
                <button id="searchButton">Search</button>
            </div>
            <div id="result"></div>
        </div>
    </div>

    <script>
        const searchInput = document.getElementById('searchInput');
        const searchButton = document.getElementById('searchButton');
        const result = document.getElementById('result');
        const searchHistory = document.getElementById('searchHistory');
        const themeToggle = document.getElementById('themeToggle');
        let history = [];

        async function search(text) {
            result.innerHTML = '<p class="loading">Searching...</p>';
            try {
                const response = await axios.post('/api/search', { text });
                return response.data.result;
            } catch (error) {
                console.error('Error searching:', error);
                return 'An error occurred while searching.';
            }
        }

        async function handleSearch() {
            const text = searchInput.value.trim();
            if (text) {
                const searchResult = await search(text);
                result.textContent = searchResult;
                addToHistory(text);
            } else {
                result.textContent = 'Please enter a valid prompt.';
            }
        }

        function addToHistory(text) {
            if (!history.includes(text)) {
                history.unshift(text);
                if (history.length > 10) {
                    history.pop();
                }
                updateHistoryDisplay();
            }
        }

        function updateHistoryDisplay() {
            searchHistory.innerHTML = '';
            history.forEach(item => {
                const historyItem = document.createElement('div');
                historyItem.classList.add('history-item');
                historyItem.textContent = item;
                historyItem.addEventListener('click', () => {
                    searchInput.value = item;
                    handleSearch();
                });
                searchHistory.appendChild(historyItem);
            });
        }

        function toggleTheme() {
            document.body.classList.toggle('light-theme');
        }

        searchButton.addEventListener('click', handleSearch);
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                handleSearch();
            }
        });
        themeToggle.addEventListener('click', toggleTheme);
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)