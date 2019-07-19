from config import *
import numpy as np


class AnnTools:
    module_dict = {}

    def discern_mp(self, base64_code):
        from tools.image.ImageTools import image_tools
        gray = image_tools.base64_to_gray(base64_code)

        gray = image_tools.binarization(gray, 130)
        gray = image_tools.noise_remove(gray, 4)

        gray = np.array(gray)
        # 调用神经网络
        batch_size = 1
        ret = self.prediction(np.asarray([[gray]]), (batch_size, 1, 40, 100), (batch_size, 4), name="mp4")
        ret = np.argmax(ret, axis=1)
        msg = ""
        for i in ret:
            msg += str(i)
        return msg

    def prediction(self, np_data, dataShape, labelShape, name=None, module=None):
        """
        启动预测神经网络
        :param np_data:     numpy数据,dataShape格式
        :param dataShape:   预测的格式,与训练相同,区别是批次=1 如(1,训练通道数,训练x,训练y)
        :param labelShape:  预测的格式,与训练相同,区别是批次=1(1,训练输出数)
        :param name:        模块名
        :param module:      模块实例
        :return:
        """
        if module is None and name is not None:
            if name in AnnTools.module_dict:
                module = AnnTools.module_dict[name]
            else:
                module = self.module_read(GF.getAnnDiscernPath(name), name, dataShape, labelShape=labelShape)
                AnnTools.module_dict[name] = module

        assert module is not None, "请检查神经网络配置文件"

        ret = module.predict(np_data).asnumpy()
        return ret

    def module_read(self, path, fileName, dataStruct, labelShape=None, dataName=None, labelName=None, cpuType=True):
        """
        加载神经网络
        :param path:
        :param fileName:
        :param dataStruct:
        :param labelShape:
        :param dataName:
        :param labelName:
        :param cpuType:
        :return:
        """
        print("加载神经网络,首次加载用时较长,请耐心等待")
        import mxnet as mx
        # 判断硬件类型
        processor = mx.cpu() if (cpuType) else mx.gpu()
        # 读取路径为空默认填充
        prefix = path + fileName

        param_name = prefix + ".params"

        symbol = mx.sym.load(prefix + '-symbol.json')

        if dataName is None:
            lst = symbol.list_arguments()
            dataName = lst[0]

        if labelName is None:
            lst = symbol.list_arguments()
            labelName = lst[-1]

        save_dict = mx.nd.load(param_name)
        arg_params = {}
        aux_params = {}
        for k, v in save_dict.items():
            tp, name = k.split(':', 1)
            if tp == 'arg':
                arg_params[name] = v
            if tp == 'aux':
                aux_params[name] = v

        # 加载module
        mod = mx.mod.Module(symbol=symbol, context=processor, data_names=[dataName], label_names=[labelName])

        if labelShape is None:
            labelShape = (dataStruct[0],)
        mod.bind(for_training=False, data_shapes=[(dataName, dataStruct)],
                 label_shapes=[(labelName, labelShape)])
        mod.set_params(arg_params, aux_params)
        return mod


ann_tools = AnnTools()
