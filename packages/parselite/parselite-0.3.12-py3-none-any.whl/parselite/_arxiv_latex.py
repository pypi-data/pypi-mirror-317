from typing import List

import requests
import tarfile
import tempfile
import re
import os
from io import BytesIO
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor


@dataclass
class ArxivResponse:
    url: str
    content: str

def get_latex_from_arxiv_urls(urls:List[str]|str) -> List[ArxivResponse]|ArxivResponse:

    def get_latex_from_arxiv(url):
        match = re.search(r'arxiv\.org/(?:abs|pdf)/([a-z\-]+/\d{7}|\d+\.\d+)', url)
        if not match:
            return ArxivResponse(url, None)
        arxiv_id = match.group(1)
        response = requests.get(f'https://arxiv.org/e-print/{arxiv_id}')
        if response.status_code != 200:
            return ArxivResponse(url, None)
        with tarfile.open(fileobj=BytesIO(response.content), mode='r:gz') as tar:
            temp_dir = tempfile.mkdtemp()
            tar.extractall(temp_dir)
        tex_files = [os.path.join(root, f) for root, _, files in os.walk(temp_dir) for f in files if f.endswith('.tex')]
        if not tex_files:
            return ArxivResponse(url, None)
        main_tex = max(tex_files, key=os.path.getsize)
        with open(main_tex, 'r', encoding='utf-8') as f:
            return ArxivResponse(url, f.read())

    if isinstance(urls,str):
        return get_latex_from_arxiv_urls([urls])[0]

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(get_latex_from_arxiv, urls))

    return results