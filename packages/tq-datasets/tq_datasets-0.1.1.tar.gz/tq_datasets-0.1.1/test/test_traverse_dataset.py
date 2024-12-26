from typing import Optional, Any

from tq_datasets.dataset_op_interface import TraverseDataset
from tq_utils import my_json, time_util


def test_default_method():
    print()
    t = TraverseDataset()
    t.traverse_dataset(r'E:\Workspace\Pycharm\Datasets\data\Dataset-DOWL2\DOWL2\eng\al-monitor',
                       'json')


class TraverseDOWL(TraverseDataset):
    @staticmethod
    def item_reader(file_abs_path: str) -> str:
        print('oaushoiasdoiajsodiasoidowifoqn')
        return my_json.load_json_safe(file_abs_path)

    @staticmethod
    def item_processor(**kwargs) -> Optional[Any]:
        print('asdasda')
        return kwargs['raw_item_data']


def test_override_methods():
    print()
    t = TraverseDOWL()
    with time_util.Timer('aa'):
        r = t.traverse_dataset(r'E:\Workspace\Pycharm\Datasets\data\Dataset-DOWL2\DOWL2\eng',
                               'json', external_raw_data={'s': 1})
        print(len(r))
    """
    3174
    Elapsed time: 2.8971 seconds
    """


def test_override_methods_multithread():
    print()
    t = TraverseDOWL()
    with time_util.Timer('aa'):
        r = t.traverse_dataset(r'E:\Workspace\Pycharm\Datasets\data\Dataset-DOWL2\DOWL2\eng',
                               'json', external_raw_data={'s': 1}, multi_process=True)
        print(len(r))
    """
    3174
    Elapsed time: 0.9121 seconds
    """


def test_override_methods_with_max_num():
    print()
    t = TraverseDOWL()
    with time_util.Timer('aa'):
        r = t.traverse_dataset(r'E:\Workspace\Pycharm\Datasets\data\Dataset-DOWL2\DOWL2\eng',
                               'json', max_num=30, external_raw_data={'s': 1})
        print(len(r))
    """
    30
    Elapsed time: 0.0765 seconds
    """


def test_override_methods_multithread_with_max_num():
    print()
    t = TraverseDOWL()
    with time_util.Timer('aa'):
        r = t.traverse_dataset(r'E:\Workspace\Pycharm\Datasets\data\Dataset-DOWL2\DOWL2\eng',
                               'json', max_num=30, external_raw_data={'s': 1}, multi_process=True)
        print(len(r))
    """  数量比较少，反而开销打了，没有单线程来的划算
    30
    Elapsed time: 0.0800 seconds
    """


def test_no_return():
    print()
    t = TraverseDOWL()
    t.traverse_dataset_without_return(r'E:\Workspace\Pycharm\Datasets\data\Dataset-DOWL2\DOWL2\eng',
                                      'json', max_num=30, external_raw_data={'s': 1})


def test_multi_process_no_return():
    print()
    t = TraverseDOWL()
    t.traverse_dataset_without_return(r'E:\Workspace\Pycharm\Datasets\data\Dataset-DOWL2\DOWL2\eng',
                                      'json', max_num=30, external_raw_data={'s': 1}, multi_process=True)
