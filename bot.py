import os
from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
from openai import OpenAI


TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)


PROMPTS = {
    "codigo": "Crie código de programação para o pedido abaixo. Explique brevemente como usar.",
    "programa": "Crie um programa completo para o pedido abaixo. Organize o código e explique como executar.",
    "explicar": "Explique o código ou conceito abaixo de forma simples e didática.",
    "corrigir": "Analise o código abaixo, encontre os problemas e forneça uma versão corrigida.",
    "melhorar": "Melhore o código abaixo mantendo seu objetivo original.",
    "converter": "Converta o código abaixo para a linguagem solicitada.",
    "python": "Ajude com programação Python usando boas práticas.",
    "javascript": "Ajude com programação JavaScript usando boas práticas.",
    "html": "Crie ou corrija HTML para o pedido abaixo.",
    "css": "Crie ou corrija CSS para o pedido abaixo.",
    "sql": "Crie ou corrija SQL para o pedido abaixo.",
    "api": "Crie uma API para o pedido abaixo e explique sua estrutura.",
    "bot": "Ajude a criar um bot para o pedido abaixo.",
    "debug": "Faça uma análise de debug do problema abaixo e mostre possíveis correções.",
    "funcao": "Crie uma função de programação para realizar o pedido abaixo.",
    "projeto": "Planeje a estrutura de um projeto de programação para o pedido abaixo.",
    "comentar": "Adicione comentários úteis ao código abaixo sem alterar sua lógica.",
    "otimizar": "Otimize o código abaixo, explicando as principais melhorias.",
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Olá! Sou seu assistente de programação.\n\n"
        "Use /ajuda para ver todos os comandos."
    )


async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    comandos = "\n".join(
        f"/{nome} — {descricao}"
        for nome, descricao in [
            ("codigo", "criar código"),
            ("programa", "criar programa"),
            ("explicar", "explicar código"),
            ("corrigir", "corrigir código"),
            ("melhorar", "melhorar código"),
            ("converter", "converter linguagem"),
            ("python", "ajuda com Python"),
            ("javascript", "ajuda com JavaScript"),
            ("html", "criar HTML"),
            ("css", "criar CSS"),
            ("sql", "criar SQL"),
            ("api", "criar API"),
            ("bot", "criar bot"),
            ("debug", "analisar erro"),
            ("funcao", "criar função"),
            ("projeto", "planejar projeto"),
            ("comentar", "comentar código"),
            ("otimizar", "otimizar código"),
        ]
    )

    await update.message.reply_text(
        "🧠 COMANDOS DO ASSISTENTE\n\n"
        + comandos
        + "\n\nExemplo:\n"
        "/codigo crie uma calculadora em Python"
    )


async def ia_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text.split()[0].replace("/", "").split("@")[0]

    pedido = " ".join(context.args).strip()

    if not pedido:
        await update.message.reply_text(
            f"❌ Use o comando assim:\n\n"
            f"/{command} o que você quer fazer"
        )
        return

    system_prompt = PROMPTS.get(
        command,
        "Ajude o usuário com programação."
    )

    await update.message.reply_text("🧠 Pensando...")

    try:
        response = client.responses.create(
            model="gpt-5.6",
            instructions=system_prompt,
            input=pedido,
        )

        resposta = response.output_text

        # Telegram possui limite de tamanho para mensagens.
        limite = 4000

        for i in range(0, len(resposta), limite):
            await update.message.reply_text(
                resposta[i:i + limite]
            )

    except Exception as e:
        print("Erro:", e)

        await update.message.reply_text(
            "❌ Ocorreu um erro ao conversar com a IA."
        )


async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    comandos = [
        BotCommand("start", "iniciar o bot"),
        BotCommand("ajuda", "ver todos os comandos"),
        BotCommand("codigo", "criar código"),
        BotCommand("programa", "criar programa"),
        BotCommand("explicar", "explicar código"),
        BotCommand("corrigir", "corrigir código"),
        BotCommand("melhorar", "melhorar código"),
        BotCommand("converter", "converter código"),
        BotCommand("python", "ajuda com Python"),
        BotCommand("javascript", "ajuda com JavaScript"),
        BotCommand("html", "criar HTML"),
        BotCommand("css", "criar CSS"),
        BotCommand("sql", "criar SQL"),
        BotCommand("api", "criar API"),
        BotCommand("bot", "criar bot"),
        BotCommand("debug", "debug de código"),
        BotCommand("funcao", "criar função"),
        BotCommand("projeto", "planejar projeto"),
        BotCommand("comentar", "comentar código"),
        BotCommand("otimizar", "otimizar código"),
    ]

    await app.bot.set_my_commands(comandos)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ajuda", ajuda))

    for command in PROMPTS:
        app.add_handler(CommandHandler(command, ia_command))

    print("🤖 Bot iniciado!")

    await app.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
