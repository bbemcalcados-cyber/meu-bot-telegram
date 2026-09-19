import os

from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)


COMMANDS = {
    "codigo": "Criar código",
    "programa": "Criar um programa",
    "explicar": "Explicar código",
    "corrigir": "Corrigir código",
    "melhorar": "Melhorar código",
    "python": "Programar em Python",
    "javascript": "Programar em JavaScript",
    "html": "Criar HTML",
    "css": "Criar CSS",
    "sql": "Criar SQL",
    "api": "Criar uma API",
    "bot": "Criar um bot",
    "debug": "Encontrar erros",
    "funcao": "Criar uma função",
    "converter": "Converter código",
    "projeto": "Planejar um projeto",
    "otimizar": "Otimizar código",
    "comentar": "Comentar código",
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 KodyxBot\n\n"
        "Seu assistente de programação com IA!\n\n"
        "Digite /ajuda para ver os comandos."
    )


async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = "🧠 COMANDOS DO KODYXBOT\n\n"

    for comando, descricao in COMMANDS.items():
        texto += f"/{comando} - {descricao}\n"

    texto += (
        "\nExemplo:\n"
        "/codigo crie uma calculadora em Python"
    )

    await update.message.reply_text(texto)


async def processar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    comando = update.message.text.split()[0]
    comando = comando.replace("/", "").split("@")[0]

    pedido = " ".join(context.args).strip()

    if not pedido:
        await update.message.reply_text(
            f"❌ Escreva o que você quer fazer.\n\n"
            f"Exemplo:\n/{comando} crie uma calculadora em Python"
        )
        return

    tipo = COMMANDS.get(comando, "Ajuda de programação")

    prompt = f"""
Você é o KodyxBot, um assistente de programação.

Tipo de solicitação:
{tipo}

Pedido do usuário:
{pedido}

Responda em português do Brasil.

Se criar código:
- use bloco de código;
- informe a linguagem;
- forneça código completo;
- explique brevemente como usar;
- não invente bibliotecas.
"""

    try:
        await update.message.reply_text("🤖 Pensando...")

        response = client.responses.create(
            model="gpt-5.6",
            input=prompt
        )

        resposta = response.output_text

        if not resposta:
            resposta = "Não consegui gerar uma resposta."

        limite = 4000

        for inicio in range(0, len(resposta), limite):
            await update.message.reply_text(
                resposta[inicio:inicio + limite]
            )

    except Exception as erro:
        print("ERRO:", erro)

        await update.message.reply_text(
            "❌ Erro ao conectar com a IA.\n\n"
            "Verifique as configurações do Render."
        )


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ajuda", ajuda))

    for comando in COMMANDS:
        app.add_handler(
            CommandHandler(comando, processar)
        )

    print("KodyxBot iniciado!")

    app.run_polling()


if __name__ == "__main__":
    main()