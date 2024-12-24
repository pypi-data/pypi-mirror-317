from typing import Callable, Any
from pydantic import BaseModel, Field
# from flask import request, Response, jsonify
import inspect


def post_mapping(path: str):
    """映射post请求"""

    def add_post_url(view_fn: Callable):
        register_url(path, view_fn, methods=['post'])

    return add_post_url


def get_mapping(path: str):
    """映射get请求"""

    def add_get_url(view_fn: Callable):
        register_url(path, view_fn, methods=['get'])

    return add_get_url


class WebUrl(BaseModel):
    """web url配置"""
    path: str = Field(title="映射地址", default=None)
    handler: Callable = Field(title="函数处理器", default=None)
    methods: list[str] = Field(title="映射方法", default=['post'])


# 存储注册过的url
registered_urls: list[WebUrl] = []


def request_handler_creator(raw_handler: Callable, arg_num: int) -> Callable:
    def get_request_param() -> dict[str, Any] | None:
        return flask.request.json or {}

    def get_response(handler_obj: dict[str, Any] | None = None) -> flask.Response:
        if handler_obj is None:
            return flask.jsonify({
                'success': True
            })
        return flask.jsonify(handler_obj)

    def request_handler() -> flask.Response:
        request_param = {
            'params': get_request_param()
        }

        if arg_num < 1:
            handler_obj = raw_handler()
        else:
            handler_obj = raw_handler(**request_param)

        return get_response(handler_obj)

    return request_handler


def register_url(path: str, raw_handler: Callable, **kwargs):
    """注册url"""

    if inspect.isfunction(raw_handler) is False:
        error_text = f"{path} 映射对象必须为函数"
        raise ValueError(error_text)

    raw_handler_arg_specs = inspect.getfullargspec(raw_handler)
    if len(raw_handler_arg_specs.args) > 1:
        error_text = f"{path} 映射函数参数个数不能多于1个"
        raise ValueError(error_text)

    web_url = WebUrl(path=path, handler=request_handler_creator(raw_handler, len(raw_handler_arg_specs.args)), **kwargs)
    registered_urls.append(web_url)
