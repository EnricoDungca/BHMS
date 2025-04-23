from tkinter import messagebox
from cryptography.fernet import Fernet
import mysql.connector
import smtplib
import random as rd
from dotenv import load_dotenv, dotenv_values
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


config = {
    **dotenv_values(r"Back_End\.env.secret")
}

class email():
    def __init__(self, email, validation):
        self.email = email
        self.validate = validation
        self.code = rd.randint(100000, 999999)
        
    def verify_gmail(self):
        no_white_space = self.email
        return no_white_space.endswith(("@gmail.com", "icloud.com"))

    def otp_send(self):
        if self.validate and self.verify_gmail():
            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(config["EMAIL"], config["GOOGLE_KEY"])
                server.sendmail(config["EMAIL"], self.email, f"""Subject: OTP\n\nYour OTP is {self.code}""")
                return self.code
            except Exception as e:
                messagebox.showerr or("Error", "Error in sending OTP", str(e))
        else:
            messagebox.showerror("Error", "Invalid email address")
            
    def send_email(self, message):
        if self.verify_gmail():
            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(config["EMAIL"], config["GOOGLE_KEY"])
                server.sendmail(config["EMAIL"], self.email, message.as_string())
            except Exception as e:
                messagebox.showerr or("Error", "Error in sending OTP", str(e))
        else:
            messagebox.showerror("Error", "Invalid email address")
    

class authentication():
    def __init__(self, email, password):
        self.email = email
        self.password = password
        
    def verify_login(self):
        try:
            for row in database_con().read("accounts", "*"):
                if self.email == row[4]:
                    if self.password == Security().decrypt_str(row[5]):
                        return row[0], True
            return False
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def verify_login_admin(self):
        try:
            for row in database_con().read("admin", "*"):
                if self.email == row[2]:
                    if self.password == row[3]:
                        return True
            return False
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def main(self, mode):
        if mode == "user":
            return self.verify_login()
        elif mode == "admin":
            return self.verify_login_admin()
        
    
    

# This class isused to encrypt and decrypt String
class Security:
    def __init__(self):
        self.Encrpt_key = config["ENCRYPT_KEY"].encode()
        
    def Encrypt_str(self, text):
        cipher_suite = Fernet(self.Encrpt_key) 
        ciphertext = cipher_suite.encrypt(text.encode())
        return ciphertext
    
    def decrypt_str(self, encrypted_str):
        cipher_suite = Fernet(self.Encrpt_key)
        plaintext = cipher_suite.decrypt(encrypted_str)
        return plaintext.decode()
    
    
# This class is used to connect to the database and execute queries
class database_con:
    def __init__(self):
        self.mydb = None
        self.host = config["HOST"]
        self.user = config["USER"]
        self.passw = config["PASSWORD"]
        self.DBName = config["DATABASE"]
    
    # This function is used to check the connection
    def check_connection(self):
        try:
            self.mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.passw,
                database=self.DBName
            )
            return self.mydb
        except mysql.connector.Error as e:
            print("Error: " + str(e))
            return None
        
    # This function is used to close the connection
    def close_connection(self):
        if self.mydb:
            self.mydb.close()
    
    # This function is used to insert data
    def insert(self, Table: str, Column_Names: list, values: tuple):
        database_con.check_connection(self)
        if not self.mydb:
            messagebox.showwarning("Warning", "No active database connection.")
            return  # Stop execution if no connection

        try:
            cursor = self.mydb.cursor()

            # Ensure Column_Names is a list
            if isinstance(Column_Names, str):  
                Column_Names = [Column_Names]  # Convert to list if it's a string

            # Convert list to properly formatted SQL column names
            columns = ", ".join(Column_Names)

            # Generate placeholders (%s, %s, ...) dynamically
            placeholders = ", ".join(["%s"] * len(values))

            # Safe SQL query using placeholders
            sql = f"INSERT INTO {Table} ({columns}) VALUES ({placeholders})"
            
            # Execute safely
            cursor.execute(sql, values)

            self.mydb.commit()

            messagebox.showinfo("Success", "Record inserted successfully.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error: {e}")
        finally:
            if cursor:
                cursor.close()


    # This function is used to update data
    def Record_edit(self, Table, Column_Names, new_value, condition_column, condition_value):
        database_con.check_connection(self)
        if not self.mydb:
            messagebox.showwarning("Warning", "No active database connection.")
            return  # Stop execution

        try:
            cursor = self.mydb.cursor()

            # Safe parameterized SQL query
            sql = f"UPDATE {Table} SET {Column_Names} = %s WHERE {condition_column} = %s"
            cursor.execute(sql, (new_value, condition_value))

            self.mydb.commit()

            messagebox.showinfo("Success", "Table updated successfully.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", "Error: " + str(e))
        finally:
            if cursor:
                cursor.close()

    # This function is used to delete data
    def Record_delete(self, Tablename, condition_column, condition_value):
        database_con.check_connection(self)
        if not self.mydb:
            messagebox.showwarning("Warning", "No active database connection.")

        try:
            cursor = self.mydb.cursor()
            sql = f"DELETE FROM {Tablename} WHERE {condition_column} = %s"
            cursor.execute(sql, (condition_value,))

            self.mydb.commit()

            messagebox.showinfo("Success", "Record deleted successfully.")
        except mysql.connector.Error as e:
            print("Error: " + str(e))
        finally:
            cursor.close()
    
    # This function is used to read data
    def read(self, Tablename, ColumnName):
        database_con.check_connection(self)  # Ensure database connection is active
        if not self.mydb:
            messagebox.showwarning("Warning", "No active database connection.")
            return []  # Return an empty list if no connection

        try:
            cursor = self.mydb.cursor()
            sql = f"SELECT {ColumnName} FROM {Tablename}"
            cursor.execute(sql)

            result = cursor.fetchall()  # Fetch all rows at once

            if not result:  # If no data is found
                print("No records found.")
                return []

            # for row in result:
            return result  # Return all fetched rows
        except mysql.connector.Error as e:
            messagebox.showerror("Error", "Error: " + str(e))
            return []
        finally:
            cursor.close()

def read_data():
    data1 = database_con().read("accounts", "*")
    data2 = database_con().read("admin", "*")
    data3 = database_con().read("appointment", "*")
    data4 = database_con().read("registration", "*")
    