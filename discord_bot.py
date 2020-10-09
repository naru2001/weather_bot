import discord
import urllib.request
import json
import re
import sys

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'NzA3NDQzMzkzNDI0MzkyMjIz.XrI45A.MH_hhzjamQMUPuCZ8gm9XMPMIx4'

hiratokana = {
    "あ": "ア", "い": "イ", "う": "ウ", "え": "エ", "お": "オ",
    "か": "カ", "き": "キ", "く": "ク", "け": "ケ", "こ": "コ",
    "さ": "サ", "し": "シ", "す": "ス", "せ": "セ", "そ": "ソ",
    "た": "タ", "ち": "チ", "つ": "ツ", "て": "テ", "と": "ト",
    "な": "ナ", "に": "ニ", "ぬ": "ヌ", "ね": "ネ", "の": "ノ",
    "は": "ハ", "ひ": "ヒ", "ふ": "フ", "へ": "ヘ", "ほ": "ホ",
    "や": "ヤ", "ゆ": "ユ", "よ": "ヨ",
    "ら": "ラ", "り": "リ", "る": "ル", "れ": "レ", "ろ": "ロ",
    "わ": "ワ", "を": "ヲ", "ん": "ン",
    "が": "ガ", "ぎ": "ギ", "ぐ": "グ", "げ": "ゲ", "ご": "ゴ",
    "ざ": "ザ", "じ": "ジ", "ず": "ズ", "ぜ": "ゼ", "ぞ": "ゾ",
    "だ": "ダ", "ぢ": "ヂ", "づ": "ヅ", "で": "デ", "ど": "ド",
    "ば": "バ", "び": "ビ", "ぶ": "ブ", "べ": "ベ", "ぼ": "ボ",
    "ぱ": "パ", "ぴ": "ピ", "ぷ": "プ", "ぺ": "ペ", "ぽ": "ポ",
    "ゃ": "ャ", "ゅ": "ュ", "ょ": "ョ"}


def hiragana_to_katakana(sentence):
    ret = ""
    for i in sentence:
        if i in hiratokana:
            ret += hiratokana[i]
        else:
            ret += i
    return ret


# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    # ターミナルにログイン通知
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):

    # メッセージ送信者がBotだった場合は無視
    if message.author.bot:
        return

    if message.content == "/bye":
        
        await client.logout()
        
    req_msg = re.compile(u"/weather (.+)").search(message.content) or\
        re.compile(u"/weather　(.+)").search(message.content)

    if req_msg:

        city_ids = {}
        city_data_path = "city_data.txt"

        with open(city_data_path) as w:
            for w_line in w:
                s = w_line.split(":")
                s[1].rstrip()
                city_ids[s[0]] = s[1]

        url_base = "http://weather.livedoor.com/forecast/webservice/json/v1?city=%s"
        
        if req_msg.group(1) in city_ids.keys():
            city_id = city_ids[req_msg.group(1)]
            response = urllib.request.urlopen(url_base % city_id).read()
            response = json.loads(response.decode("utf-8"))

            ret_msg = response["location"]["city"]
            ret_msg += "の天気は\n"
            for fc in response["forecasts"]:
                ret_msg += fc["dateLabel"]+": "+fc["telop"]+"\n"
            ret_msg += "です。\n"

            await message.channel.send(message.author.mention+"\n"+ret_msg)
        else:
            await message.channel.send(message.author.mention+"\n"+"知らねえよ自分で調べろ")

    name = hiragana_to_katakana(message.content)

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
