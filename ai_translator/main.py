import sys
import os

#这行代码的作用是将当前脚本（或模块）所在的目录添加到Python解释器的模块搜索路径中。
# os.path.abspath(__file__)：获取当前脚本的绝对路径。
# os.path.dirname(...)：获取绝对路径的父目录。
# sys.path.append(...)：将父目录添加到Python解释器的模块搜索路径中。
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, ConfigLoader, LOG
from model import GLMModel, OpenAIModel
from translator import PDFTranslator

# python ai_translator/main.py --model_type OpenAIModel --openai_api_key $OPENAI_API_KEY --file_format pdf
# python ai_translator/main.py --model_type OpenAIModel --openai_api_key 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 --file_format pdf

if __name__ == "__main__":
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()
    config_loader = ConfigLoader(args.config)

    config = config_loader.load_config()

    model_name = args.openai_model if args.openai_model else config['OpenAIModel']['model']
    api_key = args.openai_api_key if args.openai_api_key else config['OpenAIModel']['api_key']
    model = OpenAIModel(model=model_name, api_key=api_key)


    pdf_file_path = args.book if args.book else config['common']['book']
    file_format = args.file_format if args.file_format else config['common']['file_format']

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(model)
    #pages表示翻译到第pages面
    translator.translate_pdf(pdf_file_path, file_format,pages=3)
