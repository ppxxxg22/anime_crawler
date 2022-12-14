import os
from anime_crawler.settings import FILE_PATH
from random import randint, choice
from typing import Tuple


class FileIO:
    def __init__(self) -> None:
        self._path = FILE_PATH
        if not os.path.exists(self._path):
            os.makedirs(self._path)

    def to_file(self, img: bytes, name: str) -> bool:
        '''
        将图像持久化到文件函数

        Args:
            img (bytes): 字节格式的图片
            name (str): 图片名称

        Returns:
            bool: 是否写入成功
        '''
        while os.path.exists(os.path.join(self._path, name)):
            # 保证当前图像名不被占用
            if("." in name):
                name = "{}_.{}".format(*name.split("."), randint(1, 1e5))
            else:
                name += f"_{randint(1,1e5)}.jpg"
        # 下面写入文件
        with open(os.path.join(self._path, name), "wb") as f:
            f.write(img)
        return True

    def from_file(self, name: str) -> bytes:
        '''
        从文件中读取图像

        Args:
            name (str): 文件名称

        Returns:
            bytes: 图像的字节流
        '''
        if os.path.exists(os.path.join(self._path, name)):
            with open(os.path.join(self._path, name), "rb") as f:
                # TODO 这是否是正确的字节流呢？
                img = f.read()
            return img

    def random_img(self) -> Tuple[str, bytes]:
        '''
        从文件中随机抽取一张图像并返回其名字和字节流

        Returns:
            Tuple[str, bytes]: 名字和字节流
        '''

        files = next(os.walk(self._path))[-1]
        file = choice(files)
        return (file, self.from_file(file))

    def get_file_nums(self) -> int:
        '''
        获取目标目录下文件数目

        Returns:
            int: 数值
        '''
        # if os.path.exists(self._path):
        return len(next(os.walk(self._path))[-1])
        # return 0

    def get_file_size(self) -> float:
        '''
        返回目录的空间大小

        Returns:
            float: 占用空间，单位MB
        '''
        size = 0
        *_, files = next(os.walk(self._path))
        for file in files:
            size += os.path.getsize(os.path.join(self._path, file))
        return size/1048576
