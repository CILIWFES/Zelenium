def X_XSRF_TOKEN(httper, request_options, method):
    """
    针对cookie的TOKEN验证
    :param httper:
    :param request_options:
    :param method:
    :return:
    """
    cookies = httper.get_cookies()
    for item in cookies:
        if "name" in item and item["name"] == "XSRF-TOKEN":
            request_options["X-XSRF-TOKEN"] = item["value"]
            request_options["X-Requested-With"] = "XMLHttpRequest"
            break
    return request_options
