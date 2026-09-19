import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from openai import OpenAI

Chaves configuradas nas Environment Variables do Render

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)

Comandos disponíveis

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
texto = (
"🤖 KodyxBot\n\n"
"Seu assistente de programação com IA!\n\n"
"Digite /ajuda para ver os comandos."
)

await update.message.reply_text(texto)

async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
texto = "🧠 COMANDOS DO KODYXBOT\n\n"

for comando, descricao in COMMANDS.items():
    texto += f"/{comando} — {descricao}\n"

texto += (
    "\n💡 Exemplo:\n"
    "/codigo crie uma calculadora em Python\n\n"
    "Ou:\n"
    "/corrigir meu código está dando erro"
)

await update.message.reply_text(texto)

async def processar(update: Update, context: ContextTypes.DEFAULT_TYPE):
comando = update.message.text.split()[0]
comando = comando.replace("/", "").split("@")[0]

pedido = " ".join(context.args).strip()

if not pedido:
    await update.message.reply_text(
        f"❌ Você precisa escrever o que quer fazer.\n\n"
        f"Exemplo:\n/{comando} crie uma calculadora em Python"
    )
    return

instrucoes = COMMANDS.get(comando, "Ajude o usuário com programação.")

prompt = f"""

Você é o KodyxBot, um assistente de programação.

Tipo de pedido: {instrucoes}

Pedido do usuário:
{pedido}

Responda em português do Brasil.

Quando criar código:

- use blocos de código;

- informe a linguagem;

- mantenha o código completo;

- explique brevemente como usar;

- não invente bibliotecas ou funções que não existem.
  """
  
  try:
  await update.message.reply_text("🤖 KodyxBot está pensando...")
  
    resposta = client.responses.create(
      model="gpt-5.6",
      input=prompt
  )

  texto = resposta.output_text

  if not texto:
      texto = "❌ A IA não retornou uma resposta."

  # Divide respostas muito grandes para o limite do Telegram
  limite = 4000

  for inicio in range(0, len(texto), limite):
      await update.message.reply_text(
          texto[inicio:inicio + limite]
      )
  
  except Exception as erro:
  print("ERRO:", erro)
  
    await update.message.reply_text(
      "❌ Não consegui falar com a IA.\n\n"
      "Verifique se OPENAI_API_KEY está configurada corretamente "
      "no Render."
  )

def main():
app = Application.builder().token(TELEGRAM_TOKEN).build()

# Comandos básicos
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ajuda", ajuda))

# Comandos de programação
for comando in COMMANDS:
    app.add_handler(CommandHandler(comando, processar))

print("🤖 KodyxBot iniciado!")

app.run_polling()

if name == "main":
main()