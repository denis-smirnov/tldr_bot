# -*- coding: utf-8 -*-
import telepot
import logging
from app.parser import extract_text
from app.summarizer import summarize_text


def launch_bot(bot):

    _extract_upper_bound = 4096
    _default_extract_fraction = .25

    _response_dict = {
        "parse_error": "Неудалось извлечь данные, проверьте корректность ссылки.",
        "start": "Отправьте мне ссылку на новость или статью, а я подготовлю краткое содержание"
    }

    def process_message(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, chat_type, chat_id)

        if content_type == "text":
            if msg["text"] == "/start":
                bot.sendMessage(chat_id, _response_dict["start"])
            else:
                try:
                    title, text = extract_text(msg["text"])
                    extract = summarize_text(text, _default_extract_fraction, _extract_upper_bound)

                    bot.sendMessage(chat_id, title)
                    bot.sendMessage(chat_id, extract)

                except Exception as ex:
                    logging.exception(ex)
                    bot.sendMessage(chat_id, _response_dict["parse_error"])

    bot.message_loop(process_message, run_forever=True)
