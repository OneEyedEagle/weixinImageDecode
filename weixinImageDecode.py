# weixin_Image.bat 破解
# JPG 16进制 FF D8 FF
# PNG 16进制 89 50 4e
# 微信.bat 16进制 97 4e 50
# key 值 1e1e 0x1e  weixin.bat-jpg

import os

class WeixinImageDecode(object):
    def __init__(self, into_path, out_path ,jpg_decimal=255):
        """
        初始化
        :param into_path: 文件输入路径
        :param out_path: 文件转换后存放路径
        :param jpg_decimal:jpg16进制FF 转成十进制255
        """
        self.into_path = into_path
        self.out_path = out_path
        self.jpg_decimal = jpg_decimal

    def get_dat_decimal(self):
        """
        获取微信图片的开头值
        :return: dat_decimal
        """
        fsinto = os.listdir(self.into_path)
        # print(fsinto)
        into_path = os.path.join(self.into_path, fsinto[0])
        # print(into_path)
        with open(into_path, 'rb')as f:
            dat_strs = f.readline(1)
            # print(str)
            for dat_str in dat_strs:
                # print(dat_strs)
                dat_decimal = dat_str
                # print(dat_decimal)
                return dat_decimal

    def xor_Calculate(self, dat_decimal):
        """
        根据weixin图片.bat计算xor值
        :param dat_decimal: dat_decimal
        :return: xor
        """
        xor = dat_decimal ^ self.jpg_decimal
        # xor = hex(xor)
        return xor

    def imageDecode(self, f, fn ,xor):
        """
        解码
        :param f: 微信图片路径
        :param fn:微信图片目录下的.bat
        :return:
        """
        # 读取.bat
        dat_read = open(f, "rb")
        # 图片输出路径
        out = os.path.join(self.out_path, fn + ".jpg")
        # 图片写入
        png_write = open(out, "wb")
        # 循环字节
        for now in dat_read:
            for nowByte in now:
                # print(xor)
                # 转码计算
                newByte = nowByte ^ xor
                # 转码后重新写入
                png_write.write(bytes([newByte]))
        dat_read.close()
        png_write.close()

    def findFile(self, f,xor):
        """
        寻找文件
        :param f:微信图片路径
        :return:
        """
        # 把路径文件夹下的文件以列表呈现
        fsinfo = os.listdir(f)
        # 逐步读取文件
        for fn in fsinfo:
            # 拼接路径：微信图片路径+图片名
            temp_path = os.path.join(f, fn)
            # 判断目录还是.bat
            if not os.path.isdir(temp_path):
                print('文件路径：{}'.format(temp_path))
                #print(fn)
                # 转码函数
                self.imageDecode(temp_path, fn, xor)
            else:
                pass

    def main(self):
        dat_decimal = self.get_dat_decimal()
        xor = self.xor_Calculate(dat_decimal)
        self.findFile(self.into_path, xor)


if __name__ == '__main__':
    # 录入需要转换的微信路径
    #into_path = 'D:\Project0611\weixin_image\weixin1212800'
    # 录入需要保存后图片的路径
    #out_path = 'D:\Project0611\weixin_image\weixin1212800\\'
    # weixinImageDecode = WeixinImageDecode(into_path, out_path)
    # dat_decimal = weixinImageDecode.get_dat_decimal()
    # xor = weixinImageDecode.xor_Calculate(dat_decimal)
    # weixinImageDecode.findFile(into_path,xor)
    # weixinImageDecode.main()

    # -----------------------------------------------------------------
    # 2023.2.15 更新
    # 针对 2022.7 后的 3.9.0 版本wx
    #   图片放在 MsgAttach 下，各个聊天对象有独立的文件夹，在其下的 Image 文件夹内，再按月份分文件夹存储

    # 需要转换的微信文件夹，最后一级必须为 FileStorage 下的 MsgAttach 文件夹
    path1 = 'D:\Documents\WeChat Files\wxid_xxx\FileStorage\MsgAttach'

    # 转换后的存储位置，将按照 path2\各个聊天对象\各个月份 的路径导出jpg图片
    # （若路径不存在，则会自动创建）
    path2 = 'E:\导出目录'

    # 枚举全部月份的文件夹，逐个处理并导出
    def process_image_folder(in_path, out_path):
        fs = os.listdir(in_path)
        for fn in fs:
            temp_path = os.path.join(in_path, fn) # 月份文件夹
            if os.path.isdir(temp_path):
                fs2 = os.listdir(temp_path)
                if len(fs2) == 0:  # 如果该月份文件夹下没有图片，则退出
                    return 
                out_path2 = os.path.join(out_path, fn)
                if os.path.exists(out_path2):  # 如果导出目录中该月份的对应文件夹已存在，则退出
                    return
                os.makedirs(out_path2, exist_ok=True)
                # 处理该月份文件夹下的全部图片，并保存到指定位置的同名文件夹下
                weixinImageDecode = WeixinImageDecode(temp_path, out_path2)
                weixinImageDecode.main()
    
    # 枚举全部聊天对象的文件夹，再处理 Image 文件夹下的各个月份
    def process_object_folder(in_path, out_path):
        fs = os.listdir(in_path)
        for fn in fs:
            temp_path = os.path.join(in_path, fn, "Image")
            if os.path.isdir(temp_path):
                out_path2 = os.path.join(out_path, fn)
                os.makedirs(out_path2, exist_ok=True)
                process_image_folder(temp_path, out_path2)

    # 开始处理
    process_object_folder(path1, path2)
