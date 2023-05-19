import sys
from functools import partial

from PySide6.QtGui import QFont, Qt, QIcon
from PySide6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QGridLayout, QApplication, QWidget


class Calculadora(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculadora')
        self.setFixedSize(235, 235)

        # Creamos un Layout principal
        self.layout_principal = QVBoxLayout()

        # Creamos un contenedor para el Layout principal
        self.contenedor = QWidget()
        self.contenedor.setLayout(self.layout_principal)

        # Publicamos el contenedor
        self.setCentralWidget(self.contenedor)
        # Mandamos a llamar los métodos creadores
        self._crear_componentes_captura()
        self._crear_botones()

    # Creamos el método que creará la linea de texto
    def _crear_componentes_captura(self):
        # Creamos una caja de texto para el vertical layout
        self.entrada_texto = QLineEdit()
        # Configuramos el largo para que se ajuste a la pantalla
        self.entrada_texto.setMaximumWidth(235)
        # Configuramos el alto de la caja de texto
        self.entrada_texto.setMaximumHeight(30)
        # Configuramos la alineación (Hacia donde se va a mostrar el texto agregado)
        self.entrada_texto.setAlignment(Qt.AlignRight)
        # Hacemos la linea de texto de solo lectura
        self.entrada_texto.setReadOnly(True)
        # Configuramos la fuente
        fuente = QFont()
        fuente.setFamily('Comic Sans MS')
        fuente.setBold(True)
        self.entrada_texto.setFont(fuente)
        # Conectamos la señal de enter al slot que calculará el resultado resultado
        self.entrada_texto.returnPressed.connect(self._evento_resultado)
        self.layout_principal.addWidget(self.entrada_texto)

    # Creamos el método que creará los botones
    def _crear_botones(self):
        # Creamos un diccionario (por el momento vacío) para almacenar los componentes de tipo botón
        self.botones = {}
        # Creamos el Grid Layout
        self.grid = QGridLayout()
        # Creamos un diccionario con el texto y posición (en forma de tupla) de cada botón, para luego utilizarlos para
        # crear los botones de manera dinámica
        self.botones = {
            '7': (0, 0),
            '8': (0, 1),
            '9': (0, 2),
            '/': (0, 3),
            'Del': (0, 4),
            '4': (1, 0),
            '5': (1, 1),
            '6': (1, 2),
            '*': (1, 3),
            '1': (2, 0),
            '2': (2, 1),
            '3': (2, 2),
            '-': (2, 3),
            '0': (3, 0),
            '.': (3, 1),
            'C': (3, 2),
            '+': (3, 3),
            '=': (3, 4)
        }
        # Creamos los botones de manera dinámica
        for texto_boton, posicion in self.botones.items():
            self.botones[texto_boton] = QPushButton(texto_boton)
            self.botones[texto_boton].setFixedSize(40, 40)
            self.grid.addWidget(self.botones[texto_boton], posicion[0], posicion[1])
        self.layout_principal.addLayout(self.grid)
        # Mandamos a llamar al método que conectará la señal de los botones con slots
        self._conectar_botones()

    # Creamos un slot para conectar los botones
    def _conectar_botones(self):
        for texto_boton, boton in self.botones.items():
            if texto_boton not in {'C', '=', 'Del'}:
                boton.pressed.connect(partial(self._evento_click, texto_boton))
            # Conectamos las señales de los textos que faltan
            self.botones['C'].pressed.connect(self._evento_limpiar)
            self.botones['='].pressed.connect(self._evento_resultado)
            self.botones['Del'].pressed.connect(self._evento_borrar)

    def _evento_click(self, operacion):
        # Nos ayudamos de más métodos para construir la expresión final
        self.texto = self.recuperar_texto() + operacion
        # Usamos otro método para actualizar el texto de la caja de texto
        self.actualizar_texto(self.texto)

    def recuperar_texto(self):
        return self.entrada_texto.text()

    def actualizar_texto(self, texto):
        self.entrada_texto.setText(texto)

    def _evento_resultado(self):
        self.texto = self.evaluar_resultado(self.recuperar_texto())
        self.actualizar_texto(self.texto)

    def evaluar_resultado(self, expresion):
        try:
            resultado = f'{eval(expresion)}'
        except ZeroDivisionError:
            resultado = 'Error al dividir por 0'
        except Exception:
            resultado = 'Ocurrió un error'
        return resultado

    def _evento_limpiar(self):
        self.texto = ''
        self.actualizar_texto(self.texto)

    def _evento_borrar(self):
        largo = len(self.recuperar_texto())
        self.texto = self.texto[:largo-1]
        self.actualizar_texto(self.texto)


if __name__ == '__main__':
    # Creamos la aplicación
    app = QApplication()
    # Creamos el objeto de tipo calculadora
    calculadora = Calculadora()
    # Mostramos la calculadora
    calculadora.show()
    # Ejecutamos la app
    sys.exit(app.exec())
