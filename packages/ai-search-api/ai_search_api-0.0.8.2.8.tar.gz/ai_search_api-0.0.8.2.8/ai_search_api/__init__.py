import ai_search_api.ai_search as ai

def update():
    import ai_search_api.update
    return "updating..."
    
def _error(page, error_type):
    import ai_search_api.error
    import webbrowser

    # URL della pagina web da aprire
    url = "localhost:5000/" + str(error_type) + "/" + str(page)

    # Apre la pagina nel browser predefinito
    webbrowser.open(url)


def localMode():
    # import ai_search_api.local
    _error('local', '404')
    return "localMode..."
    
def request(text):
    # set the request
    ai.req = text
    ai.run()
    results = ai.result
    ai.result = []

    # print the results
    return results