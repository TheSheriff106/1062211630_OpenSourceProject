import sqlite3
import pyperclip
import getpass

# Connect to the database
conn = sqlite3.connect('mpasswords.db')
c = conn.cursor()

# Create table if it does not exist
c.execute('''CREATE TABLE IF NOT EXISTS mpasswords
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             website TEXT,
             username TEXT,
             password TEXT)''')

# Function to get master password
def get_master_password():
    while True:
        master_password = getpass.getpass(prompt='\nEnter master password: ')
        confirm_password = getpass.getpass(prompt='Confirm master password: ')
        if master_password == confirm_password:
            return master_password
        else:
            print('passwords do not match. Please try again.')

# Function to add password
def add_password():
    website = input('\nEnter website name: ')
    username = input('Enter username: ')
    password = input('Enter password: ')
    c.execute('INSERT INTO mpasswords (website, username, password) VALUES (?, ?, ?)',
              (website, username, password))
    conn.commit()
    print('\nPassword added successfully.')

# Function to view all mpasswords
def view_mpasswords():
    c.execute('SELECT * FROM mpasswords')
    mpasswords = c.fetchall()
    for password in mpasswords:
        print(f'\nID: {password[0]}')
        print(f'Website: {password[1]}')
        print(f'Username: {password[2]}')
        print(f'Password: {password[3]}')
        print('')

# Function to delete password by ID
def delete_password():
    password_id = input('Enter password ID: ')
    c.execute('DELETE FROM mpasswords WHERE id = ?', (password_id,))
    conn.commit()
    print('\nPassword deleted successfully.')

# Function to copy password to clipboard by ID
def copy_password():
    password_id = input('\nEnter password ID: ')
    c.execute('SELECT password FROM mpasswords WHERE id = ?', (password_id,))
    password = c.fetchone()[0]
    pyperclip.copy(password)
    print('\nPassword copied to clipboard.')

# Main function
def main():
    master_password = get_master_password()
    while True:
            print("\n1. Store Password")
            print("2. View passwords")
            print("3. Delete Password")
            print("4. Copy Password")
            print("5. Exit")
            option = input("\nEnter your choice: ")
            if option == "1":
                add_password()
            elif option == "2":
                view_mpasswords()
            elif option == "3":
                delete_password()
            elif option == "4":
                copy_password()
            elif option == "5":
                break
            else:
                print('Invalid option. Please try again.')
    conn.close()

if __name__ == '__main__':
    main()
