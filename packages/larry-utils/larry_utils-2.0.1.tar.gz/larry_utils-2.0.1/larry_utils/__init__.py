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
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>对话展示</title>
    <!-- 引入 Marked.js -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            font-size: 12px; /* 减小字体大小 */
            margin: 0;
            padding: 15px;
            background-color: #f9f9f9;
            position: relative;
            height: 50vh;
            box-sizing: border-box;
        }
        /* 切换开关样式 */
        .toggle-container {
            position: absolute;
            top: 20px;
            right: 20px;
            display: flex;
            align-items: center;
            font-family: "宋体", SimSun, serif;
            font-weight: bold;
            color: #333;
            z-index: 1;
        }
        .toggle-container label {
            margin-left: 10px;
            cursor: pointer;
        }
        .switch {
            position: relative;
            display: inline-block;
            width: 50px;
            height: 24px;
        }
        .switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }
        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: 0.4s;
            border-radius: 24px;
        }
        .slider:before {
            position: absolute;
            content: "";
            height: 18px;
            width: 18px;
            left: 3px;
            bottom: 3px;
            background-color: white;
            transition: 0.4s;
            border-radius: 50%;
        }
        input:checked + .slider {
            background-color: #66bb6a;
        }
        input:checked + .slider:before {
            transform: translateX(26px);
        }

        /* 容器样式 */
        .container {
            display: flex;
            position: relative;
            width: 90%;
            max-width: 1200px;
            margin: 60px auto 0 auto; /* 留出顶部空间给开关 */
            height: calc(100vh - 50px); /* 根据需要调整高度 */
        }
        .column {
            width: 50%;
            padding: 20px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
        }
        .column.left {
            border-right: 1px solid #ccc;
        }
        .header {
            text-align: center;
            font-family: "宋体", SimSun, serif;
            font-weight: bold;
            font-size: 12px;
            margin-bottom: 5px; /* 减少标题下方间距 */
        }
        .messages {
            flex: 1;
            overflow-y: auto;
        }
        .message {
            margin-bottom: 10px; /* 减少消息之间的间距 */
        }
        .message .label {
            font-family: "宋体", SimSun, serif;
            font-weight: bold;
            color: #000;
            margin-bottom: 3px; /* 减少标签与内容之间的间距 */
            text-align: left;
        }
        .message .box {
            padding: 8px; /* 减少内边距 */
            border-radius: 5px;
            position: relative;
            transition: transform 0.3s, box-shadow 0.3s;
            font-size: 12px; /* 减小字体大小 */
            white-space: pre-wrap; /* 保留空格和换行 */
        }
        /* 用户消息样式 */
        .user .box {
            background-color: #B2EB72; /* 微信绿色 */
            color: #000;
            text-align: left;
        }
        /* 助手消息样式 */
        .assistant .box {
            background-color: #f0f0f0; /* 浅灰色 */
            color: #000;
            text-align: left;
            cursor: pointer;
            white-space: normal; /* 覆盖 pre-wrap */
        }
        .assistant .box:hover {
            transform: translateY(-3px); /* 减小浮动距离 */
            box-shadow: 0 2px 4px rgba(0,0,0,0.2); /* 减小阴影 */
        }
        /* 系统消息样式 */
        .system .box {
            background-color: #000; /* 黑色背景 */
            color: #fff; /* 白色文字 */
            text-align: left;
        }
        /* 竖线样式 */
        .vertical-line {
            position: absolute;
            left: 50%;
            top: 0;
            bottom: 0;
            width: 1px;
            background-color: #ccc;
        }
        /* 优化 Markdown 列表样式 */
        .box ul {
            margin: 0;
            padding-left: 18px; /* 调整列表缩进 */
        }
        .box li {
            margin-bottom: 3px; /* 减少列表项之间的间距 */
        }
        /* 优化段落间距 */
        .box p {
            margin: 0;
        }
    </style>
</head>
<body>
    <!-- 切换开关 -->
    <div class="toggle-container">
        <div class="switch">
            <input type="checkbox" id="markdown-toggle" checked>
            <span class="slider"></span>
        </div>
        <label for="markdown-toggle">Markdown</label>
    </div>

    <div class="container">
        <div class="column left">
            <div class="header">hunyuan</div>
            <div class="messages" id="hunyuan-messages"></div>
        </div>
        <div class="vertical-line"></div>
        <div class="column right">
            <div class="header">竞品</div>
            <div class="messages" id="jingpin-messages"></div>
        </div>
    </div>

    <script>
        // 定义 hunyuan 的对话数组
        const hunyuanConversations = __|LEFT|__;

        // 定义 jingpin 的对话数组
        const jingpinConversations = __|RIGHT|__;

        // 函数：转义HTML以防止XSS攻击
        function escapeHTML(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        // 函数：渲染对话
        function renderConversations(markdownEnabled) {
            const hunyuanContainer = document.getElementById('hunyuan-messages');
            const jingpinContainer = document.getElementById('jingpin-messages');

            // 清空现有消息
            hunyuanContainer.innerHTML = '';
            jingpinContainer.innerHTML = '';

            // 渲染 hunyuan 对话
            hunyuanConversations.forEach((conv) => {
                const messageDiv = document.createElement('div');
                messageDiv.classList.add('message');

                const label = document.createElement('div');
                label.classList.add('label');
                label.textContent = conv.role;

                const box = document.createElement('div');
                box.classList.add('box');

                if (conv.role === 'system') {
                    box.innerHTML = escapeHTML(conv.content).replace(/\\n/g, '<br>');
                } else if (markdownEnabled && conv.role === 'assistant') {
                    // 如果启用了Markdown并且是助手消息，使用marked渲染
                    box.innerHTML = marked.parse(conv.content);
                } else {
                    // 否则，渲染原始文本并保留换行符
                    box.innerHTML = escapeHTML(conv.content).replace(/\\n/g, '<br>');
                }

                // 添加特定于发言者的类
                if (conv.role === 'user') {
                    messageDiv.classList.add('user');
                } else if (conv.role === 'assistant') {
                    messageDiv.classList.add('assistant');
                } else if (conv.role === 'system') {
                    messageDiv.classList.add('system');
                }

                messageDiv.appendChild(label);
                messageDiv.appendChild(box);

                hunyuanContainer.appendChild(messageDiv);
            });

            // 渲染 jingpin 对话
            jingpinConversations.forEach((conv) => {
                const messageDiv = document.createElement('div');
                messageDiv.classList.add('message');

                const label = document.createElement('div');
                label.classList.add('label');
                label.textContent = conv.role;

                const box = document.createElement('div');
                box.classList.add('box');

                if (conv.role === 'system') {
                    box.innerHTML = escapeHTML(conv.content).replace(/\\n/g, '<br>');
                } else if (markdownEnabled && conv.role === 'assistant') {
                    // 如果启用了Markdown并且是助手消息，使用marked渲染
                    box.innerHTML = marked.parse(conv.content);
                } else {
                    // 否则，渲染原始文本并保留换行符
                    box.innerHTML = escapeHTML(conv.content).replace(/\\n/g, '<br>');
                }

                // 添加特定于发言者的类
                if (conv.role === 'user') {
                    messageDiv.classList.add('user');
                } else if (conv.role === 'assistant') {
                    messageDiv.classList.add('assistant');
                } else if (conv.role === 'system') {
                    messageDiv.classList.add('system');
                }

                messageDiv.appendChild(label);
                messageDiv.appendChild(box);

                jingpinContainer.appendChild(messageDiv);
            });
        }

        // 初始化渲染
        document.addEventListener('DOMContentLoaded', () => {
            const toggle = document.getElementById('markdown-toggle');
            let markdownEnabled = toggle.checked;

            renderConversations(markdownEnabled);

            toggle.addEventListener('change', () => {
                markdownEnabled = toggle.checked;
                renderConversations(markdownEnabled);
            });
        });
    </script>
</body>
</html>


'''
    msg1 = str(msg1)
    msg2 = str(msg2)
    a = pattern.replace('__|LEFT|__', msg1).replace('__|RIGHT|__', msg2)
    with open(savename, 'w') as f:
        f.write(a)


