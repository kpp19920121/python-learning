import os
import sys
from dotenv import  load_dotenv,find_dotenv
from concurrent.futures import ThreadPoolExecutor,as_completed

from langchain_core.documents import Document

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from dataprocess import readdocument

ROOT_PATH="F:/repository/git_repository/document/运维"

#每个文件的loader
loaders = []



def get_documents(root_folder:str)->list[Document]:

    return_list=[]

    with ThreadPoolExecutor(os.cpu_count()) as executor:
        futures = []
        for dirpath, dirnames, filenames in  os.walk(ROOT_PATH):
            for tempfile in filenames:
                real_path=os.path.join(dirpath,tempfile)
                futures.append(executor.submit(readdocument.get_processfile, real_path))


        for temp_futures in as_completed(futures):
            (doc_type,docs)=temp_futures.result()
            if doc_type:
                return_list.extend(docs)

    return return_list


if  __name__=='__main__':
    documents=get_documents(ROOT_PATH)

    for temp in documents:
        print("文件元信息 => " + temp.metadata)




