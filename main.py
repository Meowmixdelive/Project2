from controller import *
# MainWindow and SecondaryWindow code located in controller.py

# Code for Outfront Steakhouse waiting list
def main() -> None:
    '''
    Initializes the program, brings up the gui window, and begins the application
    :return: None
    '''
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

