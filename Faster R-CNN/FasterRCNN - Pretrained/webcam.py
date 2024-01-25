import cv2
import numpy as np
import time
from model_fasterrcnn import *

cap = cv2.VideoCapture(0)


while True:

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    hiegh = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    ret, frame = cap.read()

    # # Pré-processando a imagem
    # input_image = preprocess_image(frame)

    # # Realizando a inferência (substitua essa parte pelo seu código de detecção)
    # transform = transforms.Compose([transforms.ToTensor()])
    # img = transform(input_image).float()

    # pred = model([img])

    # pred_class = get_predictions(pred, objects="mouse")
    
    # draw_box(pred_class, img)

    # Exibindo a imagem na tela
    cv2.imshow("Webcam Object Detection", frame)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()        
cv2.destroyAllWindows()