import asyncio
from dataclasses import dataclass
from io import BytesIO
from typing import List, Tuple

import PyPDF2
import aiohttp
from tqdm import tqdm
from .html_parser import FastHTMLParserV3

from .yt_parser import YoutubeExtractor

@dataclass
class FastParserResult:
    url: str
    content:str

class FastParser:
    def __init__(self,extract_pdf=True,
                 allow_youtube_urls_extraction=False,
                 arxiv_html_flag=False):
        self.extract_pdf = extract_pdf
        self.allow_youtube_urls_extraction=allow_youtube_urls_extraction
        self.arxiv_html_flag = arxiv_html_flag

    def fetch(self,url:str):
        res = self.fetch_batch([url])
        return FastParserResult(url=url,content=res[0].content if res else "")

    def fetch_batch(self, urls: list) -> List[FastParserResult]:
        return asyncio.run(self._async_html_parser(urls))

    async def afetch_batch(self, urls: list) -> List[FastParserResult]:
        return await self._async_html_parser(urls)

    async def afetch(self,url:str):
        res = await self.afetch_batch([url])
        return FastParserResult(url=url,content=res[0][1] if res else "")

    async def aparse(self, urls: str|list,*args, **kwargs) -> FastParserResult|List[FastParserResult]:
        if isinstance(urls,str):
            return await self.afetch(urls)
        return await self.afetch_batch(urls)

    def __call__(self, urls: str|list,*args, **kwargs) -> FastParserResult|List[FastParserResult]:
        if isinstance(urls,str):
            return self.fetch(urls)
        return self.fetch_batch(urls)

    async def _async_html_parser(self, urls) -> List[FastParserResult]:
        html_urls = []
        pdf_urls = []
        yt_urls = []
        for url in tqdm(urls,desc = "processing urls",unit = 'url'):
            url = self._arxiv_url_fix(url)
            if '/pdf' in url or url.lower().endswith('.pdf'):
                pdf_urls.append(url)
            elif 'youtube' in url:
                yt_urls.append(url)
            else:
                html_urls.append(url)

        results:List = []

        html_urls = list(dict.fromkeys(html_urls))
        pdf_urls = list(dict.fromkeys(pdf_urls))
        yt_urls = list(dict.fromkeys(yt_urls))

        if html_urls:
            fetcher = FastHTMLParserV3()
            html_results = await fetcher.fetch_content(urls=html_urls)
            results.extend(list(zip(html_urls,html_results)))

        if pdf_urls and self.extract_pdf:
            pdf_results = await self._fetch_pdf_content(pdf_urls)
            results.extend(list(zip(pdf_urls,pdf_results)))

        if self.allow_youtube_urls_extraction:
            yt_results = YoutubeExtractor.extract(urls = yt_urls)
            results.extend(list(zip(yt_urls,yt_results)))

        result_v1 = [FastParserResult(url=u,content=c) for u,c in results]
        return result_v1

    async def _fetch_pdf_content(self, pdf_urls):
        async def fetch_pdf(session, url):
            async with session.get(url) as response:
                if response.status == 200:
                    pdf_content = await response.read()
                    pdf_file = BytesIO(pdf_content)
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                    return text
                else:
                    return ""

        async with aiohttp.ClientSession() as session:
            tasks = [fetch_pdf(session, url) for url in pdf_urls]
            results = await asyncio.gather(*tasks)
            return results

    def _arxiv_url_fix(self, url):
        if 'https://arxiv.org/abs/' in url and self.extract_pdf:
            return url.replace('https://arxiv.org/abs/', 'https://arxiv.org/pdf/')
        elif 'http://arxiv.org/html/' in url:
            if self.arxiv_html_flag: #default False
                return url.replace('http://arxiv.org/html/', 'https://arxiv.org/abs/')
            else:
                return url.replace('http://arxiv.org/html/', 'https://arxiv.org/pdf/')
        else:
            return url


def parse(urls: list | str, allow_pdf_extraction=True,
          allow_youtube_urls_extraction=False, arxiv_html_flag=False) -> List[FastParserResult] | FastParserResult:
    parser = FastParser(extract_pdf=allow_pdf_extraction,
                        allow_youtube_urls_extraction=allow_youtube_urls_extraction,
                        arxiv_html_flag=arxiv_html_flag)
    return parser(urls)

async def aparse(urls: list | str, allow_pdf_extraction=True,
          allow_youtube_urls_extraction=False, arxiv_html_flag=False) -> List[FastParserResult] | FastParserResult:
    parser = FastParser(extract_pdf=allow_pdf_extraction,
                        allow_youtube_urls_extraction=allow_youtube_urls_extraction,
                        arxiv_html_flag=arxiv_html_flag)
    return await parser.aparse(urls)

