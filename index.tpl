<!DOCTYPE html>
<html lang="zh_CN">

<head>
    <meta charset="UTF-8">
    <title>曲春光电影收藏</title>
    <style type="text/css">
    h1 {
        color: #111;
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 70px;
        font-weight: bold;
        letter-spacing: -1px;
        line-height: 1;
        text-align: center;
    }

    h2 {
        font-family: sans-serif;
    }

    .list {
        font-family: sans-serif;
        margin: 0;
        padding: 20px 0 0;
    }

    .list > li {
        display: block;
        background-color: #eee;
        padding: 10px;
        box-shadow: inset 0 1px 0 #fff;
        min-height: 150px;
    }

    .avatar {
        max-width: 150px;
    }

    img {
        max-width: 100%;
    }

    h3 {
        font-size: 16px;
        margin: 0 0 0.3rem;
        font-weight: normal;
        font-weight: bold;
    }

    p {
        margin: 0;
    }

    input {
        border: solid 1px #ccc;
        border-radius: 5px;
        padding: 7px 14px;
        margin-bottom: 10px
    }

    input:focus {
        outline: none;
        border-color: #aaa;
    }

    .sort {
        padding: 8px 30px;
        border-radius: 6px;
        border: none;
        display: inline-block;
        color: #fff;
        text-decoration: none;
        background-color: #28a8e0;
        height: 30px;
    }

    .sort:hover {
        text-decoration: none;
        background-color: #1b8aba;
    }

    .sort:focus {
        outline: none;
    }

    .sort:after {
        width: 0;
        height: 0;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-bottom: 5px solid transparent;
        content: "";
        position: relative;
        top: -10px;
        right: -5px;
    }

    .sort.asc:after {
        width: 0;
        height: 0;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid #fff;
        content: "";
        position: relative;
        top: 13px;
        right: -5px;
    }

    .sort.desc:after {
        width: 0;
        height: 0;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-bottom: 5px solid #fff;
        content: "";
        position: relative;
        top: -10px;
        right: -5px;
    }

    .thumb {
        width: 100px;
        height: 148px;
        float: left;
        margin-right: 20px;
        border: solid 1px #333;
    }
    </style>
</head>

<body>
    <h1>曲春光电影收藏</h1>
    <div id="users">
        <input class="search" placeholder="搜索题名或年份" />
        <button class="sort" data-sort="name">
            按名字排序
        </button>
        <p>说明：搜索可以输入题名或年份的任意部分内容，下面列表将即时返回过滤结果。</p>
        <ul class="list">
{{ITERATOR_ITEMS}}
        </ul>
    </div>
    <script src="http://cdn.bootcss.com/jquery/3.0.0-beta1/jquery.js"></script>
    <script src="http://cdn.bootcss.com/list.js/1.1.1/list.min.js"></script>
    <script>
    var options = {
        valueNames: ['name', 'born']
    };
    var userList = new List('users', options);
    </script>
</body>

</html>
