from data.modelo.hospital import Hospital

class DaoHospitales:
    # Obtiene todos los hospitales de la base de datos y los devuelve como una lista de objetos Hospital
    def get_all(self, db) -> list[Hospital]:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM hospitales")
        hospitales_en_db = cursor.fetchall()
        hospitales: list[Hospital] = []
        for hospital in hospitales_en_db:
            nueva_hospital = Hospital(hospital[0], hospital[1], hospital[2])
            hospitales.append(nueva_hospital)
        cursor.close()
        return hospitales

    # Inserta un nuevo hospital en la base de datos con nombre y número de personas
    def insert(self, db, nombre: str, numero_pacientes: int):
        cursor = db.cursor()
        sql = ("INSERT INTO hospitales (nombre, numero_pacientes) VALUES (%s, %s)")
        data = (nombre, numero_pacientes)
        cursor.execute(sql, data)
        db.commit()
        cursor.close()

    # Borra un hospital de la base de datos por su id
    def delete(self, db, id: int):
        cursor = db.cursor()
        sql = "DELETE FROM hospitales WHERE id = %s"
        data = (id,)
        cursor.execute(sql, data)
        db.commit()
        cursor.close()

    # Actualiza el nombre y número de personas de un hospital por su id
    def update(self, db, id: int, nombre: str, numero_pacientes: int):
        cursor = db.cursor()
        sql = """
            UPDATE hospitales 
            SET nombre = %s, numero_pacientes = %s
            WHERE id = %s
        """
        data = (nombre, numero_pacientes, id)
        cursor.execute(sql, data)
        db.commit()
        cursor.close()

    # Obtiene un hospital por su id y lo devuelve como objeto Hospital (o None si no existe)
    def get_by_id(self, db, id: int) -> Hospital:
        cursor = db.cursor()
        sql = "SELECT * FROM hospitales WHERE id = %s"
        cursor.execute(sql, (id,))
        hospital_en_db = cursor.fetchone()

        if hospital_en_db:
            hospital = Hospital(hospital_en_db[0], hospital_en_db[1], hospital_en_db[2],)
        else:
            hospital = None

        cursor.close()
        return hospital

    # Obtiene todos los hospitales con más pacientes que el número dado
    def get_by_numero_pacientes(self, db, numero_pacientes: int) -> list[Hospital]:
        cursor = db.cursor()
        sql = "SELECT * FROM hospitales WHERE numero_pacientes > %s"
        cursor.execute(sql, (numero_pacientes,))
        hospitales_en_db = cursor.fetchall()
        hospitales: list[Hospital] = []
        for hospital in hospitales_en_db:
            hospitales.append(Hospital(hospital[0], hospital[1], hospital[2]))
        cursor.close()
        return hospitales

