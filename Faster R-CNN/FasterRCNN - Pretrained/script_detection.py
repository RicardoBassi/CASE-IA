import cv2
import numpy as np
from model_fasterrcnn import *

# Iniciando a WebCam
cap = cv2.VideoCapture(0)

while True:

    # Obter o endereço MAC do computador
    mac_address = get_mac_address()

    print(mac_address)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    hiegh = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    ret, frame = cap.read()

    # Pré-processando a imagem da webcam
    # input_image = preprocess_image(frame)

    # Pegar imagem de diretório em vez da webcam
    img_path='pessoa-usando-mouse.jpg'
    half = 0.5
    image = Image.open(img_path)
    image.resize([int(half * s) for s in image.size] )
    input_image = image

    # Realizando a inferência (substitua essa parte pelo seu código de detecção)
    transform = transforms.Compose([transforms.ToTensor()])
    img = transform(input_image).float()

    # img = torch.stack(image).to(device)

    pred = model([img])

    # bounding_box = pred[0]['boxes'][0].tolist()

    pred_class = get_predictions(pred, objects="mouse")
    
    draw_box(pred_class, img)

    # Exibindo a imagem com as caixas delimitadoras
    cv2.imshow("Webcam Object Detection", frame)

    # Pressione 'q' para sair
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

# Liberando recursos
cap.release()
cv2.destroyAllWindows()