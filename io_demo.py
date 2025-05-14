



with open("D:/改动增量/was静默安装.txt","r",encoding="utf-8") as f:
    #print(f.read())
    for line in f.readlines():
        print(line.strip())