import logging
import random
from uuid import uuid4

from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.utils.helpers import escape_markdown


docAzul = open("azul.txt","r+")
docAmarelo = open("amarelo.txt","r+")
docVermelho = open("vermelho.txt","r+")

azul = set()
vermelho =set()
amarelo = set()

raids = {}
raidText="""
🔰 RAID LEVEL {}
🐣 Chefe: {}
⏳ Hora: {}
🏟 Gym: {}
🌎 Local: {}
"""


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def my_debug(update):
    print(update.message.from_user.username)
    print(update.message.text)

def azul_seting():
    linhas = docAzul.readlines()
    palavras=[]
    for linha in linhas:
        palavras = linha.split()
    for palavra in palavras:
        azul.append(" "+str(palavra))
def vermelho_seting():
    linhas = docVermelho.readlines()
    palavras=[]
    for linha in linhas:
        palavras = linha.split()
    for palavra in palavras:
        vermelho.append(" "+str(palavra))
def amarelo_seting():
    linhas = docAmarelo.readlines()
    palavras=[]
    for linha in linhas:
        palavras = linha.split()
    for palavra in palavras:
        amarelo.append(" "+str(palavra))

def start(update, context):
    my_debug(update)
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    my_debug(update)
    """Send a message when the command /help is issued."""
    helpText="""
    /raid (level, chefe, hora, gym, local): inicia uma nova raid e retorna um RAID ID;
    /entrar (RAID ID), entra na raid;
    /sair (RAID ID), sai da raid[NÃO FUNCIONA AINDA];
    /acordo : TEXTÃO do acordo;
    /planilha : planilha de informações dos membros;
    /time (azul, vermelho, amarelo) : marca todos os membros do time;
    /adicionar (SUA TAG) (azul, vermelho, amarelo) : adiciona sua tag ao time;
    /remover (SUA TAG) (azul, vermelho, amarelo) : remove sua tag do time;
    /info : Informações do bot, (TEXTÃO, evite usar);
    """
    update.message.reply_text(helpText)

def acordo(update, context):
    my_debug(update)
    """Send a message when the command /start is issued."""
    acordoText="""
    Nós também temos um acordo de rodízio no ginásio que DEVE ser respeitada pelos membros do grupo (vide planilha):
1 - Só pode derrubar o ginásio após o primeiro defensor completar 3h de permanência;
1.1 - Esse defensor deve ser do grupo;
1.2 - Se o 1º defensor não for do grupo (principalmente os fly conhecidos) pode derrubar o gym todo ou até restar membros do grupo e assim já adiantar a contagem de suas horas;
1.3 - Sendo desrespeitado o ponto 1, quem perdeu a posição no gym pode derrubar imediatamente, RESETANDO O TEMPO de permanência dele.
2 - Após o gym ser derrubado, a cor determinada é daquele, DO GRUPO, que ocupar a vaga primeiro;
Recomendações para melhor proveito do acordo:
*Quando alguém tomar o ginásio, avisem para os outros membros de sua cor aproveitarem as moedas também, e evitar gente de fora no gym;
*Quando virem o gym ser atacado antes da hora, avisem para os defensores poderem alimentar os seus pokémons, e evitar o item 1.3;
*Se precisar batalhar no gym para cumprir missão, avise para que os defensores possam dar frutas e evitar que eles sejam derrubados antes da hora;
*Não dar frutas aos seus pokémons para não dificultar a derrubada do mesmo depois das 3h do gym;
*Não colocar seu pokemon no gym caso já tenha pego as 50 moedas diárias. Uma hora você consegue sua medalha de ouro no gym e temos mais 2 pokestops para você pegar itens. Salvo se você estiver indo embora ou for no fim do dia visando a possibilidade de permanência até o próximo dia;
*Viu alguma regra ser desrespeitada? Procure sempre a conversa antes da retaliação, pois no meio das ações pode ter ocorrido ações de terceiros que desconhecem o acordo e assim vamos mantendo a boa convivência. Sendo assim, está aberta a possibilidade de acordos temporários para soluções pontuais;
*Viu alguém jogando pokémon no IMD? Converse sobre o grupo e sobre nosso acordo convidando-o pro grupo. Se ele não quiser entrar ou não usar o telegram, pergunte se ele vai respeitar o acorde e coloque-o na lista das pessoas do IMD que não estão no grupo.
    """
    update.message.reply_text(acordoText)


def raid(update, context):
    my_debug(update)
    RAID_ID = random.randint(0, 10000)
    while RAID_ID in raids:
        RAID_ID = random.randint(0, 10000)

    # Some standard values for missing arguments cases
    level = "?"
    boss = "?"
    time = "?"
    gym = "IMD"

    try:
        level = context.args[0]
        boss = context.args[1]
        time = context.args[2]
        gym = context.args[3]
        local = context.args[4]

    except:
        local = "UFRN"

    thisRaidText = "RAID ID " + str(RAID_ID) + "\n" + raidText.format(level, boss, time, gym, local)
    raids[RAID_ID] = [level, boss, time, gym, local, thisRaidText, 1]
    print(raids[RAID_ID])
    # raids.append([RAID_ID, level, boss, time, gym, local, thisRaidText, 1])
    update.message.reply_text(thisRaidText)
    # update.message.reply_text("RAID ID: "+str(RAID_ID))

def info(update, context):
    my_debug(update)
    """Send a message when the command /help is issued."""
    infoText="""
IMD_POGO_BOT
Versão: Alpha0.1

Este bot foi criado para ajudar a organização do grupo de pokemon go do IMD.

Quer ajudar no desenvolvimento? Entre no grupo de desenvolvimento https://t.me/joinchat/LrZ0NAvToUjayFW7X11xqA.

Repositório:
ssh: git@github.com:GuiEgle/IMD-POGO_bot.git
https: https://github.com/GuiEgle/IMD-POGO_bot.git

IMPORTANTE(dicas de uso):
Os comandos vão funcionar melhor se executados em linhas ISOLADAS.
O bot ainda está em desenvolvimento caso você execute um comando e ele aparentemente falhou, evite repetir.

Sobre o estado atual do bot:
O bot ainda está sendo hosteado em um computador pessoal, o de @GuiEgle, isso significa que ele só funciona se o computador estiver executando o processo responsável pelo bot. Como ele ainda está em desenvolvimento, o processo tera de ser reiniciado várias vezes, o que implica no desligamento do bot.

O bot não está com memória persistente, logo sempre que reiniciado os grupos de times serão esquecidos(IMPORTANTE).

Encontrou um problema?
Você pode entrar em contato com @GuiEgle, @TONHAUNM ou @ppaulo_hh.
Ou mande um email para guiegle@hotmail.com.

Para começar digite "/help".

É isso, bom proveito!
    """
    update.message.reply_text(infoText)


def planilha(update, context):
    my_debug(update)
    """Send a message when the command /help is issued."""
    link_planilha="""
    https://bit.ly/2M0O29N
    """
    update.message.reply_text(link_planilha)

def adicionar(update, context):
    my_debug(update)
    """Send a message when the command /help is issued."""
    if str(context.args[1]) == "azul":
        azul.add(context.args[0])
    elif str(context.args[1]) == "vermelho":
        vermelho.add(context.args[0])
    elif str(context.args[1]) == "amarelo":
        amarelo.add(context.args[0])

def remover(update, context):
    my_debug(update)
    """Send a message when the command /help is issued."""
    if str(context.args[1]) == "azul":
        azul.remove(context.args[0])
    elif str(context.args[1]) == "vermelho":
        vermelho.remove(context.args[0])
    elif str(context.args[1]) == "amarelo":
        amarelo.remove(context.args[0])

def time(update, context):
    my_debug(update)
    saida = ""
    if context.args[0] == "azul":
        for membro in azul:
            saida += " {}".format(str(membro))
    elif context.args[0] == "vermelho":
        for membro in vermelho:
            saida += " {}".format(str(membro))
    elif context.args[0] == "amarelo":
        for membro in amarelo:
            saida += " {}".format(str(membro))
    update.message.reply_text(saida)

def entrar(update, context):
    my_debug(update)
    # for raid in raids:
        # if str(raid[0])==str(context.args[0]):
        #     raid[6] += "\n{}. {}".format(raid[7], update.message.from_user.username)
        #     raid[7]+=1
    raids[int(context.args[0])][5] += "\n{}. {}".format(raids[int(context.args[0])][6], update.message.from_user.username)
    raids[int(context.args[0])][6] += 1
    update.message.reply_text(raids[int(context.args[0])][5])


def sair(update, context):
    my_debug(update)



def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Caps",
            input_message_content=InputTextMessageContent(
                query.upper())),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Bold",
            input_message_content=InputTextMessageContent(
                "*{}*".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN)),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Italic",
            input_message_content=InputTextMessageContent(
                "_{}_".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN))]

    update.inline_query.answer(results)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    botToken = "883043016:AAHkO92cdcMjGBP_nAX4beRYiOu0yRb_j3w"
    updater = Updater(botToken, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help, pass_user_data=True))
    dp.add_handler(CommandHandler("info", info, pass_user_data=True))
    dp.add_handler(CommandHandler("acordo", acordo))
    dp.add_handler(CommandHandler("raid", raid, pass_args=True))
    dp.add_handler(CommandHandler("planilha", planilha))
    dp.add_handler(CommandHandler("adicionar", adicionar, pass_args=True))
    dp.add_handler(CommandHandler("remover", remover, pass_args=True))
    dp.add_handler(CommandHandler("time", time, pass_args=True))
    dp.add_handler(CommandHandler("entrar", entrar, pass_args=True))
    dp.add_handler(CommandHandler("sair", sair, pass_args=True))

    dp.add_handler(InlineQueryHandler(inlinequery))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    azul_seting()
    amarelo_seting()
    vermelho_seting()
    main()
