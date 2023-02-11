from GetData import GData
from ManipulateData import MData
from User import User
from App import App

# GUI | Character synopsis and relation


def main():
        
    gdata = GData('themes')

    mdata = MData(gdata)

    user = User('User', mdata)

    app = App(user)

    app.setup()

    app.start()

if __name__ == '__main__':
    main()
