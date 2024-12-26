import ai_search_api.ai_search as ai

def update():
    import ai_search_api.update
    return "updating..."
    
def _error(page, error_type):
    import webbrowser

    # URL della pagina web da aprire
    url = "http://localhost:5000/" + str(error_type) + "/" + str(page)

    # Apre la pagina nel browser predefinito
    webbrowser.open(url)
    import ai_search_api.error


def localMode():
    # import ai_search_api.local
    _error('local', '404')
    
def request(text):
    # set the request
    ai.req = text
    ai.run()
    results = ai.result
    ai.result = []

    # print the results
    return results