import re
import asyncio
from pathlib import Path
from typing import List
from .optimized_multi_query_searcher import OptimizedMultiQuerySearcher

class RealTimeGoogleSearchProvider:
    def __init__(
        self,
        search_provider="google",
        chromedriver_path="/usr/local/bin/chromedriver",
        max_workers=None,
        animation = False
    ):
        self.search_provider = search_provider
        self.chromedriver_path = chromedriver_path
        self.max_workers = max_workers
        self.animation = animation


    def search(self, query: str,max_urls=50, min_waiting_time:int=2) -> List[str]:
        with OptimizedMultiQuerySearcher(chromedriver_path=self.chromedriver_path,
                                                    max_workers=self.max_workers,
                                                    animation=self.animation) as searcher:
            res = searcher.search_single_query(query, search_provider=self.search_provider,
                                               min_waiting_time=min_waiting_time)
            # print("@@@@@")
            # Path('goolge_page_source.txt').write_text(res.page_source)
            return res.urls[:max_urls]


    async def _async_batch_search(self, batch_queries,max_urls=50) -> List[str]:
        with OptimizedMultiQuerySearcher(chromedriver_path=self.chromedriver_path,
                                         max_workers=self.max_workers,
                                         animation=self.animation) as searcher:
            all_urls = await searcher.search_multiple_queries(
                queries=batch_queries,
                search_provider=self.search_provider
            )
            all_urls = [url.urls for url in all_urls]
            filtered_urls = [y for x in zip(*all_urls) for y in x]
            filtered_urls = [self._extract_until_hash(x) if self._is_hash(x) else x for x in filtered_urls]
            filtered_urls = [_ for _ in filtered_urls if _]
            duplicate_removed_urls = self._remove_duplicate_urls(filtered_urls)
            return duplicate_removed_urls[:max_urls]

    def search_batch(self, batch_queries,max_urls=50) -> List[str]:
        return asyncio.run(self._async_batch_search(batch_queries,max_urls=max_urls))


    def __call__(self, query:str|list,*args, **kwargs):
        if isinstance(query,str):
            return self.search(query,*args,**kwargs)
        return self.search_batch(query,*args,**kwargs)

    def _is_hash(self, x):
        return '#' in x

    def _extract_until_hash(self, x):
        results = re.findall(r'(.*)#',x)
        if results:
            return results[0]
        return ""

    def _remove_duplicate_urls(self, filtered_urls):
        """Remove duplicates  by maintaining order"""
        seen = set()
        seen_add = seen.add
        return [x for x in filtered_urls if not (x in seen or seen_add(x))]




if __name__ == '__main__':
    s = RealTimeGoogleSearchProvider(animation=True)
    print(s.search("who is modi?"))