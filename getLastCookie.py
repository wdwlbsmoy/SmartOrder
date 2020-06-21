import os
before_list = []
after_list = []
with open(r'D:\John\work\airtestLearning\before.txt') as fp:
    with open(r'D:\John\work\airtestLearning\after.txt') as afp:
        with open(r'D:\John\work\airtestLearning\need.txt','w',encoding='utf-8') as nfp:
            for line in fp:
                cookieDict = eval(line)
                before_list.append((cookieDict['name'],cookieDict))
            for linea in afp:
                acookieDict = eval(linea)
                after_list.append((acookieDict['name'],acookieDict))
            for cc in after_list:
                if cc[0] not in [item[0] for item in before_list]:
                    print(cc[1])
                    nfp.write(str(cc[1])+'\n')
            # for line in afp:
            #     ll = eval(line)
            #     for l in ll:
            #         print(l)