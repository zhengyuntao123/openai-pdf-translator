import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, send_file, jsonify
from translator import PDFTranslator, TranslationConfig
from utils import ArgumentParser, LOG

app = Flask(__name__)

TEMP_FILE_DIR = "flask_temps/"

# 装饰器用于设计api的URL
@app.route('/translation', methods=['POST'])
def translation():
    try:
        # python request库中已经实现了处理文件流
        print(os.getcwd())
        input_file = request.files['input_file']
        source_language = request.form.get('source_language', 'English')
        target_language = request.form.get('target_language', 'Chinese')

        LOG.debug(f"[input_file]\n{input_file}")
        LOG.debug(f"[input_file.filename]\n{input_file.filename}")

        if input_file and input_file.filename:
            # # 创建临时文件
            input_file_path = TEMP_FILE_DIR+input_file.filename
            LOG.debug(f"[input_file_path]\n{input_file_path}")
            # 用save方法将文件流储存为文件, input_file_path是输入文件存储的临时目录
            input_file.save(input_file_path)
            # 调用翻译函数
            output_file_path = Translator.translate_pdf(
                input_file=input_file_path,
                output_file_format=config.output_file_format,
                source_language=source_language,
                target_language=target_language,
                pages=1)
            
            # 移除临时文件
            # os.remove(input_file_path)

            # 构造完整的文件路径
            output_file_path = os.getcwd() + "/" + output_file_path
            LOG.debug(output_file_path)

            # 返回翻译后的文件
            return send_file(output_file_path, as_attachment=True)
    except Exception as e:
        response = {
            'status': 'error',
            'message': str(e)
        }
        return jsonify(response), 400


def initialize_translator():
    # 解析命令行
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()

    # 初始化配置单例
    global config
    config = TranslationConfig()
    config.initialize(args)    
    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    global Translator
    Translator = PDFTranslator(config.model_name)


if __name__ == "__main__":
    # 初始化 translator
    initialize_translator()
    # 启动 Flask Web Server
    app.run(host="0.0.0.0", port=5000, debug=True)