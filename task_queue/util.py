from aiohttp.web_response import json_response as jresponse


def json_dumps(*args, **kwargs) -> str:
    import json

    return json.dumps(*args, **kwargs, default=str)


def json_response(*args, **kwargs):
    return jresponse(*args, dumps=json_dumps, **kwargs)
