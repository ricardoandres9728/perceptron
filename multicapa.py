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
    x1 = int(form["x1"])
    x2 = int(form["x2"])
    pesos = session["pesos"]

    net = (x1 * pesos[1] + x2 * pesos[2] + pesos[0])
    resultado = funcion_activacion(net)
    return jsonify(resultado)


@app.route('/', methods=["GET", "POST"])
def hello_world():
    errors_1 = [1]
    errors_2 = [1]
    escala_1 = [1]
    escala_2 = [1]
    xs_1 = [1]
    ys_1 = [1]
    xs_2 = [1]
    ys_2 = [1]
    delta_pesos_1 = [
        [],
        [],
        []
    ]
    delta_pesos_2 = [
        [],
        [],
        []
    ]
    escala_delta_1 = [1]
    escala_delta_2 = [1]
    if request.method == "POST":
        form = request.form
        flag = True
        tasa_de_aprendizaje_n1 = float(form["en1"])
        tasa_de_aprendizaje_n2 = float(form["en2"])
        delta_pesos_1 = [
            [],
            [],
            []
        ]
        delta_pesos_2 = [
            [],
            [],
            []
        ]
        pesos_1 = [random.random() for i in range(0, 3)]
        pesos_2 = [random.random() for i in range(0, 3)]
        if form["un1"]:
            if form["un1"] == '0':
                pesos_1[0] = 0
                flag = False
            else:
                pesos_1[0] = float(form["un1"])
                flag = True
        if form["un2"]:
            if form["un2"] == '0':
                pesos_2[0] = 0
                flag = False
            else:
                pesos_2[0] = float(form["un2"])
                flag = True

        training_data_neurona_1 = [(array([1, 1, 1]), 0),
                                   (array([1, 1, 0]), 1),
                                   (array([1, 0, 1]), 0),  # (A*-B)
                                   (array([1, 0, 0]), 0), ]

        training_data_neurona_2 = [(array([1, 1, 1]), 0),
                                   (array([1, 1, 0]), 0),
                                   (array([1, 0, 1]), 1),  # (-A*B)
                                   (array([1, 0, 0]), 0), ]

        while True:
            contador_de_errores = 0
            for vector_de_entrada, salida_deseada in training_data_neurona_1:
                resultado = funcion_activacion(producto_punto(vector_de_entrada, pesos_1))
                error = salida_deseada - resultado
                if error == 0:
                    errors_1.append(0)
                else:
                    errors_1.append(1)
                if salida_deseada != resultado:
                    contador_de_errores += 1
                    for indice, valor in enumerate(vector_de_entrada):
                        delta_pesos_1[indice].append(pesos_1[indice])
                        pesos_1[indice] += tasa_de_aprendizaje_n1 * error * valor
            if contador_de_errores == 0:
                break
        session["pesos_1"] = pesos_1
        while True:
            contador_de_errores = 0
            for vector_de_entrada, salida_deseada in training_data_neurona_2:
                resultado = funcion_activacion(producto_punto(vector_de_entrada, pesos_2))
                error = salida_deseada - resultado
                if error == 0:
                    errors_2.append(0)
                else:
                    errors_2.append(1)
                if salida_deseada != resultado:
                    contador_de_errores += 1
                    for indice, valor in enumerate(vector_de_entrada):
                        delta_pesos_2[indice].append(pesos_2[indice])
                        pesos_2[indice] += tasa_de_aprendizaje_n2 * error * valor
            if contador_de_errores == 0:
                break
        session["pesos_2"] = pesos_2
        if flag:
            m_1 = (-1 * pesos_1[1]) / pesos_1[2]
            m_2 = (-1 * pesos_2[1]) / pesos_2[2]
            b_1 = -pesos_1[0] / pesos_1[2]
            b_2 = -pesos_2[0] / pesos_2[2]
            escala_1 = [i for i in range(0, len(errors_1))]
            escala_2 = [i for i in range(0, len(errors_2))]
            escala_delta_1 = [i for i in range(0, len(delta_pesos_1[0]))]
            escala_delta_2 = [i for i in range(0, len(delta_pesos_2[0]))]
            print(escala_delta_1)
            xs_1 = [round(i * 0.1, 1) for i in range(0, 12)]
            xs_1 = [round(i * 0.1, 1) for i in range(0, 12)]
            ys_1 = [lineal(i, m_1, b_1) for i in xs_1]
            ys_2 = [lineal(i, m_2, b_2) for i in xs_2]
        else:
            m_1 = (-1 * pesos_1[1]) / pesos_1[2]
            m_2 = (-1 * pesos_2[1]) / pesos_2[2]
            b_1 = 0
            b_2 = 0
            pesos_1[0] = 0
            pesos_2[0] = 0
            escala_1 = [i for i in range(0, len(errors_1))]
            escala_2 = [i for i in range(0, len(errors_2))]
            escala_delta_1 = [i for i in range(0, len(delta_pesos_1[0]))]
            escala_delta_2 = [i for i in range(0, len(delta_pesos_2[0]))]
            xs_1 = [round(i * 0.1, 1) for i in range(0, 12)]
            xs_1 = [round(i * 0.1, 1) for i in range(0, 12)]
            ys_1 = [lineal(i, m_1, b_1) for i in xs_1]
            ys_2 = [lineal(i, m_2, b_2) for i in xs_2]
    return render_template('multicapa.html', errors_1=errors_1, errors_2=errors_2, escala_1=escala_1, escala_2=escala_2,
                           x_1=xs_1, x_2=xs_2, y_1=ys_1, y_2=ys_2, delta_pesos_1=delta_pesos_1, delta_pesos_2=delta_pesos_2,
                           escala_delta_1=escala_delta_1, escala_delta_2=escala_delta_2,)


if __name__ == '__main__':
    app.run(debug=True)
