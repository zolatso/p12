import re
import rich_click as click
from datetime import datetime, date

email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'
french_phone_regex = r'^0[1-9]\d{8}$'


def valid_email(msg="Email"):
    while True:
        email = click.prompt(msg)
        if re.match(email_regex, email):
            return email
        click.echo("L'adresse e-mail n'est pas dans le bon format. Veuillez réessayer.")

def valid_string(length, msg):
    while True:
        input = click.prompt(msg)
        if len(input) <= length:
            return input
        click.echo("L'adresse e-mail n'est pas dans le bon format. Veuillez réessayer.")

def valid_password():
    while True:
        pw = click.prompt("Mot de passe (le mot de passe doit contenir au moins : une majuscule, un caractère spécial et un chiffre)")
        if re.match(password_regex, pw):
            return pw
        click.echo("Le mot de passe doit contenir au moins : une majuscule, un caractère spécial et un chiffre.")

def valid_phone():
    while True:
        phone = click.prompt("Numero de telephone (0x-xx-xx-xx-xx): ")
        if re.match(french_phone_regex, phone):
            return phone
        click.echo("Le numero de telephone n'est pas valide. Veuillez réessayer.")

def valid_date(msg, optional=False):
    while True:
        date_str = click.prompt(msg, default='', show_default=False)
        if optional and date_str == "":
            date_str = date.today().strftime("%d/%m/%Y")
        try:
            # Try parsing the input as DD/MM/YYYY
            datetime.strptime(date_str, "%d/%m/%Y")
            return date_str
        except ValueError:
            click.echo("La date doit être valide et au format: dd/mm/yyyy")

def valid_datetime(msg):
    while True:
        datetime_str = click.prompt(msg)
        try:
            # Try parsing the input as DD/MM/YYYY HH;MM
            datetime.strptime(datetime_str, "%d/%m/%Y %H:%M")
            return datetime_str
        except ValueError:
            click.echo("L'heure doit être valide et au format: dd/mm/yyyy HH:MM")

def valid_int(msg):
    while True:
        int_string = click.prompt(msg)
        try:
            int(int_string)
            return int_string
        except ValueError:
            click.echo("Le montant doit être un nombre entier.")