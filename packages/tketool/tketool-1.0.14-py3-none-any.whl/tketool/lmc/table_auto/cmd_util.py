from tketool.lmc.table_auto.engines import *
from tketool.lmc.table_auto.task_init import get_init_llm


def execute_excel(path, start_row_index=1):
    model_obj = get_init_llm()
    e_engine = excel_engine(model_obj, double_shape(), prompt_file_shape())
    e_engine.call_file(path)
