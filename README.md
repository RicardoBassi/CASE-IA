## Contextualização
Este repositório foi criado com intuito de desenvolvimento de um case proposto. Este arquivo README foi incluído APÓS o prazo de entrega apenas para fins de contextualização dos arquivos do repositório.
A entrega do case são as duas pastas: DjangoAPI e Faster R-CNN. O diretório "Adições Posteriores" contém melhoramentos do código de detecção realizados APÓS a data final de entrega, portanto foram adicionados apenas para fins de aprofundamento do tema.

## Faster R-CNN
Esse diretório contém duas pastas com dois modelos independentes de detecção de objetos e uma pasta com um Dataset anotado de mouses de computador.

### FasterRCNN - Pretrained
O diretório "FasterRCNN - Pretrained" contém um jupyter notebook com a importação de um modelo pré treinado em várias instâncias. São realizadas predições em imagens não rotuladas para teste, e a seleção da instância de interesse "mouse".
No arquivo "model_fasterrcnn.py" é realizada a importação do modelo, criadas funções para envio de dados para uma API, funções para cortes da imagem detectada pela webcamm e função para preprocessamento da imagem captada.
O arquivo "script_detection.py" é o arquivo principal de detecção deste modelo. Ele é responsável pela ativação da webcam, leitura da imagem e detecção de objetos. Este aquivo deve iniciar a webcam e ao detectar o objeto de interesse, o que está no interior da bounding box deve ser enviado para a API juntamente com a data e hora, MAC e classe do objeto.
Devido ao baixo fps da webcam ao iniciar o script, a parte de envio para API não foi incluida à entrega do arquivo final.
O arquivo "webcam.py" apenas inicia a webcam com as configurações padrão para o teste de fps. As imagens incluidas na pasta podem ser utilizadas para teste do modelo.

### Detectron2
Esse diretório contém um jupyter notebook que inicia um modelo detectron2, treina com o banco de dados anotado e testa o resultado do treinamento com predições.
O arquivo adicionado a entrega contém erros de execução, erros estes devidos à incompatibilidade com o ambiente virtual em que o código foi executado pela última vez.
Embora contenha erros, este modelo foi treinado e seus pesos foram guardados. (Este modelo é corrigido e melhorado e está no diretório "Adições Posteriores").

### DatasetMouse
Contém o dataset com as anotações de mouses de computador. Já está dividido em treino, teste e validação.

## DjangoAPI
Contém o esboço da API desenvolvida em django. Contém apenas algumas funções de cadastro de user e superuser, adição de views de login, logout e renew.

## Adições Posteriores
Nesse diretório foi adicionado o complemento para o modelo detectron2. O modelo foi retreinado e foi escrito o código de reconhecimento de objetos e de envio para API.
Este modelo e script funcionam relativamente bem para a detecção de objetos, basta executar o notebook com o dataset anotado do objeto de escolha, ajustar os parâmetros, e após realizar o treinamento, executar o script de detecção.
O frame recortado do objeto detectado é exibido em uma nova janela. O código pode ser facilmente ajustado para o envio para a API. Este modelo não compromete de forma severa o FPS da webcam.
