import uvicorn
import uuid
import os
from fastapi import HTTPException, UploadFile
from PIL import Image
from app import app
from helpers.net import crop_objects, remove_bg, cords_format


@app.get("/")
async def root():
    return {"message": "v0.0.1"}


@app.post('/prepare_image')
async def prepare_image(file: UploadFile):
    if file.content_type != 'image/jpeg' and file.content_type != 'image/png':
        raise HTTPException(status_code=400, detail="Invalid format image")

    img = Image.open(file.file)
    uid = uuid.uuid4()
    folder_path = os.path.join('static', str(uid))

    os.mkdir(folder_path)

    original_path = os.path.join(folder_path, 'original.jpg')
    img.save(original_path, 'JPEG')

    result = crop_objects(img)
    bg_removed_imgs = remove_bg(result['img'])
    cords = cords_format(result['cord'])

    for i in range(len(bg_removed_imgs)):
        im = bg_removed_imgs[i]

        im.save(folder_path + '/' + str(i) + '.png', 'PNG')

    images = []

    for i in range(len(cords)):
        image = {
            'y': cords[i]['x1'],
            'x': cords[i]['y1'],
            'src': '/static/' + str(uid) + '/' + str(i) + '.png',
            'id': str(i),
            'scaleX': 1,
            'scaleY': 1,
            'rotation': 0
        }

        images.append(image)

    return {'uid': uid, 'images': images, 'original': '/static/' + str(uid) + '/original.jpg'}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, root_path='/')
