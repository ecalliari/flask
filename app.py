from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
import pandas as pd
import psycopg2


app = Flask(__name__)
app.config['SECRET_KEY'] = 'some_secret_key'

class ContactForm(FlaskForm):
    name = StringField('Nome:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    message = TextAreaField('Messagem:', validators=[DataRequired()])
    submit = SubmitField('Send')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        # do something with the form data here
        flash('Your message has been sent. Thank you!')
        return render_template('contact.html', form=form)
    return render_template('contact.html', form=form)

@app.route('/filter', methods=['POST'])
def projects():
  nombre = request.form['nombre']
  apellido = request.form['apellido']
  df = pd.read_excel("positivacao-de-clientes.xlsx", sheet_name="Worksheet")
  df = pd.DataFrame(df)
  df = df[['Cliente','Data do último pedido','Vendido Acumulado']]
  df = df[df['Cliente'].str.contains(nombre, na=False)]
  html = df.to_html(columns=['Cliente','Data do último pedido','Vendido Acumulado'], index=False, decimal=',', classes='my-table')
  
  #return nombre + html
  return render_template("tabResult.html", table=html)

@app.route("/cotacoes", methods=['GET', 'POST'])
def selectCity():
      fruits = ['ipca', 'igpm', 'tjlp', 'us/real']
      if request.method == 'POST':
        
        return f'Você escolheu {varMacro}'
    
      varMacro = request.args.get('comp_select')
      varMacro_ = request.args.get('comp_select')
      if varMacro == 'ipca':
          varMacro = 433
      elif varMacro == 'igpm':
          varMacro = 189
      elif varMacro == 'tjlp':
          varMacro = 256    
      else:
          varMacro = 1
      
      if varMacro_ == None:
          varMacro_ = 'ipca'
          varMacro = 888
      class Conection():
        def __init__(self):
            self.con = psycopg2.connect(
                host='containers-us-west-204.railway.app', port=6444, database='railway', user='postgres', password='maBMwPOIdscQ32wJppPQ')
            self.con.autocommit = True
            
        def getPotencial(self) -> list:
            #arquivo = open("D:\\Trabalho\\Ambiente DEV\\Conferencias Agco\\sql\\potencial.txt","r")
            #sql = arquivo.read()
            sql = f"""select data, value from fonte_macro where code = {varMacro} """
            cur = self.con.cursor()
            cur.execute(sql)
            recset = cur.fetchall()
            result = list()
            for rec in recset:
                result.append(rec)

            return result
      a = Conection()
      tabmacro = a.getPotencial()
      tabmacro = pd.DataFrame(tabmacro)
      tabmacro.rename(columns={0: 'Perido',1: 'Cotação'})
      htmlMacro = tabmacro.to_html(index=True, decimal=',')
      
          
      return render_template("cotações.html", fruits=fruits, table=htmlMacro)
    
@app.route("/main")
def main():
    return render_template("main.html")

@app.route("/")
def principal():
    return render_template("main.html")

@app.route("/cotacoes")
def cotacoes():
    return render_template("cotações.html")

@app.route("/home")
def home():
    return render_template("main.html")

@app.route("/repre")
def repre():
    return render_template("representadas.html")
    
@app.route("/tabela")
def salvador():
    return render_template("tabela.html")

@app.route("/geo")
def geo():
    return render_template("geo.html")
    
if __name__ == "__main__":
    app.run(debug=True, host= '0.0.0.0')