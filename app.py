import os, datetime, random
from dotenv import load_dotenv
from flask import Flask, render_template, request, Markup
import matplotlib as mpl
from matplotlib import pyplot as plt
from wordcloud import WordCloud

load_dotenv() # .envを読み込む
SK = os.getenv("SECRET_KEY") # 環境変数を取得
app = Flask(__name__)
app.secret_key = SK

mpl.rcParams['figure.dpi']= 300  # dpi

now = datetime.datetime.now()
filename = now.strftime('%Y%m%d%H%M%S')+str(random.randint(10000, 100000))

def createWordcloud(bgc, cloud_data, cmap, font, height, width):
    cloud = WordCloud(
        background_color=bgc,
        colormap=cmap,
        font_path='./static/font/'+font,
        height=height*10,
        include_numbers=True,
        max_words=100,
        prefer_horizontal=0.7,
        relative_scaling=1,
        scale=1,
        width=width*10
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
        url='https://words-that-describe-me.herokuapp.com',
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
        url = 'https://words-that-describe-me.herokuapp.com/result',
        filename=filename
        )

@app.route("/sitemap.xml")
def sitemap():
    return app.send_static_file("sitemap.xml")

if __name__ == "__main__":
    app.run()
