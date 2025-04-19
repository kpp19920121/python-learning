import docx

import os
import subprocess

from langchain_community.document_loaders.word_document import  UnstructuredWordDocumentLoader

file_path="F:/repository/git_repository/document/运维/git基本操作.doc"


def load_word_doccument(file_path):


    new_file_path=file_path.replace(".doc",".docx")


    subprocess.run(['soffice', '--headless', '--convert-to', 'docx','--outdir', os.path.dirname(file_path),file_path], check=True)


    loader =UnstructuredWordDocumentLoader(new_file_path)
    docs=loader.load()

    if not docs or  len(docs)<=0:
        raise ValueError("无法正确解析文档，请联系系统管理员!")



    os.remove(new_file_path);

    return ("docx",docs)


file_type,docx=load_word_doccument(file_path)


for temp in docx:
    print(temp.page_content)