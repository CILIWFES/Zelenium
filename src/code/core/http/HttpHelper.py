import json
import re


class HttpHelper:
    """
    接口测试类
    """

    def __init__(self, scheduler):

        self._scheduler = scheduler
        self._driver = self._scheduler.get_DriverHelper()
        self.type_get = 'GET'
        self.type_post = 'POST'
        self.Content_Type = "Content-Type"
        self.contentType_form = "multipart/form-data"
        self.contentType_json = "application/json"
        self.contentType_urlencoded = "application/x-www-form-urlencoded"
        self._verification_function = None


    def http_sender(self, url, send_data, content_type=None, force_content_type=None, request_options: dict = None,
                    charset='utf-8', timeout=2000, method='POST', async_flag=False, verification_function=None,
                    all_info=False):
        """
        发送http请求,目前支持json与urlencoded
        :param url:                 资源定位符
        :param method:              请求方法
        :param timeout:             超时时间
        :param charset:             编码格式
        :param send_data:           发送数据
        :param async_flag:          异步模式,默认False 同步
        :param content_type:        发送的文本格式
        :param force_content_type:  暴力发送,忽视数据类型,直接发送
        :param request_options:     请求头文件选项
        :param verification_function: 用户自定义请求头文件方法
        :param all_info:            数据全返回{content:data,status:状态 }

        :return:
        """
        assert isinstance(send_data, (str, dict)), "请传入正确类型"

        if force_content_type is None:
            """
              1.未指定content_type,通过send_data 判断content_type
              2.指定content_type,若格式不对应,尝试转化
            """
            send_data, content_type = self._choice_content_type(send_data, content_type, method)
        else:
            content_type = force_content_type

        """
        代码生成
        """
        url, request_options, pretreatment, after = self.__generate(url, send_data, content_type,
                                                                    request_options, method, charset)
        # 用户自定义代码段,用于生成请求头选项
        if verification_function is not None or self._verification_function is not None:
            if verification_function is not None:
                request_options = verification_function(self, request_options, method)
            else:
                request_options = self._verification_function(self, request_options, method)

        # 请求头代码生成
        request_codes = ["""xhr.setRequestHeader("{0}", "{1}");""".format(key, item) for key, item in
                         request_options.items()]

        request_code = "\n".join(request_codes)

        # 执行js
        response_data = self._driver.execute_script(
            """
            let url=arguments[0];
            let send_data=arguments[1];
            let method=arguments[2];
            let timeout=arguments[3]*1.0;
            let async=arguments[4];
            
            let xhr = new XMLHttpRequest();
            var globalVariable;
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4) {
                   if (xhr.status === 304 || (xhr.status >= 200 && xhr.status < 300)) {
                       globalVariable={status:xhr.status,content:xhr.responseText,error:false};
                   }
                   else{
                       globalVariable={status:xhr.status,error:True};
                   }
                }
            };
            """ + pretreatment + """
            
            if (async) {
                xhr.timeout = timeout;
                xhr.ontimeout = function () {
                    console.log('接口命令,超时处理')
                };
            }
            
            xhr.open(method, url, async);

            """ + request_code + """
            
            """ + after + """
            if (!async) {
                return globalVariable;
            }
            """, url, send_data, method, timeout, async_flag)

        if all_info:
            return response_data
        elif response_data["error"]:
            return None
        else:
            if self._is_json(response_data["content"])[0]:
                return self.json_to_dict(response_data["content"])
            else:
                return response_data["content"]

    def judge_data_format(self, send_data):
        """
        判断格式
        :param send_data:
        :return:0 字典,1 json格式 ,2 谷歌浏览器:form_data格式  数据字典
        """
        if isinstance(send_data, dict):
            return 0, send_data

        if isinstance(send_data, str):
            isjson, dict_data = self._is_json(send_data.replace('\n', ''))
            if isjson:
                return 1, dict_data
            is_form, dict_data = self._is_form_data(send_data)

            if is_form:
                return 2, dict_data
            raise Exception("格式无法识别")
        return 0, {}

    def _choice_content_type(self, send_data, content_type, method: str):
        """
        选择content_type类型
        1.用户未选择类型,帮助选择
        2.用户选择类型,帮助转化
        :param send_data:传入数据
        :param content_type:用户选择类型
        :return: 所需类型,content_type
        """
        # 判断数据类型,获取数据字典
        type, send_dict = self.judge_data_format(send_data)
        if method.upper() == "GET":
            return send_dict, None
        # 自动选择content_type
        if content_type is None:
            if type == 0 or type == 2:
                return self.dict_to_urlencoded(send_dict), self.contentType_urlencoded
            elif type == 1:
                return send_data, self.contentType_json
        # 转化为json
        elif content_type == self.contentType_json:
            return self.dict_to_json(send_dict), self.contentType_json
        # 转化为urlencoded
        elif content_type == self.contentType_urlencoded:
            return self.dict_to_urlencoded(send_dict), self.contentType_urlencoded

        # 转化为form_data无需转化
        elif content_type == self.contentType_form:
            return send_dict, self.contentType_form

        else:
            raise Exception("请求类型错误,请确认content_type参数")

    def dict_to_urlencoded(self, dict_data: dict):
        """
        字典转urlencoded格式
        :param dict_data:
        :return:
        """
        assert isinstance(dict_data, dict), "字典参数错误"
        send_data = ""
        send_list = [key + "=" + val for key, val in dict_data.items()]
        if len(send_list) <= 0:
            return send_data
        send_data = "&".join(send_list)

        return send_data

    def dict_to_json(self, dict_data: dict):
        """
        字典转json
        :param dict_data:
        :return:
        """
        assert isinstance(dict_data, dict), "字典参数无效"
        return json.dumps(dict_data)

    def json_to_dict(self, json_data: str) -> dict:
        """
        json转字典
        :param json_data:
        :return:
        """
        assert isinstance(json_data, str), "请传入json字符串"
        return json.loads(json_data)

    def _is_json(self, send_data):
        """
        判断是否为json格式
        :param send_data:
        :return:
        """
        if not isinstance(send_data, str):
            return False, None
        try:
            dict_data = json.loads(send_data)
        except ValueError:
            return False, None
        return True, dict_data

    def _is_form_data(self, send_data):
        """
        判断是否为form_data格式
        :param send_data:
        :return:
        """
        line = send_data.split('\n')
        notNone_lines = []
        for item in line:
            item = item.strip()
            if len(item) > 0:
                notNone_lines.append(item)

        ret_dict = {}
        for item in notNone_lines:
            indx = item.find(":")
            key = item[0:indx].strip()
            match = re.match("""^[a-zA-Z$_]+[a-zA-Z$_0-9]*$""", key)
            if not match:
                return False, None
            value = item[indx + 1:].strip()
            ret_dict[key] = value

        return True, ret_dict

    def get_cookies(self):
        """
        获取浏览器cookie
        :return:
        """
        return self._driver.get_cookies()

    def __generate(self, url, send_data, content_type, request_options, method, charset):
        """
        代码自动生成与转化
        :param url:                 资源定位符
        :param send_data:           发送数据
        :param content_type:        发送的文本格式
        :param request_options:     请求头文件选项
        :param method:              请求方法
        :param charset:             编码格式
        :return:
        """
        if request_options is None:
            request_options = {}

        # 生成get方法,请求地址与请求头与对应代码
        if method.upper() == 'GET':
            url, request_options, pretreatment, after = self.__generate_get(url, send_data, request_options, charset)
        else:

            # 生成application/json方法,请求地址与请求头与对应代码
            if content_type == self.contentType_json:
                request_options, pretreatment, after = self.__generate_json(request_options, charset)


            # 生成urlencoded方法,返回请求头与对应代码
            elif content_type == self.contentType_urlencoded:
                request_options, pretreatment, after = self.__generate_urlencoded(request_options, charset)

            # 生成form方法,返回请求头与对应代码
            elif content_type == self.contentType_form:
                request_options, pretreatment, after = self.__generate_form_data(request_options, charset)
            else:
                raise Exception("content_type错误")

        return url, request_options, pretreatment, after

    def __generate_urlencoded(self, request_options, charset):
        """
        生成urlencoded 脚本
        :param send_data:       发送的数据
        :param request_options: 请求头数据
        :param charset:         编码格式
        :return: (发生数据,请求头,前处理,后处理)
        """
        if charset is not None:
            request_options[self.Content_Type] = self.contentType_urlencoded + ";charset=" + charset
        else:
            request_options[self.Content_Type] = self.contentType_urlencoded

        pretreatment = ""
        afterTreatment = "xhr.send(send_data)"
        return request_options, pretreatment, afterTreatment

    def __generate_json(self, request_options, charset):
        """
        生成urlencoded 脚本
        :param send_data:       发送的数据
        :param request_options: 请求头数据
        :param charset:         编码格式
        :return: (发生数据,请求头,前处理,后处理)
        """
        if charset is not None:
            request_options[self.Content_Type] = self.contentType_json + ";charset=" + charset
        else:
            request_options[self.Content_Type] = self.contentType_json

        pretreatment = ""
        afterTreatment = "xhr.send(send_data)"
        return request_options, pretreatment, afterTreatment

    def __generate_form_data(self, request_options, charset):
        """
        生成form_data 脚本
        :param send_data:       发送的数据
        :param request_options: 请求头数据
        :param charset:         编码格式
        :return: (发生数据,请求头,前处理,后处理)
        """

        request_options[self.Content_Type] = self.contentType_form

        pretreatment = """
            let formData=new FormData();
            Object.keys(send_data).forEach((key) => {
            	formData.append(key, send_data[key]);
            });
            send_data=formData;
        """
        afterTreatment = "xhr.send(send_data)"
        return request_options, pretreatment, afterTreatment

    def __generate_get(self, url: str, send_data: dict, request_options, charset):
        """
        生成get脚本
        :param url:             请求地址
        :param send_data:       发送的数据
        :param request_options: 请求头数据
        :param charset:         编码格式
        :return: (发生数据,请求头,前处理,后处理)
        """
        pretreatment = ""
        if send_data is not None or len(send_data) > 0:
            if isinstance(send_data, str):
                urlencode = send_data
            else:
                urlencode = self.dict_to_urlencoded(send_data)

            if url.find("?") == -1:
                url += "?" + urlencode
            else:
                url += urlencode
        afterTreatment = "xhr.send()"

        return url, request_options, pretreatment, afterTreatment

    def set_verification(self, verification_function):
        self._verification_function = verification_function
