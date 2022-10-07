from flask import Flask, render_template, request
import random
from flask_wtf import Form
from wtforms import TelField, SelectField, IntegerField
import json


def load_json(file_name):
    with open(file_name, 'r') as json_card_data:
        return json.load(json_card_data)


subjects = load_json('static/subjects.json')
card_data = load_json('static/card_data.json')
card_relationships = load_json('static/card_relationships.json')


def search(search_terms):
    most_common_words = ['i', 'a', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '10',
                         'be', 'to', 'of', 'it', 'on', 'he', 'as', 'by', 'we', 'or', 'my', 'so', 'if',
                         'and', 'the', 'for', 'not', 'you', 'but', 'his', 'her', 'she',
                         'that', 'they', 'then', 'than', 'have', 'this', 'with',
                         'there', 'their', 'which', 'would', 'about']
    terms = [t.lower() for t in search_terms.split() if t.lower() not in most_common_words]
    if not terms:
        return None
    possible_results1 = []
    for c in card_data:
        if terms[0] in card_data[c][0].lower():
            possible_results1.append(c)
    for t in terms:
        possible_results2 = search_iter(t, possible_results1)
        possible_results1 = list(set(possible_results1) & set(possible_results2))
    data = []
    possible_results1 = [int(p) for p in possible_results1]
    possible_results1.sort()
    for c in possible_results1:
        data.append([str(c), card_data[str(c)][0], '/static/images/{}.png'.format(str(c).zfill(5))])
    return data


def search_iter(term, list_items):
    return [l for l in list_items if term in card_data[l][0].lower()]


def get_card_by_subject(subject):
    data = []
    for c in card_relationships[subject]:
        data.append([c, card_data[str(c)][0], '/static/images/{}.png'.format(str(c).zfill(5))])
    return data


app = Flask(__name__)


@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    form = InputForm()
    errtext = ''
    rand = random.randrange(1, 10001)

    if request.method == 'POST':
        data = request.form
        if data.get('subject') != 'Select Subject':
            image_list = get_card_by_subject(data.get('subject'))
            return render_template('index.html', image_list=image_list, form=form)
        if data.get('search'):
            image_list = search(data.get('search'))
            if image_list:
                if data.get('search').isnumeric():
                    image_list.insert(0, [data.get('search'),
                                          card_data[data.get('search')][0],
                                          'static/images/'+data.get('search').zfill(5)+'.png'])
                return render_template('index.html', image_list=image_list, form=form)
            elif data.get('search').isnumeric() and int(data.get('search')) <= 10001:
                rand = data.get('search')
            else:
                errtext = 'No search results found, here\'s a random potshot'
    img = 'static/images/'+str(rand).zfill(5)+'.png'
    text = card_data[str(rand)][0]
    image_list = [[str(rand), text, img]]
    return render_template('index.html', image_list=image_list, errtext=errtext, form=form)


class InputForm(Form):
    subject = SelectField(label='Subjects',
                          choices=subjects,
                          render_kw={'placeholder': 'Subject Search', 'class': 'js-example-basic-single'})

    search = IntegerField(
        label='Search by ID number',
        render_kw={'placeholder': 'ID Search', 'class': 'form-control'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)