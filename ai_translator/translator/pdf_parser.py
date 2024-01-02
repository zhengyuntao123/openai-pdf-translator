import pdfplumber
from typing import Optional
from book import Book, Page, Content, ContentType, TableContent
from translator.exceptions import PageOutOfRangeException
from utils import LOG


class PDFParser:
    def __init__(self):
        pass

    def parse_pdf(self, pdf_file_path: str, pages: Optional[int] = None) -> Book:
        book = Book(pdf_file_path)

        with pdfplumber.open(pdf_file_path) as pdf:
            if pages is not None and pages > len(pdf.pages):
                raise PageOutOfRangeException(len(pdf.pages), pages)

            if pages is None:
                pages_to_parse = pdf.pages
            else:
                #翻译到第pages面
                pages_to_parse = pdf.pages[:pages]

            for pdf_page in pages_to_parse:
                page = Page()

                # Store the original text content
                # 这里并没有保持原始布局
                raw_text = pdf_page.extract_text(layout=True)
                tables = pdf_page.extract_tables()

                # Remove each cell's content from the original text
                for table_data in tables:
                    for row in table_data:
                        for cell in row:
                            # 因为extract_text也会解析出表格
                            # 所以通过该循环暴力地把文本中的表格内容替换为空
                            # replace默认替换所有出现，此处的1表示替换raw_text中cell的第一次出现
                            raw_text = raw_text.replace(cell, "", 1)

                # Handling text
                if raw_text:
                    # Remove empty lines and leading/trailing whitespaces
                    raw_text_lines = raw_text.splitlines()
                    cleaned_raw_text_lines = [line.strip() for line in raw_text_lines]
                    #必须合并在一起去问chatgpt翻译，这个时候不能拆开一个一个去翻译
                    cleaned_raw_text = "\n".join(cleaned_raw_text_lines)
                    # content类型是ContentType.TEXT
                    text_content = Content(content_type=ContentType.TEXT, original=cleaned_raw_text)
                    page.add_content(text_content)
                    LOG.debug(f"[raw_text]\n {cleaned_raw_text}")



                # Handling tables
                if tables:
                    table = TableContent(tables)
                    page.add_content(table)
                    LOG.debug(f"[table]\n{table}")

                book.add_page(page)

        return book
