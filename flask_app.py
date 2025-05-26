# -*- coding: UTF-8 -*-
from collections import defaultdict

from io import BytesIO
from flask import Flask, render_template, request, redirect, url_for
from loguru import logger
from werkzeug.serving import WSGIRequestHandler
import pandas as pd
from config import config

app = Flask(__name__, static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 限制上传文件为10MB

# 使用字典存储号码数据，格式：{号码: (过期时间, 剩余天数)}
phone_data = defaultdict(tuple)


@app.route('/query', methods=['GET', 'POST'])
def query():
    results = []

    if request.method == 'POST':
        input_text = request.form.get('phones', '')
        input_phones = [p.strip() for p in input_text.splitlines() if p.strip()][:50]  # 限制最多50个号码

        for phone in input_phones:
            if phone in phone_data:
                expire_date, remaining_days = phone_data[phone]
                results.append({
                    'phone': phone,
                    'expire_date': expire_date,
                    'remaining_days': remaining_days
                })

    return render_template('query.html', results=results)


@app.route("/upload", methods=['GET', 'POST'])
def upload_excel():
    logger.debug("upload_excel")
    global phone_data

    if request.method == 'POST':
        # 检查是否有文件被上传
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file and file.filename.endswith(('.xlsx', '.xls')):
            # 清空旧数据
            phone_data = defaultdict(tuple)

            # 使用Pandas读取Excel文件
            try:
                df = pd.read_excel(BytesIO(file.read()), header=0, usecols=[0, 1, 2])
                for _, row in df.iterrows():
                    phone = str(row.iloc[0]).strip()
                    expire_date = row.iloc[1]
                    remaining_days = row.iloc[2]
                    phone_data[phone] = (expire_date, remaining_days)
            except Exception as e:
                return f"文件解析失败: {str(e)}"

            return redirect(url_for('query'))

    return render_template('upload.html')


@app.errorhandler(Exception)
def handle_all_exceptions(e):
    app.logger.error(f"handle_all_exceptions: {e}")
    return render_template('index.html',
                           success=None,
                           code='',
                           twoFA='',
                           date='',
                           err_msg="server handle error")


@app.errorhandler(500)
def server_error(e):
    app.logger.error(f"server_error: {e}")
    return render_template('index.html',
                           success=None,
                           code='',
                           twoFA='',
                           date='',
                           err_msg="server error")


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# app launch
def start_flask_app():
    logger.info('Starting Flask App...')
    # 设置 Werkzeug 的请求处理器，确保连接正确关闭
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    b = str(config['FLASK']['DEBUG']).lower() == 'true'
    app.run(port=config['FLASK']['PORT'], host=config['FLASK']['HOST'], debug=b, use_reloader=False)
