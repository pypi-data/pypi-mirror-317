from .searcher import RealTimeGoogleSearchProvider

import sys

def check_os_sys():
    if sys.platform.startswith('win'):
        return "Windows"
    elif sys.platform.startswith('linux'):
        return "Linux"
    else:
        return "Other OS"



def bing(query: list | str, max_urls=50, animation=False,
           chromedriver_path=None,
           search_provider="bing",
         min_waiting_time:int=2):
    return google(
        query=query,
        max_urls=max_urls,
        animation=animation,
        chromedriver_path=chromedriver_path,
        search_provider=search_provider,
        min_waiting_time=min_waiting_time
    )
def google(query: list | str, max_urls=50, animation=False,
           chromedriver_path=None,
           search_provider="google",
           min_waiting_time:int=2):
    if chromedriver_path is None:
        cur_sys = check_os_sys()
        chromedriver_path = "/usr/local/bin/chromedriver" if cur_sys == 'Linux' else r"C:\Users\chromedriver-win64\chromedriver.exe"

    search = RealTimeGoogleSearchProvider(animation=animation,
                                          chromedriver_path=chromedriver_path,
                                          search_provider=search_provider
                                          )

    if isinstance(query, list):
        import threading
        results = []

        def search_query(q):
            results.append(search.search(q, max_urls=max_urls,min_waiting_time=min_waiting_time))

        threads = [threading.Thread(target=search_query, args=(q,)) for q in query]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return results
    else:
        return search.search(query, max_urls=max_urls,min_waiting_time=min_waiting_time)

# def google(query,max_urls=50,animation=False,
#            chromedriver_path=None):
#     if chromedriver_path is None:
#         cur_sys = check_os_sys()
#         chromedriver_path = "/usr/local/bin/chromedriver" if cur_sys == 'Linux' else r"C:\Users\chromedriver-win64\chromedriver.exe"
#
#     search = RealTimeGoogleSearchProvider(animation=animation,
#                                           chromedriver_path=chromedriver_path)
#     return search.search(query,max_urls=max_urls)
#
#
# def bing(query,max_urls=50,animation=False,
#          chromedriver_path=None):
#     if chromedriver_path is None:
#         cur_sys = check_os_sys()
#         chromedriver_path = "/usr/local/bin/chromedriver" if cur_sys=='Linux' else r"C:\Users\chromedriver-win64\chromedriver.exe"
#     search = RealTimeGoogleSearchProvider(search_provider="bing",
#                                           animation=animation,
#                                           chromedriver_path=chromedriver_path)
#     return search.search(query, max_urls=max_urls)