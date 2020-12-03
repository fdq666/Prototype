import pymysql

connection = pymysql.connect("127.0.0.1", "root", "password", "RESEARCHERS")

def fetchWordPosition(target):

    target = list(target)
    result={}
    select_str = 'SELECT WORD, ID, POSITION FROM `wordPosition` WHERE WORD in (%s)' % ','.join(['%s'] * len(target))
    with connection.cursor() as cursor:
        for i in target:
            result[i]={}
        cursor.execute(select_str, target)
        sulin = cursor.fetchall()
        for k in sulin:
            tempList = k[2].split(",")
            tempList = list(map(int, tempList))
            result[k[0]][k[1]]=tempList
    return result

def fetchKeywordValue(target):

    target = list(target)
    result={}
    select_str = 'SELECT WORD, ID, TFIDF, BM25 FROM `keywordValue` where WORD in (%s)' % ','.join(['%s'] * len(target))
    with connection.cursor() as cursor:
        for i in target:
            result[i]={}
        cursor.execute(select_str, target)
        sulin = cursor.fetchall()
        for k in sulin:
            temp = []
            temp.append(k[2])
            temp.append(k[3])
            result[k[0]][k[1]]=tuple(temp)
    return result
