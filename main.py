import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class AssistenteEspecialista:
    def __init__(self, assunto, nome_bot="Carlinhos"):
        self.assunto = assunto
        self.nome = nome_bot

        # Instruções de Sistema: Definem as regras e a persona do modelo
        instrucoes_sistema = (
            f"Você é um assistente virtual altamente especializado em {self.assunto}. "
            f"Seu nome é {self.nome}. Você deve agir de forma extremamente humana e amigável"
            f"Na saudação, apresente-se pelo seu nome, "
            f"reforce que é especialista em {self.assunto} e pergunte como pode ajudar no mundo da {self.assunto}."
        )

        # Inicializa o modelo passando as instruções
        self.model = genai.GenerativeModel(
            model_name="gemini-3.5-flash", system_instruction=instrucoes_sistema
        )

        self.chat = self.model.start_chat(history=[])

    def conversar(self, mensagem):
        # Envia a mensagem para o modelo e retorna a resposta
        resposta = self.chat.send_message(mensagem)
        return resposta.text


# 2. Fluxo principal de execução
if __name__ == "__main__":
    # Captura o assunto inicial
    print("Sobre qual assunto você gostaria de conversar sobre?")
    assunto_escolhido = input("> ")

    # Instancia o objeto do assistente passando o assunto (fora do corpo da classe)
    assistente = AssistenteEspecialista(assunto=assunto_escolhido)

    print(f"Olá, sou seu assistente virtual, especialista em {assunto_escolhido}.")

    # Inicia o loop de repetição para manter a conversa ativa no terminal
    while True:
        mensagem_usuario = input("> ")

        # Trava de segurança para sair do loop
        if mensagem_usuario.lower() in ["sair", "encerrar", "tchau", "0"]:
            print("Encerrando o assistente...")
            break

        try:
            resposta = assistente.conversar(mensagem_usuario)
            print(f"\n{resposta}\n")
        except Exception as e:
            print(f"\n[Erro na comunicação com a API]: {e}\n")
