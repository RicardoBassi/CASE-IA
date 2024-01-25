import cv2
import numpy as np
import requests
from datetime import datetime

# Importações para o modelo de predição
import torchvision
from torchvision import  transforms 
import torch
from torch import no_grad

from PIL import Image
import matplotlib.pyplot as plt

import uuid


# URL da API do segundo sistema
api_url = "http://localhost:8000/api/detections/"

# Função para enviar informações para a API
def send_to_api(mac_address, detection_time, object_class, image_data):
    payload = {
        "mac_address": mac_address,
        "detection_time": detection_time,
        "object_class": object_class,
        "image_data": image_data.tolist()  # Convertendo a imagem para uma lista antes de enviar
    }
    response = requests.post(api_url, json=payload)
    
    if response.status_code == 201:  # Código 201 indica criação bem-sucedida no Django Rest Framework
        print("Dados enviados com sucesso para a API!")
    else:
        print(f"Falha ao enviar dados para a API. Código de status: {response.status_code}")
        print(response.text)

# Função para obter o endereço MAC do computador
def get_mac_address():
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(2, 7)][::-1])
    return mac


def get_predictions(pred, threshold=0.2, objects=None):
    predicted_classes= [(COCO_INSTANCE_CATEGORY_NAMES[i],p,[(box[0], box[1]), (box[2], box[3])]) for i,p,box in zip(list(pred[0]['labels'].numpy()),pred[0]['scores'].detach().numpy(),list(pred[0]['boxes'].detach().numpy()))]
    predicted_classes=[  stuff  for stuff in predicted_classes  if stuff[1]>threshold ]
    
    if objects and predicted_classes :
        predicted_classes=[ (name, p, box) for name, p, box in predicted_classes if name in  objects ]
    return predicted_classes


# Função para enviar apenas as regiões dentro das bounding boxes para a API
def send_regions_to_api(mac_address, detection_time, object_class, regions):
    for region in regions:
        _, image_data = cv2.imencode('.jpg', region)  # Convertendo a região para JPEG antes de enviar
        # Enviar informações para a API (ajuste conforme necessário)
        send_to_api(mac_address, detection_time, object_class, image_data)


# Restante da função draw_box
def draw_box(pred_class, img, rect_th=2, text_size=0.5, text_th=2, download_image=False, img_name="img"):

    # Obter o endereço MAC do computador
    mac_address = get_mac_address()

    image = (np.clip(cv2.cvtColor(np.clip(img.numpy().transpose((1, 2, 0)), 0, 1), cv2.COLOR_RGB2BGR), 0, 1) * 255).astype(np.uint8).copy()

    regions_to_send = []
    times_to_send = []

    for predicted_class in pred_class:
        label = predicted_class[0]
        probability = predicted_class[1]
        box = predicted_class[2]

        t = round(box[0][0].tolist())
        l = round(box[0][1].tolist())
        r = round(box[1][0].tolist())
        b = round(box[1][1].tolist())

        # Dando informações breves sobre o retângulo, classe e probabilidade.
        print(f"\nLabel: {label}")
        print(f"Box coordinates: {t}, {l}, {r}, {b}")
        print(f"Probability: {probability}")

        # Desenhando retângulo e adicionando texto na imagem com base na classe e tamanho.
        cv2.rectangle(image, (t, l), (r, b), (0, 255, 0), rect_th)
        cv2.rectangle(image, (t, l), (t+110, l+17), (255, 255, 255), -1)
        cv2.putText(image, label, (t+10, l+12),  cv2.FONT_HERSHEY_SIMPLEX, text_size, (0,255,0), thickness=text_th)
        cv2.putText(image, label+": "+str(round(probability, 2)), (t+10, l+12),  cv2.FONT_HERSHEY_SIMPLEX, text_size, (0, 255, 0),thickness=text_th)

        # Recortando a região dentro da bounding box
        region = image[l:b, t:r, :]
        regions_to_send.append(region)

        # Capturando informações para enviar para a API
        detection_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        times_to_send.append(detection_time)

        # Exibindo a região recortada em uma nova janela
        # cv2.imshow("Region", region)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    # Exibindo imagem
    cv2.imshow("Webcam Object Detection", image)

    if download_image:
        cv2.imwrite(f'{img_name}.png', image)

    object_class = "Mouse"
    # send_regions_to_api(mac_address, detection_time, object_class, regions_to_send)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    del img
    del image


# Contrução do Modelo
def model(x):
    with torch.no_grad():
        yhat = model_(x)
    return yhat
    
model_ = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
model_.eval()

print("model imported")

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model_.to(device)

# Classes
COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']


# Função para pré-processar a imagem
def preprocess_image(img):
    img = cv2.resize(img, (800, 600))
    img = img / 255.0
    # img = np.expand_dims(img, axis=0)
    return img