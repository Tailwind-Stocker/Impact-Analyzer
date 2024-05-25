from flask import Flask, request, render_template, jsonify
import datetime

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text-input']
    result_list = [elem.strip() for elem in text.split('\n') if elem.strip() != '' or '.' in elem]

    sentence_list = []
    for item in result_list:
        split_items = item.split('. ')
        for split_item in split_items:
            sentence_list.append(split_item.strip())

    with open("stop.txt") as f:
        data = f.read()
        stopwords = data.split()
        all_words = []
        for sentence in sentence_list:
            wor = sentence.split()
            all_words.append(wor)
        refined_list = []
        for words in all_words:
            for word in words:
                if word in stopwords:
                    pass
                else:
                    refined_list.append(word)

    with open("positive-words.txt") as f:
        data = f.read()
        positive_words = data.split()

    with open("negative-words.txt") as f:
        data = f.read()
        negative_words = data.split()

    positive_score = 0
    negative_score = 0

    for word in refined_list:
        if word.lower() in positive_words:
            positive_score += 1
        elif word.lower() in negative_words:
            negative_score += 1
        else:
            pass

    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)

    sentences = len(sentence_list)
    total_words = sum(len(words) for words in all_words)

    average_sentence_length = total_words / sentences
    average_reading_time = 200
    reading_time = (60 / average_reading_time) * total_words
    sec = reading_time
    convert = str(datetime.timedelta(seconds=sec))
    readingtime = convert[2:7]

    result = {
        'positive_score': positive_score,
        'negative_score': negative_score,
        'polarity_score': round(polarity_score,2),
        'average_sentence_length': round(average_sentence_length,2),
        'reading_time': readingtime
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
