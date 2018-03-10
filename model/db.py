import sqlite3

class DB:
    def __init__(self):
        self.setup();

    def setup(self):
        self.conn = sqlite3.connect('register.db');
        cursor = self.conn.cursor();
        createTableUsers = """CREATE TABLE IF NOT EXISTS 'users' (
				user_name     STRING NOT NULL,
				user_genre    STRING NOT NULL,
				user_cpf      STRING NOT NULL
                                                PRIMARY KEY,
				user_birthDay DATE   NOT NULL
			)"""
        createTableExams  = """CREATE TABLE IF NOT EXISTS 'exams'(
                                exam_id     INTEGER PRIMARY KEY AUTOINCREMENT,
                                exam_data   STRING NOT NULL,
                                exam_date   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                user_cpf    STRING NOT NULL,
                                CONSTRAINT  fk_user_exam FOREIGN KEY (user_cpf) REFERENCES users (user_cpf)
                        )"""
        cursor.execute(createTableUsers);
        cursor.execute(createTableExams);
        self.conn.commit();


    # TODO: use try excep to erros
    def insertUser(self, name, genre, cpf, birthDay):
        cursor = self.conn.cursor();
        cursor.execute("INSERT INTO 'users' VALUES(:name, :genre, :cpf, :birthDay)",
                        { 'name': name, 'genre': genre, 'cpf':cpf, 'birthDay': birthDay });
        self.conn.commit();

    # TODO: Verify if user CPF exist
    def insertExam( self, user_cpf, exam_data ):
        cursor = self.conn.cursor();
        cursor.execute("INSERT INTO 'exams'(exam_data, user_cpf) VALUES(:exam_data, :user_cpf)",
                        { 'exam_data': exam_data, 'user_cpf': user_cpf });
        self.conn.commit();

    def consult( self, cpf ):
        try:
            cursor = self.conn.cursor();
            rows = cursor.execute( "SELECT users.user_name, exams.exam_date FROM 'users' INNER JOIN 'exams' ON users.user_cpf = exams.user_cpf WHERE users.user_cpf = :cpf", {'cpf': cpf} );
            return rows;
        except Exception as e:
            raise e;
            return None;

    def specificConsult( self, cpf, index ):
        try:
            cursor = self.conn.cursor();
            row = cursor.execute( "SELECT * FROM 'users' INNER JOIN 'exams' ON users.user_cpf = exams.user_cpf WHERE users.user_cpf = :cpf LIMIT :row,1", {'cpf': cpf, 'row': index} );
            return row;
        except Exception as e:
            raise e;
            return None;

    def checkUser(self, user_cpf):
        try:
            cursor = self.conn.cursor();
            cursor.execute( "SELECT user_name FROM 'users' WHERE users.user_cpf = :cpf", {'cpf': user_cpf} );
            data = cursor.fetchall();
            if len(data) == 0:
                return False;
            else:
                return True;
        except Exception as e:
            raise e;
            return False;

if __name__ == "__main__":
    db = DB();
    db.insert('Luan', 'Masculino', '01149272279', '1991-08-12');
