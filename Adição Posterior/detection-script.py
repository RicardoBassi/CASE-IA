import cv2
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.engine import DefaultPredictor
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.data.datasets import register_coco_instances

from datetime import datetime
import uuid
import requests
from API_funcions import send_to_api

# Função para obter o endereço MAC do computador
def get_mac_address():
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(2, 7)][::-1])
    return mac

# URL da API do segundo sistema
api_url = "http://localhost:8000/api/receive_data/"

# Função para enviar informações para a API
try:
    # Faz uma solicitação GET para obter o token CSRF
    response = requests.get(api_url)

    # Obtém o token CSRF do cookie
    csrf_token = response.cookies.get('csrftoken')
except:
    print("csrf_token não encontrado")
    

register_coco_instances("my_dataset_train", {}, "../DatasetMouse/Computer mouse/train/_annotations.coco.json", "../DatasetMouse/Computer mouse/train")

my_dataset_train_metadata = MetadataCatalog.get("my_dataset_train")
dataset_dicts = DatasetCatalog.get("my_dataset_train")


cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_X_101_32x8d_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 2 #your number of classes + 1
cfg.MODEL.WEIGHTS = "output/model_final.pth"
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.95


predictor = DefaultPredictor(cfg)

# Inicializa a webcam
cap = cv2.VideoCapture(0)

while True:

    # Captura um frame da webcam
    ret, frame = cap.read()

    # Obter o endereço MAC do computador
    mac_address = get_mac_address()

    # Capturando informações para enviar para a API
    detection_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Faz a previsão usando o modelo
    outputs = predictor(frame)
    
    # Obtém o visualizador e desenha as previsões no frame
    v = Visualizer(frame[:, :, ::-1], metadata=my_dataset_train_metadata, scale=1.0)

    out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    
    # Mostra o frame com as previsões
    cv2.imshow("Real time object detection", out.get_image()[:, :, ::-1])

    # Verifica se pelo menos uma instância foi detectada
    if len(outputs["instances"]) > 0:
        # Obtém as coordenadas da bounding box
        pred_boxes = outputs["instances"].to("cpu").pred_boxes.tensor.numpy()
           
        # Itera sobre as bounding boxes
        for box in pred_boxes:
            xmin, ymin, xmax, ymax = box.astype(int)
            
            # Recorta a região da bounding box da imagem original
            region_cropped = frame[ymin:ymax, xmin:xmax].copy()

            # Mostra a região recortada
            cv2.imshow("Região Recortada", region_cropped)

        # api_list.append(mac_address, detection_time, "mouse", region_cropped)
        try:
            send_to_api(api_url, csrf_token, mac_address, detection_time, object_class="mouse")#, image_data=region_cropped)
        except:
            print("API indisponível")
    
    # Encerra o loop se a tecla 'q' for pressionada
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

# Libera os recursos
cap.release()
cv2.destroyAllWindows()