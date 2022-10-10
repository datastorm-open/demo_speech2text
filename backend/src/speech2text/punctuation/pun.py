import os

from .. import config

output_path = config.Rshiny_path + "/Rshiny"
input_text_path = config.Rshiny_path +"/Rshiny/output/output.txt"


def PUN(input=input_text_path, output_adress=output_path):
    from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

    # load punctuation model
    tokenizer = AutoTokenizer.from_pretrained(config.model_path + "/model/punctuation-model2")
    model = AutoModelForTokenClassification.from_pretrained(config.model_path + "/model/punctuation-model2")

    # for app
    input_doc = open(input, encoding="utf-8")
    pun = pipeline('ner', model=model, tokenizer=tokenizer)
    output_json = pun(input_doc.read())

    # # for text
    # pun = pipeline('ner', model=model, tokenizer=tokenizer)
    # output_json = pun(input)

    text = ''
    for n in output_json:
        result = n['word'].replace('▁', ' ') + n['entity'].replace('0', '')
        text += result

    # text_final = text.capitalize()

    output_adress = output_adress + "/output"

    with open(os.path.join(output_adress + r"/output_punctuation_history.txt"), 'a+', encoding="utf-8") as file:
        file.writelines([text + "\n"])

    with open(os.path.join(output_adress + r"/output_punctuation.txt"), 'w', encoding="utf-8") as file:
        file.writelines([text + "\n"])
    print(text)
    return text

