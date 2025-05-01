from tkinter import messagebox
from cryptography.fernet import Fernet
import mysql.connector
import smtplib
import random as rd
from dotenv import dotenv_values
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys, os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller bundle"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Load .env.secret
env_path = resource_path("config\.env.secret")
if not os.path.exists(env_path):
    messagebox.showerror("Error", f".env.secret file not found at: {env_path}")

config = dotenv_values(env_path)

class email:
    def __init__(self, email, validation):
        self.email = email
        self.validate = validation
        self.code = rd.randint(100000, 999999)
        
    def verify_gmail(self):
        return self.email.endswith(("@gmail.com", "@icloud.com"))

    def otp_send(self):
        if self.validate and self.verify_gmail():
            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(config["EMAIL"], config["GOOGLE_KEY"])
                server.sendmail(config["EMAIL"], self.email, f"""Subject: OTP\n\nYour OTP is {self.code}""")
                server.quit()
                return self.code
            except Exception as e:
                messagebox.showerror("Error", f"Error in sending OTP: {e}")
        else:
            messagebox.showerror("Error", "Invalid email address")
            
    def send_email(self, message):
        if self.verify_gmail():
            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(config["EMAIL"], config["GOOGLE_KEY"])
                server.sendmail(config["EMAIL"], self.email, message.as_string())
                server.quit()
            except Exception as e:
                messagebox.showerror("Error", f"Error in sending email: {e}")
        else:
            messagebox.showerror("Error", "Invalid email address")

class authentication:
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
                if self.email == row[2] and self.password == row[3]:
                    return row[0], True
            return False
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def main(self, mode):
        if mode == "user":
            return self.verify_login()
        elif mode == "admin":
            return self.verify_login_admin()

class Security:
    def __init__(self):
        self.Encrpt_key = config["ENCRYPT_KEY"].encode()
        
    def Encrypt_str(self, text):
        cipher_suite = Fernet(self.Encrpt_key) 
        return cipher_suite.encrypt(text.encode())
    
    def decrypt_str(self, encrypted_str):
        cipher_suite = Fernet(self.Encrpt_key)
        return cipher_suite.decrypt(encrypted_str).decode()

class database_con:
    def __init__(self):
        self.mydb = None
        self.host = config["HOST"]
        self.user = config["USER"]
        self.passw = config["PASSWORD"]
        self.DBName = config["DATABASE"]
    
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
        
    def close_connection(self):
        if self.mydb:
            self.mydb.close()
    
    def insert(self, Table: str, Column_Names: list, values: tuple):
        self.check_connection()
        if not self.mydb:
            messagebox.showwarning("Warning", "No active database connection.")
            return

        cursor = None
        try:
            cursor = self.mydb.cursor()
            if isinstance(Column_Names, str):  
                Column_Names = [Column_Names]

            columns = ", ".join(Column_Names)
            placeholders = ", ".join(["%s"] * len(values))
            sql = f"INSERT INTO {Table} ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, values)
            self.mydb.commit()
            messagebox.showinfo("Success", "Record inserted successfully.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error: {e}")
        finally:
            if cursor:
                cursor.close()

    def Record_edit(self, Table, Column_Names, new_value, condition_column, condition_value):
        self.check_connection()
        if not self.mydb:
            messagebox.showwarning("Warning", "No active database connection.")
            return

        cursor = None
        try:
            cursor = self.mydb.cursor()
            sql = f"UPDATE {Table} SET {Column_Names} = %s WHERE {condition_column} = %s"
            cursor.execute(sql, (new_value, condition_value))
            self.mydb.commit()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", "Error: " + str(e))
        finally:
            if cursor:
                cursor.close()

    def Record_delete(self, Tablename, condition_column, condition_value):
        self.check_connection()
        if not self.mydb:
            messagebox.showwarning("Warning", "No active database connection.")
            return

        cursor = None
        try:
            cursor = self.mydb.cursor()
            sql = f"DELETE FROM {Tablename} WHERE {condition_column} = %s"
            cursor.execute(sql, (condition_value,))
            self.mydb.commit()
            messagebox.showinfo("Success", "Record deleted successfully.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", str(e))
        finally:
            if cursor:
                cursor.close()
    
    def read(self, Tablename, ColumnName):
        self.check_connection()
        if not self.mydb:
            messagebox.showwarning("Warning", "No active database connection.")
            return []

        cursor = None
        try:
            cursor = self.mydb.cursor()
            sql = f"SELECT {ColumnName} FROM {Tablename}"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result if result else []
        except mysql.connector.Error as e:
            messagebox.showerror("Error", "Error: " + str(e))
            return []
        finally:
            if cursor:
                cursor.close()
        
    def column_names(self, Tablename):
        self.check_connection()
        if not self.mydb:
            messagebox.showwarning("Warning", "No active database connection.")
            return []

        cursor = None
        try:
            cursor = self.mydb.cursor()
            cursor.execute(f"SHOW COLUMNS FROM {Tablename}")
            result = cursor.fetchall()
            return result if result else []
        except mysql.connector.Error as e:
            messagebox.showerror("Error", "Error: " + str(e))
            return []
        finally:
            if cursor:
                cursor.close()
