import os
import pkg_resources

class CherryExport:
    def __init__(self):
        self.words = {
            "Docx": self.create_docx,
            "TextFile": self.create_text_file,
        }

    def get_code(self, word):
        func = self.words.get(word, None)
        if func:
            func()

    def create_docx(self):
        docx_path = pkg_resources.resource_filename('CherryExport', 'resources/Docx.docx')
        print(f"Word document path: {docx_path}")
        return docx_path

    def create_text_file(self):
        text_path = pkg_resources.resource_filename('CherryExport', 'resources/TextFile.txt')
        print(f"Text file path: {text_path}")
        return text_path

# Пример использования
if __name__ == "__main__":
    log = CherryExport()
    log.get_code("Docx")  # Вернёт путь к файлу sample_docx.docx
    log.get_code("TextFile")  # Вернёт путь к файлу sample_text.txt
