from flask import Flask
import psycopg2



app =Flask(import_name=__name__)

@app.route('/getdata', methods=['GET', 'POST'])
def get_data():
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><input name="password" type="password"></p>
              <p><button type="submit">Sign In</button></p>
              </form>'''



if __name__=='__main__':
    app.run();