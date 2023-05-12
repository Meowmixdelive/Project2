from PyQt5.QtWidgets import *
from mainGui import *
from secondaryGui import *
from datetime import *
from twilio.rest import Client

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args: object, **kwargs: object) -> None:
        '''
        Constructor to create the main window
        :param args: Connects main window to PyQt5 library
        :param kwargs: Connects main window to the gui built in mainGui.py
        '''
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.RefreshButton.clicked.connect(lambda:self.refresh())  # Allows button to refresh the screen when clicked
        self.ReservationButton.clicked.connect(lambda:self.newReserve()) # Sends code to open a new gui for reservations
        self.Reservations.currentChanged.connect(lambda:self.refresh())  # Refreshes the screen with each tab change
        # The following clears allows people on the waiting list to be sat or deleted from the list
        self.SeatButton.clicked.connect(lambda:self.clear(1))
        self.SeatButton_2.clicked.connect(lambda:self.clear(2))
        self.SeatButton_3.clicked.connect(lambda:self.clear(3))
        self.SeatButton_4.clicked.connect(lambda:self.clear(4))
        self.SeatButton_5.clicked.connect(lambda:self.clear(5))
        self.SeatButton_6.clicked.connect(lambda:self.clear(6))
        self.DeleteButton.clicked.connect(lambda:self.clear(1))
        self.DeleteButton_2.clicked.connect(lambda:self.clear(2))
        self.DeleteButton_3.clicked.connect(lambda:self.clear(3))
        self.DeleteButton_4.clicked.connect(lambda:self.clear(4))
        self.DeleteButton_5.clicked.connect(lambda:self.clear(5))
        self.DeleteButton_6.clicked.connect(lambda:self.clear(6))
        # Pages the corresponding phone number when button is clicked
        self.PageButton.clicked.connect(lambda:self.page(phoneList[0]))
        self.PageButton_2.clicked.connect(lambda:self.page(phoneList[1]))
        self.PageButton_3.clicked.connect(lambda:self.page(phoneList[2]))
        self.PageButton_4.clicked.connect(lambda:self.page(phoneList[3]))
        self.PageButton_5.clicked.connect(lambda:self.page(phoneList[4]))
        self.PageButton_6.clicked.connect(lambda:self.page(phoneList[5]))
        # The following variables are used to keep track of information relevant to the waiting list
        global nameList, numberList, phoneList, timeList, reserveList
        nameList = []
        numberList = []
        phoneList = []
        timeList = []
        reserveList = []
        # Starts with all reservation tabs invisible
        self.Reservation1.setVisible(False)
        self.Reservation2.setVisible(False)
        self.Reservation3.setVisible(False)
        self.Reservation4.setVisible(False)
        self.Reservation5.setVisible(False)
        self.Reservation6.setVisible(False)
        # Refresh turns all reservations invisible and makes the center refresh button visible
        self.refresh()

    def page(self, number: str) -> str:
        '''
        Uses twilio to send a text message to the inputted number
        :param number: Phone number paged
        :return: Unique confirmation code for page
        '''
        account_sid = 'ACc5335dbf036a775e108208e5fcf26919'
        auth_token = '19a98f099ec84766115b4873f4c1947d'
        client = Client(account_sid, auth_token)  # Uses imported twilio class
        try:
            message = client.messages.create(
                from_= '18339103134',
                body = 'Your Table at Outfront Steakhouse is Ready',
                to = number
            )
            return message.sid
        except:  # Detects an invalid number and throws an error
            dlg = QMessageBox(self)  # Sets name for dialog box
            dlg.setText("Invalid Phone Number")
            dlg.setWindowTitle("Error")
            button = dlg.exec()

    def refresh(self) -> None:
        '''
        Refreshes the main window, including refreshing reservations and the time
        :return: None
        '''
        timenow = str(datetime.now())  # Uses datetime package to get the current date and time
        self.TimeLabel.setText(f"{timenow[:19]}")  # Sets the time label to the time, cutting off microseconds
        # timeEstimate is an estimated time the next person will need to wait, it scales linearly with the wait list
        timeEstimate = 5 * len(nameList)
        self.ExpectedTimeTop.setText(f"Expected Time: {timeEstimate}-{timeEstimate+5} Minutes")
        if len(nameList) > 0:
            self.RefreshButton.setVisible(False)  # Turns on the reservation tabs
            self.Reservations.setVisible(True)
            i = len(nameList)
            first = True  # Used to eliminate old reservations
            while i > 0:  # Iterates over itself to update all reservation tabs
                if i == 6:
                    self.reserve("self.Reservation6", 6)  # Separate reservation updating function
                elif i == 5:
                    self.reserve("self.Reservation5", 5)
                    if first == True:
                        self.Reservation6.setVisible(False)  # Sets previous reservation to invisible if it was skipped
                        self.Reservations.setItemText(5, "")
                elif i == 4:
                    self.reserve("self.Reservation4", 4)
                    if first == True:
                        self.Reservation5.setVisible(False)
                        self.Reservations.setItemText(4, "")
                elif i == 3:
                    self.reserve("self.Reservation3", 3)
                    if first == True:
                        self.Reservation4.setVisible(False)
                        self.Reservations.setItemText(3, "")
                elif i == 2:
                    self.reserve("self.Reservation2", 2)
                    if first == True:
                        self.Reservation3.setVisible(False)
                        self.Reservations.setItemText(2, "")
                else:
                    self.reserve("self.Reservation1", 1)
                    if first == True:
                        self.Reservation2.setVisible(False)
                        self.Reservations.setItemText(1, "")
                i -= 1  # Used to iterate properly
                first = False
        else:
            self.RefreshButton.setVisible(True)
            self.Reservations.setVisible(False)

    def reserve(self, name: str, number: int) -> None:
        '''
        Updates reservations using global lists and values from the secondaryGui
        :param name: Name of the reservation updated (currently unused)
        :param number: Number of the reservation updated
        :return: None
        '''
        if number == 1:
            self.Reservation1.setVisible(True)
            self.Reservations.setItemText(0, nameList[0])  # Sets the name of the tab
            self.NameLabel.setText(f"Name: {nameList[0]}")
            self.PhoneNumberLabel.setText(f"Phone Number: {phoneList[0]}")
            self.PeopleNumberLabel.setText(numberList[0])
            self.TimeReservedLabel.setText(f"Time Reserved: {reserveList[0]}")
            self.ExpectedTimeBottom.setText(f"Expected Time: {timeList[0]} Minutes")
        if number == 2:
            self.Reservation2.setVisible(True)
            self.Reservations.setItemText(1, nameList[1])
            self.NameLabel_2.setText(f"Name: {nameList[1]}")
            self.PhoneNumberLabel_2.setText(f"Phone Number: {phoneList[1]}")
            self.PeopleNumberLabel_2.setText(numberList[1])
            self.TimeReservedLabel_2.setText(f"Time Reserved: {reserveList[1]}")
            self.ExpectedTimeBottom_2.setText(f"Expected Time: {timeList[1]} Minutes")
        if number == 3:
            self.Reservation3.setVisible(True)
            self.Reservations.setItemText(2, nameList[2])
            self.NameLabel_3.setText(f"Name: {nameList[2]}")
            self.PhoneNumberLabel_3.setText(f"Phone Number: {phoneList[2]}")
            self.PeopleNumberLabel_3.setText(numberList[2])
            self.TimeReservedLabel_3.setText(f"Time Reserved: {reserveList[2]}")
            self.ExpectedTimeBottom_3.setText(f"Expected Time: {timeList[2]} Minutes")
        if number == 4:
            self.Reservation4.setVisible(True)
            self.Reservations.setItemText(3, nameList[3])
            self.NameLabel_4.setText(f"Name: {nameList[3]}")
            self.PhoneNumberLabel_4.setText(f"Phone Number: {phoneList[3]}")
            self.PeopleNumberLabel_4.setText(numberList[3])
            self.TimeReservedLabel_4.setText(f"Time Reserved: {reserveList[3]}")
            self.ExpectedTimeBottom_4.setText(f"Expected Time: {timeList[3]} Minutes")
        if number == 5:
            self.Reservation5.setVisible(True)
            self.Reservations.setItemText(4, nameList[4])
            self.NameLabel_5.setText(f"Name: {nameList[4]}")
            self.PhoneNumberLabel_5.setText(f"Phone Number: {phoneList[4]}")
            self.PeopleNumberLabel_5.setText(numberList[4])
            self.TimeReservedLabel_5.setText(f"Time Reserved: {reserveList[4]}")
            self.ExpectedTimeBottom_5.setText(f"Expected Time: {timeList[4]} Minutes")
        if number == 6:
            self.Reservation6.setVisible(True)
            self.Reservations.setItemText(5, nameList[5])
            self.NameLabel_6.setText(f"Name: {nameList[5]}")
            self.PhoneNumberLabel_6.setText(f"Phone Number: {phoneList[5]}")
            self.PeopleNumberLabel_6.setText(numberList[5])
            self.TimeReservedLabel_6.setText(f"Time Reserved: {reserveList[5]}")
            self.ExpectedTimeBottom_6.setText(f"Expected Time: {timeList[5]} Minutes")

    def clear(self, number: int) -> None:
        '''
        Clears all values associated with a reservation then refreshes the page
        :param number: Number of the reservation being removed
        :return: None
        '''
        if number == 1:
            nameList.pop(0)  # Pop is used so that next reservations can move up in place
            numberList.pop(0)
            phoneList.pop(0)
            timeList.pop(0)
            reserveList.pop(0)
            self.refresh()
        if number == 2:
            nameList.pop(1)
            numberList.pop(1)
            phoneList.pop(1)
            timeList.pop(1)
            reserveList.pop(1)
            self.refresh()
        if number == 3:
            nameList.pop(2)
            numberList.pop(2)
            phoneList.pop(2)
            timeList.pop(2)
            reserveList.pop(2)
            self.refresh()
        if number == 4:
            nameList.pop(3)
            numberList.pop(3)
            phoneList.pop(3)
            timeList.pop(3)
            reserveList.pop(3)
            self.refresh()
        if number == 5:
            nameList.pop(4)
            numberList.pop(4)
            phoneList.pop(4)
            timeList.pop(4)
            reserveList.pop(4)
            self.refresh()
        if number == 6:
            nameList.pop(5)
            numberList.pop(5)
            phoneList.pop(5)
            timeList.pop(5)
            reserveList.pop(5)
            self.refresh()

    def newReserve(self) -> None:
        '''
        Opens a new gui from secondaryGui.py if reservation do not exceed 6
        :return: None
        '''
        if len(nameList) < 6:
            window = SecondWindow()  # Initializes the new gui
            window.show()
            self.refresh()
        else:
            dlg = QMessageBox(self)  # Sets name for dialog box
            dlg.setText("Too many reservations (max 6)")
            dlg.setWindowTitle("Error")
            button = dlg.exec()

class SecondWindow(QMainWindow, Ui_SecondWindow):
    def __init__(self, *args: object, **kwargs: object) -> None:
        '''
        Constructor to create the secondary window
        :param args: Connects secondary window to PyQt5 library
        :param kwargs: Connects secondary window to the gui built in secondaryGui.py
        '''
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        # Initializes variables to grab from the user
        self.name = ""
        self.number = 0
        self.phone = ""
        self.ReservationButton.clicked.connect(lambda:self.reserve())  # Grabs variables from inputs

    def reserve(self) -> None:
        '''
        Detects if inputs meet requirements, then adds a new entry in the global lists to signify a new reservation
        :return: None
        '''
        # Grabs inputs from text lines
        self.name = self.NameInput.text()
        self.phone =  self.PhoneInput.text()
        self.number = self.NumberInput.text()
        error = False  # Prevents list writing if inputs are not correct
        dlg = QMessageBox(self)     # Sets name for dialog box
        if self.name == "":  # Detects for no name
            dlg.setText("Enter Name")
            error = True
        elif self.number == "" or self.number == "0" or self.number == "00":  # Detects for no group number
            dlg.setText("Enter Group Number")
            error = True
        elif len(self.phone) != 10:  # Detects a number less than 10
            dlg.setText("Enter Valid Phone Number")
            error = True
        if error == True:
            dlg.setWindowTitle("Error")
            button = dlg.exec()  # Sends error to user
        else:
            # Writes new index in lists, then closes secondary window
            nameList.append(self.name)
            numberList.append(self.number)
            phoneList.append(self.phone)
            reserveList.append(str(datetime.now())[11:19])  # Saves just the time for use with the reservation
            timeEstimate = 5 * (len(nameList))  # Recalculates time estimate
            timeList.append(str(timeEstimate))
            self.close()  # Closes window
