import readdocument

from langchain.text_splitter import  RecursiveCharacterTextSplitter

# 知识库中单段文本长度
CHUNK_SIZE = 500

# 知识库中相邻文本重合长度
OVERLAP_SIZE = 50

doc_type,docs=readdocument.load_pdf_document("F:/repository/git_repository/book/技术/appserver/宝兰德/BES AppServer 应用服务器中间件企业版用户手册V9.5.pdf")


text_splitter =RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE,chunk_overlap=OVERLAP_SIZE)


text_list=text_splitter.split_text(docs[0].page_content[0:1000])

for temp in text_list:
    print(temp)
    print(f"===================无敌分割线=========================")


docu_list=text_splitter.split_documents(docs)
print(f"切分后的文件数量：{len(docu_list)}")



print(f"切分后的字符数（可以用来大致评估 token 数）：{sum([len(doc.page_content) for doc in docu_list])}")




