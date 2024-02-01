import requests

def send_to_api(api_url, csrf_token, mac_address, detection_time, object_class):#, image_data):
    payload = {
        "mac_address": mac_address,
        "detection_time": detection_time,
        "object_class": object_class,
        # "image_data": image_data.tolist()  # Convertendo a imagem para uma lista antes de enviar
    }

    # Inclui o token CSRF no cabeçalho da solicitação
    headers = {
        'X-CSRFToken': csrf_token,
    }

    # Passa o token CSRF como um cookie no formato de dicionário
    cookies = {'csrftoken': csrf_token}

    response = requests.post(api_url, data=payload, headers=headers, cookies=cookies)
    
    if response.status_code == 201:
        print("Dados enviados com sucesso para a API!")
    else:
        print(f"Falha ao enviar dados para a API. Código de status: {response.status_code}")
        print(response.text)