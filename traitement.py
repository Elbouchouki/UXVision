# import io
import json
import sqlite3
import numpy as np


###### ===> class Face ######
class Face:
    def __init__(self, person_id, image, face_encode):
        self.person_id = person_id
        self.image = image
        self.face_encode = face_encode

    def get_face_id(self):
        return self.face_id

    def get_person_id(self):
        return self.person_id

    def get_image(self):
        return self.image

    def get_face_encode(self):
        return self.face_encode

    def set_face_id(self, face_id):
        self.face_id = face_id

    # def set_person_id(self, person_id):
    #     self.person_id = person_id

    # def set_image(self, image):
    #     self.image = image

    # def set_face_encode(self, face_encode):
    #     self.face_encode = face_encode


###### ===> class Person ######


class Person:

    def __init__(self, nom, prenom):
        self.nom = nom
        self.prenom = prenom

    def getNom(self):
        return self.nom

    def getPrenom(self):
        return self.prenom

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def setNom(self, nom):
        self.nom = nom

    def setPrenom(self, prenom):
        self.prenom = prenom

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return str(self.nom).lower() == str(other.nom).lower() and str(self.prenom).lower() == str(other.prenom).lower() or str(self.nom).lower() == str(other.prenom).lower() and str(self.nom).lower() == str(other.prenom).lower()
        else:
            return False
        ###### ===> class Database / include tout les methodes pour manipuler la base de données #####


class Database:
    # ----> constructor
    def __init__(self):
        self.con = sqlite3.connect(
            'configs/person.db')
        self.c = self.con.cursor()

    # ----> create table if not exist

    def close(self):
        if(self.con):
            self.con.close()

    def initiate(self):
        # ----> create a table : Person
        self.c.execute("""CREATE TABLE IF NOT EXISTS Person(
        id integer primary key AUTOINCREMENT,
        nom TEXT,
        prenom TEXT
        )
        """)
    # ----> create a table : Face
        self.c.execute("""CREATE TABLE IF NOT EXISTS Face(
            face_id integer primary key AUTOINCREMENT,
            person_id TEXT,
            image BLOB,
            face_encode TEXT,
            FOREIGN KEY(person_id) REFERENCES Person(id) on delete cascade
            )
            """)
        # ---> commit les modification
        self.con.commit()


# ----> test insert
# c.execute("insert into Person(nom,prenom) values('Elbouchouki','Ahmed')")
# con.commit()
# ----> requet select
# c.execute("select * from Person")
# items = c.fetchall()
# for item in items:
#     print(item)
    # ----> add person to the database

    def convertImgToBinary(self, img):
        return sqlite3.Binary(img.read())

    def add_person(self, person: Person):
        nom = str(person.getNom())
        prenom = str(person.getPrenom())
        self.c.execute(
            "insert into Person(nom,prenom) values(?,?)", (nom, prenom))
        self.con.commit()
    # ----> delete person from the database

    def delete_person(self, person: Person):
        nom = str(person.getNom())
        prenom = str(person.getPrenom())
        self.c.execute(
            "delete from Person where nom = ? and prenom = ?", (nom, prenom))
        self.con.commit()
    # ----> update a person given in parameters the person

    def update_person(self, person: Person, personOld: Person):
        nomOld = personOld.getNom()
        prenomOld = personOld.getPrenom()
        nom = person.getNom()
        prenom = person.getPrenom()
        self.c.execute(
            "update Person set nom = ? , prenom = ? where nom = ? and prenom = ?", (nom, prenom, nomOld, prenomOld))
        self.con.commit()
    # ----> get person from database by given its id in parameters | return Object Person

    def getById_person(self, person: Person):
        id = person.getId()
        self.c.execute("select * from Person where id = ?", id)
        item = self.c.fetchone()
        person = Person(item[1], item[2])
        person.setId(item[0])
        return person

    def get_person(self, person: Person):
        nom = person.getNom()
        prenom = person.getPrenom()
        self.c.execute(
            "select * from Person where nom = ? and prenom = ?", (nom, prenom))
        item = self.c.fetchone()
        person = Person(item[1], item[2])
        person.setId(item[0])
        return person

    # ----> delete person from the database | return list of arrays ( Tableau d'arraylist) => [(),(),()]

    def get_all_person(self):
        self.c.execute("select id,nom,prenom from Person")
        items = self.c.fetchall()
        listPerson = []
        for item in items:
            person = Person(str(item[1]), str(item[2]))
            person.setId(item[0])
            listPerson.append(person)
        return listPerson
    # ----> get all encoded faces (128dim) from the database | return dictionary (comme associative arrays)  => {}

    def get_encoded_faces(self):
        encoded = {}
        self.c.execute(
            "select nom,prenom,face_id,face_encode from Person,Face where Person.id=Face.person_id")
        items = self.c.fetchall()
        for row in items:
            fullname = str(row[2])+" "+str(row[1])+" "+str(row[0])
            encode = json.loads(row[3])
            for i in range(len(encode)):
                encode[i] = float(encode[i])
            encoding = np.array(encode)
            encoded[fullname] = encoding
        return encoded
    # ----> delete face from database given Face in parameters

    def delete_face(self, face: Face):
        id = face.get_face_id()
        print(id)
        self.c.execute("delete from Face where face_id=" + id)
        self.con.commit()

    # def adapt_array(arr):
    #     out = io.BytesIO()
    #     np.save(out, arr)
    #     out.seek(0)
    #     return sqlite3.Binary(out.read())

    # def convert_array(text):
    #     out = io.BytesIO(text)
    #     out.seek(0)
    #     return np.load(out)s
    def add_face(self, face: Face):
        person_id = face.get_person_id()
        image = face.get_image()
        face_encode = face.get_face_encode()
        stringArray = str((np.array2string(face_encode))[1:-1]).split()
        jarray = json.dumps(stringArray)
        print(image)
        self.c.execute(
            "insert into Face(person_id,image,face_encode) values(?,?,?)", (person_id, image, jarray))
        self.con.commit()

    # ----> get all images that a person have (parameters person) |return list of (id , image)

    def get_person_images(self, person: Person):
        id = person.getId()
        self.c.execute(
            "select face_id,image from Face where person_id = ?", str(id))
        items = self.c.fetchall()
        return items
