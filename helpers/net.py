import torch
import cv2
from torchvision.transforms import transforms
import torchvision.transforms.functional as f
from rembg.bg import remove
from PIL import Image


model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
transform_to_img = transforms.ToPILImage()


def crop_objects(img):
    results = model(img)
    imgs = results.crop(save=False)
    result_imgs = {'img': [], 'cord': []}

    for i in range(len(imgs)):
        result_imgs['img'].append(imgs[i]['im'])
        result_imgs['cord'].append(imgs[i]['box'])

    return result_imgs


def remove_bg(imgs):
    result = []

    for i in range(len(imgs)):
        prepare_transform = transforms.ToTensor()
        post_stransform = transforms.ToPILImage()

        img = imgs[i]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)

        img_tensor = prepare_transform(img)
        img_tensor = f.autocontrast(img_tensor)
        img = post_stransform(img_tensor)
        img = remove(img)

        result.append(img)

    return result


def cords_format(cords):
    result = []

    for i in range(len(cords)):
        y1 = cords[i][0].item()
        x1 = cords[i][1].item()
        y2 = cords[i][2].item()
        x2 = cords[i][3].item()

        result.append({'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2})

    return result
