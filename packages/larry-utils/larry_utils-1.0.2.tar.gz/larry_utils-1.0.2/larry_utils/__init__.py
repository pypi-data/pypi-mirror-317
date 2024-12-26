from PIL import Image
import io
import json
import logging
from logging import FileHandler
import pickle 
import threading



def get_logger(logger_path: str = './logger',
               logger_name: str = 'video-fps',
               drop_console_handler: bool = False):

    # initialize logger
    logger = logging.getLogger(logger_name)
    # set level: NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler = FileHandler(filename=logger_path)


    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if not drop_console_handler:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger



def read_bytes(file_name, start_num, size, is_image=True):
    with open(file_name, 'rb') as f:
        f.seek(start_num)
        image = f.read(size)
    if is_image:
        image = Image.open(io.BytesIO(image))
    return image


def save_image_bytes(file_name, start_num, size, savename):
    try:
        x = read_bytes(file_name, start_num, size)
        with open(savename, 'wb') as f:
            f.write(x)
        return True
    except Exception as e:
        print(e)
        return False



def read_json(file_path):
    d = open(file_path).read().split('\n')
    res = []
    for line in d:
        try:
            res.append(json.loads(line))
        except:
            continue
    print('all {} lines, success {} lines'.format(len(d), len(res)))

    return res

def write_json(file_path, dat, mode='a'):
    with open(file_path, mode) as f:
        for i in dat:
            f.write(json.dumps(i, ensure_ascii=False) + '\n')

def read_pkl(file_path):
    import pickle 
    return pickle.loads(open(file_path, 'rb').read())

def write_pkl(file_path, d):
    import pickle
    with open(file_path, 'wb') as f:
        f.write(pickle.dumps(d))



def get_resolution(resolution):
    resolutions = [('16:9', 16./9), ('4:3', 4./3), ('1:1', 1), ('3:4', 3./4), ('9:16', 9./16)]
 
    Bmatch, Bdistance = '', 19
    ratio = resolution[0] / resolution[1]
    if True:
        for match, distance in resolutions:
            if abs(ratio - distance) < Bdistance:
                Bmatch = match
                Bdistance = abs(ratio - distance)
    return Bmatch


def hash(x):
    import hashlib
    return hashlib.md5(x.encode()).hexdigest()



def read_excel(file_path, is_ordered=False):
    import pandas as pd
    from collections import OrderedDict

    if '.xlsx' in file_path:
        # org = pd.read_excel(file_path).to_dict()
        xl = pd.ExcelFile(file_path)
        sheet_names = xl.sheet_names

        all_d = []
        for sheet_name in sheet_names:
            org = xl.parse(sheet_name)
            keys = org.keys()

            N = len(org[list(org.keys())[0]])

            dat = []
            for i in range(N):
                if is_ordered:
                    line = OrderedDict()
                else:
                    line = {}
                for k in keys:
                    line[k] = org[k][i]
                dat.append(line)
            all_d.append([sheet_name, dat])

        if len(all_d) == 1:
            return all_d[0][1]
        else:
            return all_d

         
    else:
        org = pd.read_csv(file_path).to_dict()
        keys = org.keys()

        N = len(org[list(org.keys())[0]])

        dat = []
        for i in range(N):
            if is_ordered:
                line = OrderedDict()
            else:
                line = {}
            for k in keys:
                line[k] = org[k][i]
            dat.append(line)

        return dat



def write_excel(file_path, dat):
    import pandas as pd
    pd.DataFrame(dat).to_csv(file_path)



def include_str_and(line, *args):
    for _ in args:
        if _ not in line:
            return False

    return True

def include_str_or(line, *args):
    for _ in args:
        if _  in line:
            return True

    return False



def sbs_html(msg1, msg2=[], savename='./t.html'):
    pattern = '''

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Conversation Layout with Vertical Separator</title>
  <style>
    /* 全局：黑体，字号15px */
    body {
      font-family: "SimHei","黑体", sans-serif;
      font-size: 15px;
      margin: 0;
      padding: 0;
    }

    /* 页面容器：左右两列，中间竖线分隔
       重点：align-items: stretch 让所有子元素(含separator)自适应父容器高度 */
    .container {
      display: flex;
      align-items: stretch;  /* 让左右两列+分隔条都被拉伸到相同高度 */
      justify-content: center;
      margin: 20px;
    }

    /* 左列、右列 */
    .left-column, .right-column {
      flex: 1;                     /* 各占剩余空间 */
      display: flex;
      flex-direction: column;      /* 垂直排列对话 */
    }

    /* 中间竖线分隔条 */
    .separator {
      width: 2px;
      background-color: #888;
      margin: 0 20px;
      align-self: stretch;         /* 自己也要被拉伸，撑满容器可用高度 */
    }

    /* 左侧、右侧顶部标题 */
    .title-left, .title-right {
      font-weight: bold;
      margin-bottom: 10px;
    }

    /* 每条对话的整体容器（含角色行 + 对话框） */
    .dialog-item {
      margin-bottom: 20px; /* 每条对话的下间距 */
    }

    /* 角色行：放在对话框上方，user左对齐，assistant右对齐 */
    .role-line {
      margin-bottom: 5px;
    }
    .role-line strong {
      font-family: "SimSun","宋体", serif; /* 使用宋体，加粗、加黑 */
      font-weight: bold;
      color: #000;
    }
    .user-line {
      text-align: left;    /* “user”在左侧 */
    }
    .assistant-line {
      text-align: right;   /* “assistant”在右侧 */
    }

    /* 对话框公共样式 */
    .dialog-box {
      border: 1px solid #ccc;
      border-radius: 5px;
      padding: 10px;
      transition: transform 0.2s, box-shadow 0.2s;
      word-wrap: break-word; /* 长文本自动换行 */
    }

    /* user：左对齐，浅绿色背景，不浮动 */
    .user {
      background-color: #d2f5d2; /* 微信浅绿色示例 */
      text-align: left;
    }

    /* assistant：浅灰色，鼠标悬浮时浮动 + 内部文字左对齐 */
    .assistant {
      background-color: #f8f8f8; /* 浅浅灰色 */
      text-align: left;
    }
    /* assistant 悬浮 */
    .assistant:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }

    /* Markdown内容默认样式微调 */
    .markdown-content p {
      margin: 0.5em 0;
    }
  </style>
</head>
<body>

<div class="container">
  <!-- 左侧列 -->
  <div class="left-column">
    <div class="title-left">hunyuan</div>
    <div id="left-conversations"></div>
  </div>

  <!-- 中间竖线 -->
  <div class="separator"></div>

  <!-- 右侧列 -->
  <div class="right-column">
    <div class="title-right">doubao-1210</div>
    <div id="right-conversations"></div>
  </div>
</div>

<!-- 引入 Marked.js 用于渲染 Markdown -->
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

<script>
/**
 * 对话数据，分 left / right
 *   role: 'user'或'assistant'
 *   content: Markdown字符串
 */
const conversations = {
  left: __LEFT__,
  right: __RIGHT__};

/**
 * 渲染对话
 * @param {string} containerId - 容器ID
 * @param {Array} dialogList - 对话数组 [{ role, content }, ...]
 */
function renderConversations(containerId, dialogList) {
  const container = document.getElementById(containerId);
  
  dialogList.forEach(item => {
    const dialogItem = document.createElement('div');
    dialogItem.classList.add('dialog-item');

    // 角色行
    const roleLine = document.createElement('div');
    roleLine.classList.add('role-line');
    if (item.role === 'user') {
      roleLine.classList.add('user-line');
      roleLine.innerHTML = `<strong>user</strong>`;
    } else {
      roleLine.classList.add('assistant-line');
      roleLine.innerHTML = `<strong>assistant</strong>`;
    }

    // 对话框
    const dialogBox = document.createElement('div');
    dialogBox.classList.add('dialog-box', item.role);

    // Markdown内容
    const mdDiv = document.createElement('div');
    mdDiv.classList.add('markdown-content');
    mdDiv.dataset.md = item.content; // 存放MD文本

    dialogBox.appendChild(mdDiv);
    dialogItem.appendChild(roleLine);
    dialogItem.appendChild(dialogBox);
    container.appendChild(dialogItem);
  });
}

/** 用 Marked.js 将 data-md 中的 Markdown 转为 HTML */
function applyMarkdown() {
  document.querySelectorAll('.markdown-content').forEach(el => {
    const mdText = el.dataset.md || '';
    el.innerHTML = marked.parse(mdText);
  });
}

// 分别渲染左、右列对话
renderConversations('left-conversations', conversations.left);
renderConversations('right-conversations', conversations.right);

// 最后执行 Markdown 转换
applyMarkdown();
</script>

</body>
</html>
'''
    a = pattern.replace('__LEFT__', eval(msg1)).replace('__RIGHT__', eval(msg2))
    with open(savename, 'w') as f:
        f.write(a)


