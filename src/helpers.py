import ujson
from flask import Response
from src.config.config import *

def responsify(payload, links={}, http_code=200, mimetype="application/json"):
  if payload is not None and links:
    payload["links"] = links

  data = ujson.dumps(payload) if payload is not None else None

  return Response(
    response=data,
    status=http_code,
    mimetype=mimetype
  )
  
def errorit(msg, custom_code, http_code=400, info="", mimetype="application/json", debug_info=None, **kwargs):
  return Response(
    response=err_dict(msg, custom_code, ( "{}{}".format(API_URI, info) if info else ""), debug_info, **kwargs),
    status=http_code,
    mimetype=mimetype
  )

def err_dict(msg, code, info="", debug_info=None, **kwargs):
  if not isinstance(msg, list): # convert message to an array, if it is not
    msg = [msg]

  dc = {
    "errors": msg,
    "code": code,
    **kwargs
  }

  if not code:
    dc.pop("code")
  if info:
    dc.update({"info": info})
  if debug_info:
    dc.update({"debug_info": debug_info})

  dc["service"] = SERVICE_ID

  return ujson.dumps(dc)