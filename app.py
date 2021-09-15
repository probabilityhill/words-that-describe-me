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

def createWordcloud(bgc, cloud_data, cmap, font, height, width):
    cloud = WordCloud(
        background_color=bgc,
        colormap=cmap,
        font_path='./static/font/'+font,
        height=height,
        prefer_horizontal=0.7,
        scale=50,
        width=width
        ).fit_words(cloud_data)

    plt.axis('off')
    plt.imshow(cloud)
    plt.savefig(
        './static/img/wordcloud_'+filename+'.png',
        bbox_inches='tight',
        dpi=300,
        pad_inches=0
        )



@app.route("/")
def top():
    tr = Markup('<tr><th>要素</th><th>大きさ</th></tr>')
    for i in range(100):
        tr += Markup('<tr><td><input type="text" name="word" placeholder="'+str(i+1)+'"></td><td><input type="text" inputmode="decimal" name="freq"></td></tr>')
    return render_template(
        'index.html',
        description='「私を構成する100の要素」作成ツールです。',
        title='私を構成する100の要素｜作成ツール',
        url='https://beautyofthebrain.pythonanywhere.com/',
        tr = tr
        )


# postのときの処理
@app.route("/result", methods=['POST'])
def post():
    aspect_ratio = request.form.get('aspect_ratio').split(':')
    width = int(aspect_ratio[0])
    height = int(aspect_ratio[1])

    bgc = request.form.get('bgc')
    cmap = request.form.get('cmap')
    font = request.form.get('font')

    wordlist = request.form.getlist('word')
    wordlist = [a for a in wordlist if a != '']
    freqlist = request.form.getlist('freq')
    freqlist = [a for a in freqlist if a != '']
    freqlist = list(map(float, freqlist)) # str --> float
    cloud_data = dict(zip(wordlist,freqlist))

    createWordcloud(bgc, cloud_data, cmap, font, height, width)

    return render_template(
        'result.html',
        description = '',
        title = '私を構成する100の要素｜出力画像',
        url = 'https://beautyofthebrain.pythonanywhere.com/result',
        filename=filename
        )

if __name__ == "__main__":
    app.run()
