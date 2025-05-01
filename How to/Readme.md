# Birthing Home Management System

## About

A Birthing Home Management System is a desktop application solution designed to help manage various aspects of a birthing home or maternity clinic. The system typically focuses on digitizing and organizing the management of patient records, appointments, medical history, billing, and other essential administrative tasks. It streamlines operations and enhances the overall patient experience by providing easy access to critical information.

The key features of a Birthing Home Management System may include:

1. **_Patient Management:_**

   - Patient registration and record-keeping.

   - Tracking personal information, medical history, emergency contacts, and Insurance Details.

   - Appointment scheduling and tracking.

2. **_Medical Record Management:_**

   - Storing and updating medical records related to checkups and Normal Spontaneous Delivery.

   - Providing easy access to patient medical histories for healthcare providers.

3. **_Billing and Payments:_**

   - Managing charges for consultations, delivery services, and any additional care.

   - Issuing invoices and tracking payments.

   - Generating financial reports.

4. **_Inventory and Bed Management:_**

   - Tracking available beds assignments.

   - Managing medical supplies and other resources required for birthing homes.

5. **_Scheduling and Appointments:_**

   - Scheduling appointments for check-ups, deliveries, and post-natal care.

   - Managing appointments and ensuring availability of resources such as doctors and rooms.

6. **_Account and User Management:_**

   - Managing user roles and permissions (e.g., administrators, doctors, nurses).

   - Supporting the registration of new staff and managing access to sensitive information.

A Birthing Home Management System can help ensure that a birthing home operates smoothly, provides quality care, and maintains accurate records in a secure and organized manner.

## Modules Used

- Birthing Home Management System are Build in full Python code.

```python
# Tkinter modules for GUI elements and layouts
import tkinter as tk
from tkinter import font, ttk, messagebox, simpledialog, scrolledtext, filedialog
from tkinter.font import Font

# Date and time modules
from datetime import date, datetime

# CustomTkinter for enhanced UI elements
import customtkinter as ctk

# Tkinter calendar widget
from tkcalendar import DateEntry

# JSON handling for working with configuration or data files
import json

# OS-related functionalities like file handling and environment variables
import os

# System-related functions like exiting the program
import sys

# Time-related utilities, such as delays or time tracking
import time

# Cryptography for secure encryption/decryption (Fernet key)
from cryptography.fernet import Fernet

# MySQL Connector for database operations
import mysql.connector

# Email-related modules for sending emails
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Random module for generating random numbers or selections
import random as rd

# Dotenv for loading environment variables from .env files
from dotenv import load_dotenv, dotenv_values

# Regular expression (regex) module for pattern matching
import re

```

# How to Setup and Deploy

### how to setup

1.  **_Setup Database and desktop Application:_**

    - Clone Github Repositoty From CMD/Terminal:

      1. Open terminal or cmd
      2. choose directory where you want to clone the repository and
      3. Type This: gh repo clone EnricoDungca/BHMSapp

    - import ".spl" file to localhost/phpmyadmin:

      1.  Download Xampp.
      2.  after download Open Xampp and start Apache and MySql
      3.  And go to browser type "http://localhost/phpmyadmin/index.php" or open xamp and click "Admin" on MySql.
      4.  After opening look for "Import" and "Choose File" choose the .spl file that you cloned earlier click "Go".
