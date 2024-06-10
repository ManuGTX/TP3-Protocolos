from flask import Flask, render_template, request, abort, jsonify, redirect
import time
import random
import sqlite3
from datetime import datetime
from funciones import geo_latlon

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('tabla_sensores_para_editar.html')

@app.route('/api/test')
def test():
    return "Prueba de ruta API..."

@app.route('/api/datos')
def datos():
    conn = sqlite3.connect('sensores.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM lectura_sensores')
    records = cursor.fetchall()
    conn.close()
    data = []
    for record in records:
        data.append(
        {
        'id': record[0],
        'co2': record[1],
        'temp': record[2],
        'hum': record[3],
        'fecha': record[4],
        'lugar': record[5],
        'altura': record[6],
        'presion': record[7],
        'presion_nm': record[8],
        'temp_ext': record[9]
        })
    
    return jsonify({
        'data': data,
        'total': len(data),
    })

@app.route('/api/primer-registro')
def primerRegistro():
    try:
        conn = sqlite3.connect('sensores.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lectura_sensores")
        primero = cursor.fetchone()
        conn.close()
        if not primero:
            return jsonify({'mensaje': 'No se encontraron datos'}), 404
        return jsonify(primero)
    except Exception as e:
        return jsonify({'error': 'Error al buscar datos', 'detalle': str(e)}), 500
       
@app.route('/api/anadir', methods=["POST"])
def añadir():
    try:
        CO2 = request.form.get('CO2')
        Temp = request.form.get('Temp')
        Hum = request.form.get('Hum')
        Lugar = request.form.get('Lugar')
        Altura = request.form.get('Altura')
        Presion = request.form.get('Presion')
        Presion_nm = request.form.get('Presion_nm')
        Temp_ext = request.form.get('Temp_ext')
        
        if CO2 is None or Temp is None or Hum is None or Lugar is None or Altura is None or Presion is None or Presion_nm is None or Temp_ext is None:
            abort(400)
        
        current_datetime = datetime.now().strftime("%d-%B-%Y (%H:%M:%S)")
        
        conn = sqlite3.connect('sensores.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO lectura_sensores (co2, temp, hum, fecha, lugar, altura, presion, presion_nm, temp_ext) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (CO2, Temp, Hum, current_datetime, Lugar, Altura, Presion, Presion_nm, Temp_ext))
        conn.commit()
        conn.close()
        
        
        return redirect("/")
    except Exception as e:
        return jsonify({'error': 'Error al añadir datos', 'detalle': str(e)}), 500
        
@app.route('/api/eliminar', methods=['DELETE'])
def eliminar():
    try:
        data = request.get_json()
        if 'id' not in data:
            abort(400)
        
        conn = sqlite3.connect('sensores.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lectura_sensores WHERE id = ?", (data['id']))
        record = cursor.fetchone()
        conn.close()
        
        if not record:
            abort(404)
        
        conn = sqlite3.connect('sensores.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM lectura_sensores WHERE id = ?", (data['id']))
        conn.commit()
        conn.close()
        return '', 204
    except Exception as e:
        return jsonify({'error': 'Error al buscar datos', 'detalle': str(e)}), 500

@app.route('/api/data', methods=['PUT'])
def update():
    try:
        data = request.get_json()
        if 'id' not in data:
            abort(400)
            
        conn = sqlite3.connect('sensores.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lectura_sensores WHERE id = ?", (data['id']))
        record = cursor.fetchone()
        conn.close()
        
        if not record:
            abort(404)
            
        if 'lugar' in data:
            new_lugar = data['lugar']
            conn = sqlite3.connect('sensores.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE lectura_sensores SET lugar = ? WHERE id = ?", (new_lugar, data['id']))
            conn.commit()
            conn.close()
        elif 'co2' in data:
            new_co2 = data['co2']
            conn = sqlite3.connect('sensores.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE lectura_sensores SET co2 = ? WHERE id = ?", (new_co2, data['id']))
            conn.commit()
            conn.close()
        elif 'temp' in data:
            new_temp = data['temp']
            conn = sqlite3.connect('sensores.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE lectura_sensores SET temp = ? WHERE id = ?", (new_temp, data['id']))
            conn.commit()
            conn.close()
        elif 'hum' in data:
            new_hum = data['hum']
            conn = sqlite3.connect('sensores.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE lectura_sensores SET hum = ? WHERE id = ?", (new_hum, data['id']))
            conn.commit()
            conn.close()
        elif 'altura' in data:
            altura = data['altura']
            conn = sqlite3.connect('sensores.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE lectura_sensores SET altura = ? WHERE id = ?", (altura, data['id']))
            conn.commit()
            conn.close()
        elif 'presion' in data:
            presion = data['presion']
            conn = sqlite3.connect('sensores.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE lectura_sensores SET presion = ? WHERE id = ?", (presion, data['id']))
            conn.commit()
            conn.close()  
        elif 'presion_nm' in data:
            presion_nm = data['presion_nm']
            conn = sqlite3.connect('sensores.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE lectura_sensores SET presion_nm = ? WHERE id = ?", (presion_nm, data['id']))
            conn.commit() 
            conn.close() 
        elif 'temp_ext' in data:
            temp_ext = data['temp_ext']
            conn = sqlite3.connect('sensores.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE lectura_sensores SET temp_ext = ? WHERE id = ?", (temp_ext, data['id']))
            conn.commit()
            conn.close()  
            
        return '', 204
    except Exception as e:
        return jsonify({'error': 'Error al actualizar datos', 'detalle': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
