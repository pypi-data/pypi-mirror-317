import ai_search_api.ai_search as ai

def update():
    import ai_search_api.update
    return "updating..."
    
def localMode():
    import ai_search_api.local
    return "localMode.."
def request(text):
    # set the request
    ai.req = text
    ai.run()
    results = ai.result
    ai.result = []

    # print the results
    return results