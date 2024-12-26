# pass_generate
from tketool.mlsample.NLSampleSource import NLSampleSourceBase
from tketool.mlsample.SampleSet import SampleSet
import json
from tketool.files import write_file_line
import docx2txt
import PyPDF2
from docx import Document
from zipfile import BadZipFile
from tketool.logs import log


def convert_jsonl(datasource: NLSampleSourceBase, set_name: str, prompt_completion_fun,
                  target_path: str):
    """
    这个函数用于将数据源中的数据转换为jsonl文件。函数首先会从数据源中读取指定的“set_name”的样本集，然后使用“prompt_completion_fun”函数将每个样本的问题和答案转换为字典形式，最后将所有的行写入到“target_path”指定的文件中。
    
    参数:
        datasource(NLSampleSourceBase): 数据源，必须是NLSampleSourceBase类型或其子类的实例。
        set_name(str): 从数据源中获取样本集的名称。
        prompt_completion_fun(function): 用于将样本转换为字典形式的函数。该函数必须接受一个参数（样本），并返回一个元组，元组的第一个元素是问题，第二个元素是答案。
        target_path(str): 输出jsonl文件的路径。
    
    返回:
        None
    
    示例：
    
        def prompt_completion(item):
            return item.question, item.answer
    
        datasource = MyDataSource()
        convert_jsonl(datasource, "train", prompt_completion, "train.jsonl")
    
    注意：这个函数不会检查“target_path”是否已经存在，如果存在，它会直接覆盖旧文件。
    
    错误与异常：
        如果数据源中不存在指定的“set_name”，函数会抛出异常。
        如果“prompt_completion_fun”函数不能正确处理样本，也会抛出异常。
    """

    row_lines = []
    for item in SampleSet(datasource, set_name):
        prompt, completion = prompt_completion_fun(item)
        row_data = {
            'prompt': prompt,
            'completion': completion
        }
        row_str = json.dumps(row_data)
        row_lines.append(row_str)

    write_file_line(target_path, row_lines)


def doc_to_txt(file_path, txt_path):
    try:
        text = docx2txt.process(file_path)
    except BadZipFile:
        log(f'Failed to process {file_path}: not a .doc file or file is corrupted.')
        text = ''
    with open(txt_path, 'w') as output:
        output.write(text)


def docx_to_txt(file_path, txt_path):
    try:
        doc = Document(file_path)
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    except BadZipFile:
        log(f'Failed to process {file_path}: not a .docx file or file is corrupted.')
        text = ''
    with open(txt_path, 'w') as output:
        output.write(text)


def pdf_to_txt(file_path, txt_path):
    with open(file_path, 'rb') as pdf_file_obj:
        pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
        num_pages = len(pdf_reader.pages)
        text = '\n'.join([page.extract_text() for page in pdf_reader.pages])
        with open(txt_path, 'w') as output:
            output.write(text)
