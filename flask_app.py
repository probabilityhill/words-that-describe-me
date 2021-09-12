import matplotlib as mpl
mpl.rcParams['figure.dpi']= 300  # dpi

from matplotlib import pyplot as plt
from wordcloud import WordCloud
import datetime
from flask import Flask, render_template, request, Markup

app = Flask(__name__)
app.secret_key = 'ahahahaaaa'

now = datetime.datetime.now()
filename = now.strftime('%Y%m%d%H%M%S')

def createWordcloud(cloud_data):
    """
    cloud_data = {
        '音楽':0.9,
        '読書':0.1,
        'サイケデリック':0.8,
        'シューゲイザー':1.5,
        'アンビエント':0.2,
        'Tame Impara':0.5,
        '焼肉':0.4,
        'Metafive':0.3,
        'The Flipper\'s guitar':0.2,
        '游ゴシック':0.8,
        'P-MODEL':0.08
        }
    """

    cloud = WordCloud(
        background_color='black',
        colormap='Set3',
        font_path='/home/beautyOfTheBrain/mysite/static/font/YuGothB.ttc',
        height=90,
        prefer_horizontal=0.7,
        scale=50,
        width=160
        ).fit_words(cloud_data)

    plt.axis('off')
    plt.imshow(cloud)
    plt.savefig(
        '/home/beautyOfTheBrain/mysite/static/img/wordcloud_'+filename+'.png',
        bbox_inches='tight',
        dpi=300,
        pad_inches=0
        )



@app.route("/")
def top():
    tr = Markup('<tr><th>要素</th><th>頻度</th></tr>')
    for i in range(100):
        tr += Markup('<tr><td><input type="text" size="30" name="word"></td><td><input type="text" size="5" name="freq"></td></tr>')
    return render_template(
        'index.html',
        description='「私を構成する100の要素」作成ツールです。',
        title='「私を構成する100の要素」作成ツール',
        url='https://beautyofthebrain.pythonanywhere.com/',
        tr = tr
        )


# postのときの処理
@app.route("/result", methods=['POST'])
def post():
    cloud_data = request.form.get('cloud_data')
    # radio = request.form.get('radio')
    wordlist = request.form.getlist('word')
    wordlist = [a for a in wordlist if a != '']
    freqlist = request.form.getlist('freq')
    freqlist = [a for a in freqlist if a != '']
    freqlist = list(map(int, freqlist)) # str --> int
    cloud_data = dict(zip(wordlist,freqlist))
    createWordcloud(cloud_data)
    return render_template(
        'result.html',
        description = '',
        title = 'GENERATED |「私を構成する100の要素」作成ツール',
        url = 'https://beautyofthebrain.pythonanywhere.com/result',
        filename=filename
        )
