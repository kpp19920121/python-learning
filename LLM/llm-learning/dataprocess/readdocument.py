import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.markdown import UnstructuredMarkdownLoader
from pathlib import Path

from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders.excel import UnstructuredExcelLoader

from langchain_community.document_loaders.word_document import UnstructuredWordDocumentLoader

from langchain_community.document_loaders.image import UnstructuredImageLoader

import threading
import chardet
import subprocess


def load_pdf_document(file_path: str) -> dict:
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    if not docs or len(docs) <= 0:
        raise ValueError("无法正确解析文档，请联系系统管理员!")
    return ("pdf", docs)


def load_md_doccument(file_path: str) -> dict:
    os.environ['AUTO_DOWNLOAD_NLTK'] = "False"

    loader = UnstructuredMarkdownLoader(file_path)
    docs = loader.load()
    if not docs or len(docs) <= 0:
        raise ValueError("无法正确解析文档，请联系系统管理员!")
    return ("md", docs)


def load_text_doccument(file_path: str) -> dict:
    loader = TextLoader(file_path, encoding="UTF-8")
    docs = loader.load()
    if not docs or len(docs) <= 0:
        raise ValueError("无法正确解析文档，请联系系统管理员!")
    return ("txt", docs)


def load_excel_doccument(file_path: str) -> dict:
    loader = UnstructuredExcelLoader(file_path)
    docs = loader.load()

    if not docs or len(docs) <= 0:
        raise ValueError("无法正确解析文档，请联系系统管理员!")
    return ("xlsx", docs)


def load_word_doccument(file_path: str) -> dict:
    try:
        new_file_path = file_path

        if Path(file_path).suffix[1:] == "doc":
            new_file_path = file_path.replace(".doc", ".docx")
            if os.name == 'nt':
                subprocess.run(['soffice', '--headless', '--convert-to', 'docx','--outdir', os.path.dirname(file_path),file_path], check=True)
            else:
                subprocess.run(['libreoffice', '--headless', '--convert-to', 'docx','--outdir', os.path.dirname(file_path),file_path], check=True)


        loader = UnstructuredWordDocumentLoader(new_file_path)
        docs = loader.load()

        if not docs or len(docs) <= 0:
            raise ValueError("无法正确解析文档，请联系系统管理员!")

        if Path(file_path).suffix[1:] == "doc":  os.remove(new_file_path)


        return ("docx", docs)
    except UnicodeDecodeError as e:
        print(f"解析文档{file_path}报错，字符集不匹配，开始匹配正确的字符集！")
        loader = UnstructuredWordDocumentLoader(file_path)
        docs = loader.load()

        if not docs or len(docs) <= 0:
            raise ValueError("无法正确解析文档，请联系系统管理员!")
        return ("docx", docs)


def load_image_doccument(file_path) -> dict:
    loader = UnstructuredImageLoader(file_path)
    docs = loader.load()
    if not docs or len(docs) <= 0:
        raise ValueError("无法正确解析文档，请联系系统管理员!")
    return ("image", docs)


def get_processfile(file_path: str) -> dict:
    file = Path(file_path)
    # 获取文件的后缀名称
    path_suffix = file.suffix[1:]

    excluded_keywords = ["idx", "pack", "jpg", "jar", "class", "tar.gz", "tar", "gz", "zip", "~$", "tmp"]

    # 过滤文件
    if not path_suffix or any(keyword in file_path for keyword in excluded_keywords):
        return None, None
    # 过滤空文件
    if os.path.getsize(file_path) == 0:
        print("去掉文件大小为0的文件")
        return None, None

    try:
        print(f"[线程 {threading.current_thread().name}] 开始解析：{file_path}")
        match path_suffix:
            case "pdf":
                return load_pdf_document(file_path)
            case "md":
                return load_md_doccument(file_path)
            case "txt":
                return load_text_doccument(file_path)
            case "xlsx":
                return load_excel_doccument(file_path)
            case "docx" | "doc":
                return load_word_doccument(file_path)
            case "jpg":
                return load_image_doccument(file_path)
            case _:
                return load_text_doccument(file_path)
    finally:
        print(f"[线程 {threading.current_thread().name}] 解析完成：{file_path}")


file_list = {
    "pdf": (
        "F:/repository/git_repository/book/技术/appserver/宝兰德/BES AppServer 应用服务器中间件企业版用户手册V9.5.pdf",
        load_pdf_document),
    "markdown": ("F:/repository/git_repository/python-learning/LLM/nlp-web-app/readme.md", load_md_doccument),
    "text": ("C:/Users/issuser/Desktop/新建文件夹/readme.text", load_text_doccument),
    "excel": ("C:/Users/issuser/Desktop/新建文件夹/中铝需求开发计划.xlsx", load_excel_doccument)
}

if __name__ == '__main__':
    doc_type, docs = load_pdf_document(
        "F:/repository/git_repository/book/技术/appserver/宝兰德/BES AppServer 应用服务器中间件企业版用户手册V9.5.pdf")
    for temp in docs:
        print(temp.page_content)
