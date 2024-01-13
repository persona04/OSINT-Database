import mysql.connector
import hashlib
 
class MySQLConnect():

    # Method for authentication
    def login_authentication(self,username:str,passwd:str):
        try:
            mydb = mysql.connector.connect(host="localhost",user="root",passwd="iamroot",database="credentials")
            self.cursor = mydb.cursor()
        # For connection problem.
        except Exception:
            return [500,]
        self.cursor.execute("SELECT username,passwd,privilege FROM credentials WHERE username= %s AND passwd= %s ;",(username,passwd))
        self.result = self.cursor.fetchone()
        mydb.close()
        
        # If there is a resutl, it will return 200.
        if self.result:
            return [200,self.result[2]]
        # If there isn't any result, that's mean unauthenticated. Returns 401.
        else:
            return [401,]
    # Method for password hashing.
    def hash_passwd(self,passwd:str):
        h = hashlib.sha256()
        h.update(passwd.encode("utf-8"))
        return h.hexdigest()
    
    # Query for address searching
    def address_table_query(self,address):
        try:
            self.mydb = mysql.connector.connect(host="localhost",user="root",passwd="iamroot",database="testdb")
            self.cursor = self.mydb.cursor()
        # For connection problem.
        except Exception:
            return 500

        # For searching with address
        self.cursor.execute("SELECT address.person_id, persons.p_name, persons.p_surname, address.dsc, address.address, address.evidence_id FROM address INNER JOIN persons ON address.person_id = persons.person_id WHERE address LIKE %s;",(address,))
        self.results = self.cursor.fetchall()
        self.mydb.close()
        return self.results
    
    # Query for phone number searching
    def phone_number_table_query(self,number):
        try:
            self.mydb = mysql.connector.connect(host="localhost", user="root", passwd="iamroot", database="testdb")
            self.cursor = self.mydb.cursor()
        except Exception:
            return 500

        self.query = "SELECT phone_numbers.person_id, persons.p_name, persons.p_surname, phone_numbers.dsc, phone_numbers.phone_number, phone_numbers.evidence_id FROM phone_numbers INNER JOIN persons ON phone_numbers.person_id = persons.person_id WHERE phone_numbers.phone_number= %s  "
        for self.i in range(1,len(number)):
            self.query = self.query +" or phone_numbers.phone_number= %s "
        self.query = self.query + ";"
        # For searching with phone numbers.
        self.cursor.execute(self.query,number)
        self.results = self.cursor.fetchall()
        self.mydb.close()
        return self.results
    
    def account_table_query(self,info,flag):
        try:
            self.mydb = mysql.connector.connect(host="localhost",user="root",passwd="iamroot",database="testdb")
            self.cursor = self.mydb.cursor()
        
        except Exception:
            return 500
        
        if flag == "email":
            self.query = "SELECT accounts.person_id, accounts.dsc, email_address.mail_address, credentials.username, accounts.evidence_id FROM accounts INNER JOIN email_address on accounts.email_id = email_address.email_id INNER JOIN credentials ON accounts.credential_id = credentials.cred_id WHERE email_address.mail_address LIKE %s;"
            self.param = "%"+info+"%"
            self.cursor.execute(self.query,(self.param,))
            self.results= self.cursor.fetchall()
            self.mydb.close()
            return self.results
        
        elif flag == "username":
            self.query = "SELECT accounts.person_id, accounts.dsc, email_address.mail_address, credentials.username, accounts.evidence_id FROM accounts INNER JOIN credentials ON accounts.credential_id = credentials.cred_id INNER JOIN email_address ON accounts.email_id = email_address.email_id WHERE accounts.credential_id IN (SELECT cred_id FROM credentials WHERE username LIKE %s);"
            self.param = "%"+info+"%"
            self.cursor.execute(self.query,(self.param,))
            self.results = self.cursor.fetchall()
            self.mydb.close()
            return self.results
        elif flag == "site":
            self.query = "SELECT accounts.person_id, accounts.dsc, email_address.mail_address, credentials.username, accounts.evidence_id FROM accounts INNER JOIN credentials ON accounts.credential_id = credentials.cred_id INNER JOIN email_address ON accounts.email_id = email_address.email_id WHERE accounts.dsc LIKE %s ;"
            self.param = "%"+info+"%"
            self.cursor.execute(self.query,(self.param,))
            self.results = self.cursor.fetchall()
            self.mydb.close()
            return self.results
        
    def person_table_query(self,param,flag):
        try:
            self.mydb = mysql.connector.connect(host="localhost",user="root",passwd="iamroot",database="testdb")
            self.cursor = self.mydb.cursor()
        
        except Exception:
            return 500

        if flag == "list":
            param = param.strip()
            if " " in param:
                param = param.split(" ")
                self.query="SELECT person_id, p_name, p_surname, p_birth_date FROM persons WHERE p_name= %s AND p_surname= %s ;"
                self.cursor.execute(self.query,param)
                self.results = self.cursor.fetchall()
                self.mydb.close()
                return self.results
            else:
                self.query = "SELECT person_id, p_name, p_surname, p_birth_date FROM persons WHERE p_name= %s OR p_surname= %s ;"
                param = (param,param)
                self.cursor.execute(self.query, param)
                self.results = self.cursor.fetchall()
                self.mydb.close()
                return self.results
        else:
            if flag == "Email":
                self.query = "SELECT dsc, mail_address, evidence_id FROM email_address WHERE person_id=%s;"
                self.cursor.execute(self.query,(param,))
                self.results = self.cursor.fetchall()
                self.mydb.close()
                return self.results
            elif flag == "Credential":
                self.query = "SELECT username, passwd, evidence_id FROM credentials WHERE cred_id in (SELECT credential_id from accounts WHERE person_id=%s);"
                self.cursor.execute(self.query,(param,))
                self.results = self.cursor.fetchall()
                self.mydb.close()
                return self.results
            elif flag == "Account":
                self.query = "SELECT accounts.dsc, email_address.mail_address, credentials.username, accounts.evidence_id FROM accounts INNER JOIN email_address ON email_address.email_id = accounts.email_id INNER JOIN credentials ON accounts.credential_id = credentials.cred_id WHERE accounts.person_id =%s "
                self.cursor.execute(self.query,(param,))
                self.results = self.cursor.fetchall()
                self.mydb.close()
                return self.results
            elif flag == "Address":
                self.query = "SELECT dsc, address, evidence_id FROM address WHERE person_id=%s;"
                self.cursor.execute(self.query,(param,))
                self.results = self.cursor.fetchall()
                self.mydb.close()
                return self.results
            elif flag == "Phone Numbers":
                self.query = "SELECT dsc, phone_number, evidence_id FROM phone_numbers WHERE person_id=%s;"
                self.cursor.execute(self.query,(param,))
                self.results = self.cursor.fetchall()
                self.mydb.close()
                return self.results
            elif flag == "Notes":
                self.query = "SELECT note, evidence_id FROM notes WHERE person_id=%s;"
                self.cursor.execute(self.query,(param,))
                self.results = self.cursor.fetchall()
                self.mydb.close()
                return self.results
    
    def add_queries(self,qtype,query_args:tuple):
        try:
            self.mydbs = mysql.connector.connect(host="localhost",user="root",passwd="iamroot",database="testdb")
            self.cursor = self.mydbs.cursor()
        
        except Exception:
            return 500
        
        if qtype == "Person":
            self.query = "INSERT INTO persons(p_name,p_surname,p_birth_date) VALUES (%s,%s,%s);"
        elif qtype == "Email":
            self.query = "INSERT INTO email_address(person_id,dsc,mail_address,evidence_id) VALUES(%s,%s,%s,10);"
        elif qtype == "Account":
            self.query = "INSERT INTO evidence(e_date,source, reliability_score) VALUES(%s,%s,%s); set @dat = LAST_INSERT_ID(); INSERT INTO accounts(person_id,dsc,email_id,credential_id,evidence_id) VALUES(%s,%s,%s,%s,@dat);"
        elif qtype == "Note":
            self.query = "INSERT INTO evidence(e_date,source, reliability_score) VALUES(%s,%s,%s); set @dat = LAST_INSERT_ID(); INSERT INTO notes(person_id,note,evidence_id) VALUES(%s,%s,@dat);"
        elif qtype == "Adress":
            self.query = "INSERT INTO evidence(e_date,source, reliability_score) VALUES(%s,%s,%s); set @dat = LAST_INSERT_ID(); INSERT INTO address(person_id,dsc,address,evidence_id) VALUES(%s,%s,%s,@dat);"
        elif qtype == "Phone Number":
            self.query = "INSERT INTO evidence(e_date,source, reliability_score) VALUES(%s,%s,%s); set @dat = LAST_INSERT_ID(); INSERT INTO phone_numbers(person_id,dsc,phone_number,evidence_id) VALUES(%s,%s,%s,@dat);"
        elif qtype == "Credential":
            self.query = "INSERT INTO evidence(e_date,source, reliability_score) VALUES(%s,%s,%s); set @dat = LAST_INSERT_ID(); INSERT INTO credentials(username,passwd,evidence_id) VALUES(%s,%s,@dat);"
        
        try:
            self.cursor.execute(self.query,query_args,multi=True)
            self.mydbs.commit()
        except mysql.connector.errors as e:
            print(e)

    def register_query(self,username,password):
        try:
            self.mydb = mysql.connector.connect(host="localhost",user="root",passwd="iamroot",database="credentials")
            self.cursor = self.mydb.cursor()
        
        except Exception:
            return 500
        
        try:
            self.cursor = self.mydb.cursor()
            self.args = (username,password) 
            self.query ="INSERT INTO credentials(username,passwd,privilege) VALUES(%s,%s,0) ;"
            self.cursor.execute(self.query,self.args)
            self.mydb.commit()
        
        except mysql.connector.errors:
            return 400
        
        # Aggregation queries
        # SELECT person_id, count(*) AS "Account Number" FROM accounts GROUP BY person_id;
        # SELECT person_id, count(*) AS "Account Number" FROM accounts GROUP BY person_id HAVING count(*)>1;
        # SELECT persons.p_name, count(*) AS "Account Number" FROM accounts INNER JOIN persons ON accounts.person_id = persons.person_id GROUP BY accounts.person_id;
        
        # SELECT p_name, p_surname FROM persons ORDER BY p_name ASC, p_surname DESC;
        