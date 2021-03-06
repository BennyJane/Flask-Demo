# -*- coding: utf-8 -*-
import math
import json
from flask import jsonify, Response
from proStruct.utils.date_tools import json_iso_dttm_ser

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for, current_app


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='blog.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['BLUELOG_ALLOWED_IMAGE_EXTENSIONS']


def iPagination(params):
    ret = {
        "is_prev": 1,
        "is_next": 1,
        "from": 0,
        "end": 0,
        "current": 0,
        "total_pages": 0,
        "page_size": 0,
        "total": 0,
        "url": params['url']
    }

    total = params['total']
    page_size = params['page_size']
    page = params['page']
    half_page_display = int(params['half_page_display'])
    total_pages = int(math.ceil(total / page_size))
    total_pages = total_pages if total_pages > 0 else 1
    if page <= 1:
        ret['is_prev'] = 0

    if page >= total_pages:
        ret['is_next'] = 0

    if page - half_page_display > 0:
        ret['from'] = page - half_page_display
    else:
        ret['from'] = 1

    if page + half_page_display <= total_pages:
        ret['to'] = page + half_page_display
    else:
        ret['to'] = total_pages
    ret['current'] = page  # 其实就是 page的值
    ret['total'] = total
    ret['total_pages'] = total_pages
    ret['page_size'] = page_size
    ret['range'] = range(ret['from'], ret['to'] + 1)
    return ret


class RestfulResponse(object):
    ok = 200
    unAuthError = 401
    paramsError = 400
    servererror = 500

    code = ok
    message = ""
    data = []

    @classmethod
    def success(cls, message: str, code: int, data=None):
        return jsonify({"code": code or cls.code, "msg": message or cls.message, "data": data or cls.data})

    @classmethod
    def success_including_date(cls, message: str, code: int, data=None):
        # return jsonify({"code": code or cls.code, "msg": message or cls.message, "data": data or cls.data})
        res = {
            "code": code or cls.code,
            "msg": message or cls.message,
            "data": data or cls.data,
        }

        return Response(
            json.dumps(res, default=json_iso_dttm_ser, ignore_nan=True, ensure_ascii=False),
            status=code or cls.code, mimetype="application/json"
        )

    @classmethod
    def fail_result(cls, message: str, code: int, data=None):
        res = {
            "code": code or cls.code,
            "msg": message or cls.message,
            "data": data or cls.data,
        }
        return Response(
            # 设置ensure_ascii 为False, 支持中文的显示
            json.dumps(res, default=json_iso_dttm_ser, ensure_ascii=False),
            # json.dumps(obj, default=utils.json_int_dttm_ser, ignore_nan=True),
            status=code or cls.code,
            mimetype='application/json'
        )
