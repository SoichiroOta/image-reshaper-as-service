import os
import io
import json

import responder

from reshaping import (
    load_img,
    reshape,
    save_img
)


env = os.environ
DEBUG = env.get('DEBUG') in ['1', 'True', 'true']
IMAGE_FORMAT = env.get('IMAGE_FORMAT')
RESPONSE_TYPE = env.get('RESPONSE_TYPE')
SIZE = int(env['SIZE'])

api = responder.API(debug=DEBUG)


@api.route("/")
async def index(req, resp):
    body = await req.content
    img = load_img(io.BytesIO(body))
    format_str = IMAGE_FORMAT if IMAGE_FORMAT else img.format
    reshaped_img = reshape(img, SIZE)
    if RESPONSE_TYPE == 'JSON':
        resp.media = reshaped_img.tolist()
    else:
        resp.content = save_img(reshaped_img, format_str=format_str)


if __name__ == "__main__":
    api.run()
