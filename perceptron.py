from flask import Flask, jsonify, render_template, session, request
import random
from numpy import array


app = Flask(__name__)
app.secret_key = 'Mysecretkey'


def producto_punto(valores, pesos):
    return sum(valor * peso for valor, peso in zip(valores, pesos))


def lineal(x, m, b):
    return m * x + b


def funcion_activacion(net):
    if net > 0:
        return 1
    else:
        return 0


@app.route('/calcular', methods=["POST"])
def calcular():
    form = request.form
    print()
    x1 = int(form["x1"])
    x2 = int(form["x2"])
    pesos = session["pesos"]
    net = (x1 * pesos[1] + x2 * pesos[2] + pesos[0])
    resultado = funcion_activacion(net)
    return jsonify(resultado)


@app.route('/', methods=["GET", "POST"])
def hello_world():
    errors = [1]
    escala = [1]
    xs = [1]
    ys = [1]
    delta_pesos = [
        [],
        [],
        []
    ]
    escala_delta = [1]
    if request.method == "POST":
        form = request.form
        flag = True
        compuerta = form["compuerta"]
        tasa_de_aprendizaje = float(form["aprendizaje"])
        delta_pesos = [
            [],
            [],
            []
        ]

        pesos = [random.random() for i in range(0, 3)]
        print ('antes del if')
        if form["umbral"]:
            if form["umbral"] == '0':
                pesos[0] = 0
                flag = False
                print ('umbral 0')
            else:
                pesos[0] = float(form["umbral"])
                flag = True
                print('umbral !0')

        training_data = []
        if compuerta == "and":
            training_data_and = [(array([1, 1, 1]), 1),
                                 (array([1, 1, 0]), 0),
                                 (array([1, 0, 1]), 0),
                                 (array([1, 0, 0]), 0), ]
            training_data = training_data_and

        if compuerta == "or":
            training_data_or = [(array([1, 1, 1]), 1),
                                (array([1, 1, 0]), 1),
                                (array([1, 0, 1]), 1),
                                (array([1, 0, 0]), 0), ]
            training_data = training_data_or
        if compuerta == "nor":
            training_data_or = [(array([1, 1, 1]), 0),
                                (array([1, 1, 0]), 0),
                                (array([1, 0, 1]), 0),
                                (array([1, 0, 0]), 1), ]
            training_data = training_data_or
        if compuerta == "nand":
            training_data_or = [(array([1, 1, 1]), 0),
                                (array([1, 1, 0]), 1),
                                (array([1, 0, 1]), 1),
                                (array([1, 0, 0]), 1), ]
            training_data = training_data_or
        if compuerta == "xor":
            training_data_or = [(array([1, 1, 1]), 0),
                                (array([1, 1, 0]), 1),
                                (array([1, 0, 1]), 1),
                                (array([1, 0, 0]), 0), ]
            training_data = training_data_or
        while True:
            contador_de_errores = 0
            for vector_de_entrada, salida_deseada in training_data:
                resultado = funcion_activacion(producto_punto(vector_de_entrada, pesos))
                error = salida_deseada - resultado
                if error == 0:
                    errors.append(0)
                else:
                    errors.append(1)
                if salida_deseada != resultado:
                    contador_de_errores += 1
                    for indice, valor in enumerate(vector_de_entrada):
                        delta_pesos[indice].append(pesos[indice])
                        pesos[indice] += tasa_de_aprendizaje * error * valor
            if contador_de_errores == 0:
                session["pesos"] = pesos
                break
        if flag:
            m = (-1 * pesos[1]) / pesos[2]
            b = -pesos[0] / pesos[2]
            escala = [i for i in range(0, len(errors))]
            escala_delta = [i for i in range(0, len(delta_pesos[0]))]
            xs = [round(i * 0.1, 1) for i in range(0, 12)]
            ys = [lineal(i, m, b) for i in xs]
        else:
            m = (-1 * pesos[1]) / pesos[2]
            b = 0
            pesos[0] = 0
            escala = [i for i in range(0, len(errors))]
            escala_delta = [i for i in range(0, len(delta_pesos[0]))]
            xs = [round(i * 0.1, 1) for i in range(0, 12)]
            ys = [lineal(i, m, b) for i in xs]
    return render_template('home.html', errors=errors, escala=escala, x=xs, y=ys, delta_pesos=delta_pesos,
                           escala_delta=escala_delta)


if __name__ == '__main__':
    app.run(debug=True)
