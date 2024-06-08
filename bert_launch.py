from transformers import BertForSequenceClassification, BertTokenizer,AutoTokenizer,BertModel, AutoModelForMaskedLM
import telebot
BERT_PATH = 'bertorch_312_bpe_30k_MLM_20'
# model = AutoImageProcessor.from_pretrained(BERT_PATH)
tokenizer = AutoTokenizer.from_pretrained(BERT_PATH)
model = BertForSequenceClassification.from_pretrained(BERT_PATH)
from transformers import pipeline
mask_filler = pipeline("fill-mask", model=BERT_PATH, tokenizer=tokenizer)
bot = telebot.TeleBot(TG_TOKEN)

def get_answer(text):
    try:
        if text.count('$') == 1:
            text = text.replace('$', '[MASK]')
            print(text)
            preds = mask_filler(text)
            out = ['Вот варианты ответов:\n']
            for pred in preds:
                out.append(pred['sequence'])
            out = '\n'.join(out)
        else:
            out = 'Должен быть один символ $'
        return out
    except Exception as e:
        print(e)
        return 'Попробуй еще!'

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    res = get_answer(message.text)
    bot.send_message(message.chat.id, res)


if __name__=='__main__':
    
    bot.polling(none_stop=True)
