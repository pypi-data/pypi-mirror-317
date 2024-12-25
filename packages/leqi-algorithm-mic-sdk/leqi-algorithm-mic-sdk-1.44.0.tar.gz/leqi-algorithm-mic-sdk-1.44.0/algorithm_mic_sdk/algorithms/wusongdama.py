from ..auth import AuthInfo
from ..base import AlgoBase
from ..tools import FileInfo


class WusongDamaMasking(AlgoBase):
    __algo_name__ = 'dama_masking'
    DEFAULT_TIMEOUT = 1800

    def __init__(self,
                 auth_info: AuthInfo,
                 oss_file: FileInfo,
                 file_type: str,
                 intermediate_data_oss_file:FileInfo=None,
                 intermediate_data:str=None,
                 process=None,
                 custom_data=None,
                 callback_url=None,
                 **kwargs):
        """
        武松打码 打码算法
        @param auth_info: 授权信息
        @param oss_file: 待处理的文件(图片或视频)
        @param file_type:文件类型,取值有`IMAGE` `VIDEO`
        @param intermediate_data_oss_file:算法缓存文件对象,与`intermediate_data`二选一
        @param intermediate_data:算法缓存文件数据,与`intermediate_data_oss_file`二选一
        @param process:图片缩放参数,仅在file_type为`IMAGE` 时有效
        @param custom_data:
        @param callback_url:
        @param kwargs:
        """
        super().__init__(auth_info)
        if not intermediate_data_oss_file and not intermediate_data:
            raise Exception('intermediate_data_oss_file 和 intermediate_data 参数必须要有一个')
        self.request['oss_file'] = oss_file.get_oss_name(self)
        self.request['process'] = process
        self.request['custom_data'] = custom_data
        self.request['file_type'] = file_type
        self.request['intermediate_data_oss_file'] = intermediate_data_oss_file
        self.request['intermediate_data'] = intermediate_data
        self.request['callback_url'] = callback_url
        self.request.update(kwargs)


class WusongDamaScanning(AlgoBase):
    __algo_name__ = 'dama_scanning'
    DEFAULT_TIMEOUT = 1800

    def __init__(self,
                 auth_info: AuthInfo,
                 oss_file: FileInfo,
                 file_type: str,
                 options_for_scanning:dict=None,
                 process=None,
                 custom_data=None,
                 callback_url=None,
                 **kwargs):
        """
        武松打码 人脸扫描算法
        @param auth_info: 授权信息
        @param oss_file: 文件
        @param file_type:文件类型,取值有`IMAGE` `VIDEO`
        @param options_for_scanning:扫描参数
        @param process:图片缩放参数,仅在file_type为`IMAGE` 时有效
        @param custom_data:
        @param callback_url:
        @param kwargs:
        """
        super().__init__(auth_info)
        self.request['oss_file'] = oss_file.get_oss_name(self)
        self.request['process'] = process
        self.request['custom_data'] = custom_data
        self.request['file_type'] = file_type
        self.request['callback_url'] = callback_url
        self.request['options_for_scanning'] = options_for_scanning
        self.request.update(kwargs)
