from flask import Flask, render_template

app = Flask(__name__)

@app.route("/hello")
def hello():
    html = """
    Hello FLASK This is flask webpage
    """
    return html


@app.route("/world")
def world():
    html="""<h1>안녕 플라스크!!!!!</h1>
    <p style = 'color: blue'>첫 번째 플라스크 웹 페이지</p>
"""
    return html

@app.route("/myfood")
def food():
    return render_template("myfood.html")

@app.route("/mydata")
def mydata():
    mydict = {"name":"Lee","age":24,"height":198,"weight":89}
    return mydict

if __name__ == "__main__":
    app.run(port=9091, debug=True)


