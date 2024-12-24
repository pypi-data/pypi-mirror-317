from openai import OpenAI
import base64


#criar Classe
class LeitorDeImagens():
    def __init__(self, modeloLLM, chaveAPI):
        self.imagem = ''
        self.modelo = modeloLLM
        self.apiKey = chaveAPI

    def lerImagem(self, imagem):
        try:   
            self.imagem = imagem

#tratar imagem
# Codificando uma imagem
            def codificarImagem(imagem):
                
                with open(imagem, 'rb') as imagem:
                    return base64.b64encode(imagem.read()).decode('utf-8')
                
            imagemCodificada = codificarImagem(self.imagem)

#dar descrição da imagem

            client = OpenAI(api_key= self.apiKey)
            response = client.chat.completions.create(
                model=f"{self.modelo}",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "escreva o que você vê na imagem"},
                            {
                                "type": "image_url",
                                "image_url":{ 
                                    'url': f"data:image/jpeg;base64,{imagemCodificada}"
                                            
                                },
                            
                                
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )
            detalhesDaImagem = response.choices[0].message.content

            print(detalhesDaImagem)


        except Exception as e:
           return f"Erro ao analisar imagem: {str(e)}"
