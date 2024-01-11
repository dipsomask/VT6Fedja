from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='C:/Users/alexe/Documents/PyCharm Community Edition 2023.1.1/PROJECTS/VT6Fedja')


@app.route('/', methods=['GET', 'POST'])
def index():
    error = " "
    if request.method == 'POST':
        product = request.form['product']
        new_value = request.form['quantity']
        with open("data/storage.txt", "r") as file:
            lines = file.readlines()

        updated_lines = []
        for line in lines:
            line_product, line_quantity = line.split('-')
            if line_product == product:
                if int(line_quantity) - int(new_value) >= 0:
                    line_quantity = int(line_quantity) - int(new_value)
                    line = f"{line_product}- {line_quantity}\n"
                else:
                    error = "You can not buy more products than we have"
            updated_lines.append(line)

        with open("data/storage.txt", "w") as file:
            file.writelines(updated_lines)

        with open("data/storage.txt", "r") as file:
            data = file.readlines()
        prod = []
        # Обходим каждую строку
        for line in data:
            # Разделяем строку по знаку "-" и берем вторую часть (после знака "-")
            value = line.split('-')[1].strip()
            # Преобразуем значение в целое число и добавляем в массив
            prod.append(int(value))
        return render_template('choose.html', prod1=str(prod[0]), prod2=str(prod[1]), prod3=str(prod[2]),
                               prod4=str(prod[3]), error=error)

    else:
        with open("data/storage.txt", "r") as file:
            data = file.readlines()
        prod = []
        # Обходим каждую строку
        for line in data:
            # Разделяем строку по знаку "-" и берем вторую часть (после знака "-")
            value = line.split('-')[1].strip()
            # Преобразуем значение в целое число и добавляем в массив
            prod.append(int(value))
        return render_template('choose.html', prod1=str(prod[0]), prod2=str(prod[1]), prod3=str(prod[2]),
                               prod4=str(prod[3]), error=error)

# Функция, которая получает с файла колличество каждого продукта, составляет из них
# массив и отправляет в формате json в функцию на javascript - updateValues() на странницы html
@app.route('/get_values')
def get_values():
    #Открываем файл на чтение и читаем построчно в массив
    with open('data/storage.txt', 'r') as file:
        data = file.readlines()
    prod = []
    #получаем значения количества, разделяя строки по знакам "-", а потом записываем в массив
    for line in data:
        value = line.split('-')[1].strip()
        prod.append(int(value))
    #Возвращаем заполненный массив
    return jsonify(prod)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')

