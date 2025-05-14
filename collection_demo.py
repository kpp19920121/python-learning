
import os




#基础集合
def basic_collection_demo():
    temp_list=[11,2,3,4,5,6]

    print(temp_list)

    print(temp_list[1:])


    #逆向遍历，最后一个的索引为-1
    print(temp_list[-2:])

    for temp in temp_list:
        print(temp)


    #遍历下标和索引

    for index,value in enumerate(temp_list):
        print("==========================="+str(index)+":"+str(value))


    temp_dict={'name':'张三','age':'14'}


    #遍历key
    for temp_key in temp_dict:
        print(temp_key+temp_dict[temp_key])

    #遍历value
    for temp_value in temp_dict.values():
        print(temp_value)

    #遍历key和value
    for temp_key,temp_value in temp_dict.items():
        print(temp_key+":"+temp_value)


#列表生成式
def create_new_collection():
    #生成1,11十个数字
    temp_list=list(range(1,11))
    print(temp_list)
    
    temp_list2=[temp*temp for temp in range(1,11)]

    #筛选出偶数
    temp_list3= [x for x in range(1,100) if x%2==0]

    print(temp_list3)

    #列出指定目录下的所有目录

    parent_path="F:/repository/git_repository"
    folders_list=[temp for temp in os.listdir(parent_path)]
    for temp in folders_list:
        print(os.path.join(parent_path,temp))


if __name__=='__main__':
    #basic_collection_demo()
    create_new_collection()