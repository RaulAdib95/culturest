from flask import Flask, render_template, request, send_file
import csv,json,xml.etree.ElementTree as ET,xml.dom.minidom

app = Flask(__name__)

expedientes_alumnos = {
    "216207667": ["Raul Adib Armenta Loredo", "Ingeniería en Sistemas de la Información", "a216207667@unison.mx"],
    "123456789": ["Juan Pérez", "Licenciatura en Administración", "juan.perez@ejemplo.com"],
    "987654321": ["María García", "Licenciatura en Contabilidad", "a987654321@unison.mx"],
    "135792468": ["Pedro López", "Ingeniería en Electrónica", "a135792468@unison.mx"],
    "246813579": ["Ana Martínez", "Licenciatura en Derecho", "a246813579@unison.mx"],
    "579246813": ["Javier Rodríguez", "Ingeniería en Sistemas de la Información", "a579246813@unison.mx"],
    "864201357": ["Laura Díaz", "Licenciatura en Administración", "a864201357@unison.mx"],
    "802467135": ["Carlos Sánchez", "Licenciatura en Contabilidad", "a802467135@unison.mx"],
    "703186425": ["Sofía Ramírez", "Ingeniería en Electrónica", "a703186425@unison.mx"],
    "319208476": ["Diego González", "Ingeniería en Sistemas de la Información", "a319208476@unison.mx"],
    "524687031": ["Elena Pérez", "Licenciatura en Administración", "a524687031@unison.mx"],
    "927510346": ["Miguel Martín", "Licenciatura en Contabilidad", "a927510346@unison.mx"],
    "438572019": ["Lucía Gómez", "Ingeniería en Electrónica", "a438572019@unison.mx"],
    "615934802": ["Alejandro Ruiz", "Licenciatura en Administración", "a615934802@unison.mx"],
    "972103485": ["Paula Hernández", "Ingeniería en Sistemas de la Información", "a972103485@unison.mx"],
    "105239874": ["David Torres", "Licenciatura en Contabilidad", "a105239874@unison.mx"],
    "471826039": ["Isabel Flores", "Licenciatura en Derecho", "a471826039@unison.mx"],
    "823091675": ["Jorge Moreno", "Ingeniería en Sistemas de la Información", "a823091675@unison.mx"],
    "123456789": ["Carmen Vázquez", "Licenciatura en Administración", "a123456789@unison.mx"],
    "987654321": ["Raúl Núñez", "Licenciatura en Contabilidad", "a987654321@unison.mx"],
    "246813579": ["Daniela Jiménez", "Ingeniería en Sistemas de la Información", "a246813579@unison.mx"],
    "579246813": ["Pablo Castro", "Licenciatura en Administración", "a579246813@unison.mx"],
    "246813769": ["Ana López", "Ingeniería en Sistemas de la Información", "a246813769@unison.mx"],
    "975318246": ["Juan Ramírez", "Licenciatura en Contabilidad", "a975318246@unison.mx"],
    "684975312": ["María Fernández", "Licenciatura en Administración", "a684975312@unison.mx"],
    "135792864": ["Pedro Martínez", "Ingeniería en Electrónica", "a135792864@unison.mx"],
    "568731924": ["Laura González", "Licenciatura en Derecho", "a568731924@unison.mx"],
    "179248365": ["Carlos Pérez", "Ingeniería en Sistemas de la Información", "a179248365@unison.mx"],
    "849635172": ["Sofía Díaz", "Licenciatura en Administración", "a849635172@unison.mx"],
    "324786915": ["Diego Sánchez", "Ingeniería en Electrónica", "a324786915@unison.mx"],
    "517298346": ["Paula Martínez", "Licenciatura en Contabilidad", "a517298346@unison.mx"],
    "654891273": ["Ana Torres", "Ingeniería en Sistemas de la Información", "a654891273@unison.mx"],
    "123987456": ["Miguel González", "Licenciatura en Administración", "a123987456@unison.mx"],
    "456123789": ["Laura Pérez", "Ingeniería en Electrónica", "a456123789@unison.mx"],
    "789456123": ["José Martínez", "Licenciatura en Contabilidad", "a789456123@unison.mx"]
}


def guardar_alumno_txt(alumno):
    with open('alumnos_registrados.txt', 'a') as f:
        f.write(f"Matrícula: {alumno['matricula']}\n")
        f.write(f"Nombre: {alumno['nombre']}\n")
        f.write(f"Carrera: {alumno['carrera']}\n")
        f.write(f"Correo: {alumno['correo']}\n")
        f.write("\n")

@app.route('/')
def index():
    return render_template('index.html', resultado="", alumno_existe=False)

@app.route('/buscar_expediente', methods=['POST'])
def buscar_expediente():
    matricula = request.form['matricula']
    if matricula in expedientes_alumnos:
        alumno = expedientes_alumnos[matricula]
        resultado = f"Expediente: {matricula}<br>Nombre: {alumno[0]}<br>Carrera: {alumno[1]}<br>Correo: {alumno[2]}"
        alumno_existe = True
        
        return render_template('index.html', resultado=resultado, alumno_existe=alumno_existe, matricula=matricula, nombre=alumno[0], carrera=alumno[1], correo=alumno[2])
    else:
        resultado = "Expediente no encontrado"
        alumno_existe = False
        return render_template('index.html', resultado=resultado, alumno_existe=alumno_existe)

def verificar_matricula(matricula):
    with open('alumnos_registrados.txt', 'r') as f:
        for line in f:
            if f"Matrícula: {matricula}" in line:
                return True
    return False

@app.route('/registrar_alumno', methods=['POST'])
def registrar_alumno():
    matricula = request.form['matricula']
    nombre = request.form['nombre']
    carrera = request.form['carrera']
    correo = request.form['correo']
    alumno = {'matricula': matricula, 'nombre': nombre, 'carrera': carrera, 'correo': correo}
   
    if verificar_matricula(matricula):
        mensaje = f"El alumno {nombre} ya está inscrito."
        notificacion = True
    else:
        guardar_alumno_txt(alumno)
        mensaje = "Alumno registrado correctamente."
        notificacion = True

    # Redirigir a una nueva página para mostrar el contenido del archivo txt
    print(mensaje)
    return render_template('index.html', mensaje=mensaje, notificacion=notificacion)

@app.route('/lista', methods=['POST'])
def mostrar_lista():
    try:
        with open('alumnos_registrados.txt', 'r') as f:
            contenido = f.readlines()
        if contenido:
            # Renderiza la plantilla con el contenido del archivo
            return render_template('alumnos_registrados.html', contenido=contenido)
        else:
            mensaje = "No hay alumnos registrados."
            return render_template('alumnos_registrados.html', mensaje=mensaje)
    except FileNotFoundError:
        mensaje = "No se encontró el archivo de alumnos registrados."
        return render_template('alumnos_registrados.html', mensaje=mensaje)
    
import csv

@app.route('/exportar_csv', methods=['GET'])
def exportar_csv():
    # Nombre del archivo CSV de salida
    nombre_archivo = 'alumnos_registrados.csv'

    # Lista de encabezados y filas de datos CSV
    encabezados = ['Matrícula', 'Nombre', 'Carrera', 'Correo']
    filas_csv = []

    # Leer el archivo de texto y convertir cada línea a una fila CSV
    with open('alumnos_registrados.txt', 'r') as f:
        datos_alumno = {}
        for line in f:
            line = line.strip()
            if line:
                clave, valor = line.split(': ')
                datos_alumno[clave] = valor
            else:
                # Agregar los datos del alumno actual a la lista de filas
                fila = [datos_alumno.get(encabezado, '') for encabezado in encabezados]
                filas_csv.append(fila)
                datos_alumno = {}

    # Escribir los datos en un archivo CSV
    with open(nombre_archivo, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(encabezados)  # Escribir encabezados
        writer.writerows(filas_csv)

    # Enviar el archivo CSV como respuesta para descargar
    return send_file(nombre_archivo, as_attachment=True)
    return send_file(nombre_archivo, as_attachment=True)

def generar_sql_insert(matricula, nombre, carrera, correo):
    return f"INSERT INTO alumnos (matricula, nombre, carrera, correo) VALUES ('{matricula}', '{nombre}', '{carrera}', '{correo}');\n"

@app.route('/exportar_sql', methods=['GET'])
def exportar_sql():
    # Nombre del archivo SQL de salida
    nombre_archivo = 'alumnos_registrados.sql'

    # Inicializar el contenido del archivo SQL
    contenido_sql = ""

    # Leer el archivo de texto y generar comandos INSERT SQL
    with open('alumnos_registrados.txt', 'r') as f:
        datos_alumno = {}
        for line in f:
            line = line.strip()
            if line:
                clave, valor = line.split(': ')
                if clave == "Matrícula":
                    matricula = valor
                elif clave == "Nombre":
                    nombre = valor
                elif clave == "Carrera":
                    carrera = valor
                elif clave == "Correo":
                    correo = valor
                    contenido_sql += generar_sql_insert(matricula, nombre, carrera, correo)

    # Escribir los datos en un archivo SQL
    with open(nombre_archivo, 'w', encoding='utf-8') as sql_file:
        sql_file.write(contenido_sql)

    # Enviar el archivo SQL como respuesta para descargar
    return send_file(nombre_archivo, as_attachment=True)

def generar_json_data(matricula, nombre, carrera, correo):
    return {
        'matricula': matricula,
        'nombre': nombre,
        'carrera': carrera,
        'correo': correo
    }

def exportar_xml():
    # Nombre del archivo XML de salida
    nombre_archivo = 'alumnos_registrados.xml'

    # Crea el elemento raíz del XML
    root = ET.Element("alumnos")

    # Leer el archivo de texto y convertir cada línea a un elemento XML
    with open('alumnos_registrados.txt', 'r') as f:
        alumno_elem = None
        for line in f:
            line = line.strip()
            if line:
                clave, valor = line.split(': ')
                if clave == 'Matrícula':
                    if alumno_elem is not None:
                        root.append(alumno_elem)  # Agrega el elemento de alumno anterior
                    alumno_elem = ET.Element("alumno")  # Crea un nuevo elemento de alumno
                # Crea elementos XML para cada atributo del alumno
                atributo_elem = ET.SubElement(alumno_elem, clave.lower())
                atributo_elem.text = valor

        if alumno_elem is not None:
            root.append(alumno_elem)  # Agrega el último elemento de alumno

    # Crea el árbol XML
    tree = ET.ElementTree(root)

    # Guarda el árbol XML en una cadena
    xml_str = ET.tostring(root, encoding='utf-8', method='xml').decode()

    # Formatea el XML para que sea legible
    xml_str_pretty = xml.dom.minidom.parseString(xml_str).toprettyxml(indent="    ")

    # Guarda el XML formateado en el archivo
    with open(nombre_archivo, "w", encoding='utf-8') as xml_file:
        xml_file.write(xml_str_pretty)

    # Enviar el archivo XML como respuesta para descargar
    return send_file(nombre_archivo, as_attachment=True)

@app.route('/exportar_xml', methods=['GET'])
def exportar_xml_route():
    return exportar_xml()

if __name__ == '__main__':
    app.run(debug=True)