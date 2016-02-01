# coding: utf-8
import os
import urllib2
import json
import socket
import time


# Pair of your host name and base path.
#
# Ignore generate the file list and trying to using the exist filelist_file,
# if your host name not list in it or the bash_path not exist.
#
# It is useful when using generate data file from other machine.
# A Raspberry Pi, for example.
base_path_by_host = {
    "kevin3": ur"D:\movie\09_欧美电影576p",
    "kevin6": ur"D:\video\movie"
}

library_file = ur"library.json"
filelist_file = ur"filelist.json"
api_search_base = ur'https://api.douban.com/v2/movie/search?q='
api_subject_base = ur'https://api.douban.com/v2/movie/subject/'
page_subject_base = ur'http://movie.douban.com/subject/'

# Global library of select informations of my movies.
library = []


def readJson(filename):
    """
    Get data from JSON file
    """
    if not os.path.exists(filename):
        return []
    fp = open(filename, "r")
    obj = json.load(fp)
    fp.close()
    return obj


def writeJson(filename, obj):
    """
    Write out data to JSON file.
    BUG of python: json.dump(encoding='utf-8') do not convert unicode to utf-8.
    using json.dumps() and fp.write() instead.
    """
    fp = open(filename, "w")
    s = json.dumps(obj, fp,
                   indent=4,
                   sort_keys=True,
                   ensure_ascii=False,
                   encoding='utf-8')
    fp.write(s.encode('utf-8'))
    fp.close()


def getTitle(filename):
    """
    Return movie's Chinese name from its file name.

    By default, it get the string directly after the year.
    That means the filename may looks like,
        "A.Beautiful.Mind.2001.美丽心灵.双语字幕.mkv"
    """
    segs = filename.split('.')
    for i, sub in enumerate(segs):
        if sub.isdigit() and len(sub) == 4 and \
           (sub.startswith("19") or sub.startswith("20")):
            return segs[i+1]

    print "[WARN] Can not get title. file:", filename.encode("utf-8")
    return ""


def requestJson(url):
    '''
    Douban limit 150 access/h without access token and 500 access/h with token.
    '''
    # When the limit is reached, raise exception here
    response = urllib2.urlopen(url.encode('utf-8'))

    if response.code != 200:
        print "[WARN] Get data failed."
        return None
    else:
        results = json.loads(response.read())
        response.close()
        return results


def genFileList(base_path):
    exts = [".mkv", ".avi", ".rmvb"]
    filelist = []

    for filename in os.listdir(base_path):
        p = os.path.join(base_path, filename)
        if os.path.isdir(p) or not any(map(filename.endswith, exts)):
            continue
        filelist.append(p)

    writeJson(filelist_file, filelist)


def genDelta():
    """
    Generate movie info. Ignore those already in the local library.
    """
    global library

    filelist = readJson(filelist_file)
    for filename in filelist:
        movie_info = genOne(filename)
        if movie_info is not None:
            print "[INFO] New movie:", filename.encode("utf-8")
            library.append(movie_info)


def exist(title):
    for item in library:
        if item["title"] == title:
            return True
    return False


def genOne(filename):
    """
    Generate movie information from DouBan Movie by given filename.
    """
    # Get Chinese title from filename.
    title = getTitle(filename)
    if title == "" or exist(title):
        return None

    # Search movie by title.
    search = requestJson(api_search_base + title)
    if search is None or len(search["subjects"]) == 0:
        print "[WARN] Can not find this movie,"
        return None
    writeJson(ur"搜索结果\搜索结果_" + title + ".json", search)

    # Get first id of movie.
    first_id = search["subjects"][0]["id"]

    # Get title,summary of first searching result.
    movie = requestJson(api_subject_base + first_id)
    if movie is None:
        return None
    writeJson(ur"电影信息\电影信息_" + title + ".json", movie)

    # Generate Object and return.
    obj = {}
    obj["id"] = first_id
    obj["title"] = title
    obj["filename"] = filename
    obj["summary"] = movie["summary"]
    obj["year"] = movie["year"]
    obj["image"] = movie["images"]["medium"]

    return obj


def genItems(target):
    """
    Format of a item:

    <li>
        <img src="https://img1.doubanio.com/view/movie_poster_cover/spst/public/p477610353.jpg" class="thumb" alt="" />
        <h3 class="name"><a href="http://movie.douban.com/subject/6873250/">爱在招生部</a></h3>
        <p class="born">2013</p>
        <p>大学同学约翰（保罗·路德 Paul Rudd 饰）的来电让柏迪亚（蒂娜·菲 Tina Fey 饰）十分意外，电话中，约翰邀请柏迪亚参观他所在的学校，作为同行，柏迪亚欣然前往。约翰的学校给作风保守古板的柏迪亚带来了很大的震撼，一些小小的改变在她的观念中逐渐形成。</p>
        <p>约翰此次发出邀请其实还有另外一个目的，他发现自己学校中一位名叫杰瑞玛（纳特·沃尔夫 Nat Wolff 饰）的学生很可能和柏迪亚有着一段古老的渊源。果不其然，当柏迪亚看到杰瑞玛时，她感到内心里涌现出了一种特殊的感情。与此同时，她和约翰之间的距离也越来越近，幸福，在不经意间造访了这个善良的女人。</p>
    </li>
    """
    for item in library:
        s = "<li>\n"
        s += '<img src="' + item["image"] + '" class="thumb" alt="" />'
        s += '<h3 class="name"><a href="' + page_subject_base + item["id"]
        s += '">' + item["title"] + '</a></h3>'
        s += '<p class="born">' + item["year"] + '</p>'
        s += '<p>' + item["summary"] + '</p>'
        s += "</li>\n"
        target.write(s.encode("utf8"))


def genHTML():
    """
    Generate index.html file by reference the library.
    """
    tpl = open(ur"index.tpl", "r")
    target = open(ur"index.html", "w")
    for line in tpl:
        if line == "{{ITERATOR_ITEMS}}\n":
            genItems(target)
        else:
            target.write(line)
    tpl.close()
    target.close()


def main():
    if socket.gethostname() in base_path_by_host:
        base_path = base_path_by_host[socket.gethostname()]
        if base_path != "" and os.path.exists(base_path):
            genFileList(base_path)

    global library
    library = readJson(library_file)

    while True:
        try:
            genDelta()
            break
        except Exception:
            writeJson(library_file, library)
            print "[WARN] Access limit of Douban reached. Sleep 1 hour ..."
            time.sleep(3600)

    writeJson(library_file, library)
    genHTML()


if __name__ == '__main__':
    main()
