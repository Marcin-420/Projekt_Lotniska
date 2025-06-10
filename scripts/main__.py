from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

airports = []
customers = []


class Airport:
    def __init__(self, name, location, iata_code):
        self.name = name
        self.location = location
        self.iata_code = iata_code
        self.employees = []
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=self.name)

    def get_coordinates(self):
        try:
            url = f'https://pl.wikipedia.org/wiki/{self.location}'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            latitude = float(soup.select('.latitude')[1].text.replace(',', '.'))
            longitude = float(soup.select('.longitude')[1].text.replace(',', '.'))
            return [latitude, longitude]
        except Exception as e:
            print(f"Błąd pobierania współrzędnych: {e}")
            return [52.23, 21.01]


class Employee:
    def __init__(self, first_name, last_name, position):
        self.first_name = first_name
        self.last_name = last_name
        self.position = position


class Customer:
    def __init__(self, first_name, last_name, passport):
        self.first_name = first_name
        self.last_name = last_name
        self.passport = passport


# GUI
root = Tk()
root.geometry("1300x900")
root.title("System zarządzania lotniskami")

frame_airports = Frame(root)
frame_form = Frame(root)
frame_details = Frame(root)
frame_map = Frame(root)
frame_customers = Frame(root)  # ← DODANE

frame_airports.grid(row=0, column=0, sticky=N)
frame_form.grid(row=0, column=1, sticky=N)
frame_details.grid(row=1, column=0, columnspan=2)
frame_map.grid(row=2, column=0, columnspan=2)
frame_customers.grid(row=0, column=2, rowspan=3, sticky=N)  # ← DODANE

# Lotniska
Label(frame_airports, text="Lista lotnisk:").grid(row=0, column=0)
listbox_airports = Listbox(frame_airports, width=45, height=10)
listbox_airports.grid(row=1, column=0, columnspan=3)


def refresh_airports():
    listbox_airports.delete(0, END)
    for idx, a in enumerate(airports):
        listbox_airports.insert(idx, f"{idx + 1}. {a.name} ({a.iata_code})")


def add_airport():
    name = entry_name.get()
    location = entry_location.get()
    iata = entry_iata.get()

    airport = Airport(name, location, iata)
    airports.append(airport)

    entry_name.delete(0, END)
    entry_location.delete(0, END)
    entry_iata.delete(0, END)

    refresh_airports()


def remove_airport():
    i = listbox_airports.index(ACTIVE)
    if airports[i].marker:
        airports[i].marker.delete()
    airports.pop(i)
    refresh_airports()


def show_airport_details():
    i = listbox_airports.index(ACTIVE)
    selected = airports[i]
    label_detail_name_value.config(text=selected.name)
    label_detail_location_value.config(text=selected.location)
    label_detail_iata_value.config(text=selected.iata_code)
    label_detail_employees.config(text="\n".join(
        [f"{e.first_name} {e.last_name} ({e.position})" for e in selected.employees]) or "Brak"
    )
    map_widget.set_position(*selected.coordinates)
    map_widget.set_zoom(12)


def add_employee_to_airport():
    i = listbox_airports.index(ACTIVE)
    if i is None:
        return
    airport = airports[i]
    e_name = entry_emp_name.get()
    e_surname = entry_emp_surname.get()
    e_position = entry_emp_position.get()

    employee = Employee(e_name, e_surname, e_position)
    airport.employees.append(employee)

    entry_emp_name.delete(0, END)
    entry_emp_surname.delete(0, END)
    entry_emp_position.delete(0, END)

    show_airport_details()


# Formularz - lotniska i pracownicy
Label(frame_form, text="Dodaj lotnisko:").grid(row=0, column=0, columnspan=2)

Label(frame_form, text="Nazwa:").grid(row=1, column=0, sticky=W)
entry_name = Entry(frame_form)
entry_name.grid(row=1, column=1)

Label(frame_form, text="Lokalizacja:").grid(row=2, column=0, sticky=W)
entry_location = Entry(frame_form)
entry_location.grid(row=2, column=1)

Label(frame_form, text="Kod IATA:").grid(row=3, column=0, sticky=W)
entry_iata = Entry(frame_form)
entry_iata.grid(row=3, column=1)

Button(frame_form, text="Dodaj lotnisko", command=add_airport).grid(row=4, column=0, columnspan=2)

Button(frame_airports, text="Pokaż szczegóły", command=show_airport_details).grid(row=2, column=0)
Button(frame_airports, text="Usuń", command=remove_airport).grid(row=2, column=1)

# Pracownicy
Label(frame_form, text="Dodaj pracownika:").grid(row=5, column=0, columnspan=2)
Label(frame_form, text="Imię:").grid(row=6, column=0)
entry_emp_name = Entry(frame_form)
entry_emp_name.grid(row=6, column=1)

Label(frame_form, text="Nazwisko:").grid(row=7, column=0)
entry_emp_surname = Entry(frame_form)
entry_emp_surname.grid(row=7, column=1)

Label(frame_form, text="Stanowisko:").grid(row=8, column=0)
entry_emp_position = Entry(frame_form)
entry_emp_position.grid(row=8, column=1)

Button(frame_form, text="Dodaj pracownika", command=add_employee_to_airport).grid(row=9, column=0, columnspan=2)

# Szczegóły lotniska
Label(frame_details, text="Szczegóły lotniska:").grid(row=0, column=0, columnspan=2)
Label(frame_details, text="Nazwa:").grid(row=1, column=0)
label_detail_name_value = Label(frame_details, text="---")
label_detail_name_value.grid(row=1, column=1)

Label(frame_details, text="Lokalizacja:").grid(row=2, column=0)
label_detail_location_value = Label(frame_details, text="---")
label_detail_location_value.grid(row=2, column=1)

Label(frame_details, text="Kod IATA:").grid(row=3, column=0)
label_detail_iata_value = Label(frame_details, text="---")
label_detail_iata_value.grid(row=3, column=1)

Label(frame_details, text="Pracownicy:").grid(row=4, column=0)
label_detail_employees = Label(frame_details, text="---", justify=LEFT)
label_detail_employees.grid(row=4, column=1)


map_widget = tkintermapview.TkinterMapView(frame_map, width=1200, height=400, corner_radius=0)
map_widget.grid(row=0, column=0, columnspan=2)
map_widget.set_position(52.23, 21.00)
map_widget.set_zoom(6)


Label(frame_customers, text="Klienci").grid(row=0, column=0, columnspan=2)

listbox_customers = Listbox(frame_customers, width=40, height=10)
listbox_customers.grid(row=1, column=0, columnspan=2)


def refresh_customers():
    listbox_customers.delete(0, END)
    for idx, c in enumerate(customers):
        listbox_customers.insert(idx, f"{c.first_name} {c.last_name} - {c.passport}")


def add_customer():
    name = entry_cust_name.get()
    surname = entry_cust_surname.get()
    passport = entry_cust_passport.get()
    customer = Customer(name, surname, passport)
    customers.append(customer)
    entry_cust_name.delete(0, END)
    entry_cust_surname.delete(0, END)
    entry_cust_passport.delete(0, END)
    refresh_customers()


def remove_customer():
    i = listbox_customers.index(ACTIVE)
    customers.pop(i)
    refresh_customers()


Label(frame_customers, text="Dodaj klienta:").grid(row=2, column=0, columnspan=2)
Label(frame_customers, text="Imię").grid(row=3, column=0)
entry_cust_name = Entry(frame_customers)
entry_cust_name.grid(row=3, column=1)

Label(frame_customers, text="Nazwisko").grid(row=4, column=0)
entry_cust_surname = Entry(frame_customers)
entry_cust_surname.grid(row=4, column=1)

Label(frame_customers, text="Paszport").grid(row=5, column=0)
entry_cust_passport = Entry(frame_customers)
entry_cust_passport.grid(row=5, column=1)

Button(frame_customers, text="Dodaj klienta", command=add_customer).grid(row=6, column=0, columnspan=2)
Button(frame_customers, text="Usuń klienta", command=remove_customer).grid(row=7, column=0, columnspan=2)


root.mainloop()
