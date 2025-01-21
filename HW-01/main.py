from flask import Flask, render_template

app = Flask(__name__)  #Создаем экземпляр класса flask / Имя файла который ответственен за запуск скрипта


@app.route('/')  #Функция-декоратор которая отвечает за маршрут запуска сервера
def main():  #Функция-обработчик
    return '<h3> Hello Flask </h3>'


@app.route('/user/<name>')
def greeting(name):
    return render_template('user_name.html', name=name)


if __name__ == '__main__':  #__name__ В случае если файл является файлом запуска
    app.run(debug=True, host='0.0.0.0')  #Баги отображаются в реальном времени
