#include <iostream>
#include "sqlite3.h"
#include "headers\library.h"
#include <string>

using namespace std;

sqlite3* connection_handle;
sqlite3_stmt *query;
bool logged_in = false;
bool librarian = false;

#define COLUMN_ADMIN 1

void proceed_command(string command, bool usertype) {
	if (command == "add patron") {
		cout << "Insert patron's name: ";
		string name;
		cin >> name;
		cout << "Insert patron's password: ";
		string password;
		cin >> password;
		string squery = "INSERT INTO `users` (`name`, `password`) VALUES ('" + name + "', '" + password + "')";
		sqlite3_prepare(connection_handle, squery.c_str(), -1, &query, 0);
		int rc = sqlite3_step(query);
		if (rc == SQLITE_DONE) {
			cout << "Successfully done!";
		}
		else {
			cout << "Some problems...";
		}
	}
}

int main() {
	sqlite3_open("library.db", &connection_handle);

	string login, password;

	while (!logged_in) {
		cout << "Welcome to Innopolis University Library System.\n";
		cout << "Please, sign in using login: ";
		cin >> login;

		char *errMsg = 0;
		int rc;
		string squery = "SELECT * FROM `users` WHERE `name` = '" + login + "'";
		sqlite3_prepare(connection_handle, squery.c_str(), -1, &query, 0);
		rc = sqlite3_step(query);
		if (rc == SQLITE_DONE) {
			cout << "Login does not exist. Try again\n";
		}
		else {
			cout << "Welcome back, " << login << '\n';
			cout << "Enter password: ";
			cin >> password;
			squery = "SELECT * FROM `users` WHERE `name` = '" + login + "' AND `password` = '" + password + "'";
			sqlite3_prepare(connection_handle, squery.c_str(), -1, &query, 0);
			rc = sqlite3_step(query);
			if (rc == SQLITE_DONE) {
				cout << "Incorrect password!\n";
			}
			else {
				cout << "You has successfully logged in.\n";
				int is_librarian = sqlite3_column_int(query, COLUMN_ADMIN);
				librarian = is_librarian;
				logged_in = true;
			}
		}
		cout << endl;
	}

	string command;

	User current = User(login, 0);

	
	
	sqlite3_close(connection_handle);
	system("pause");
	return 0;
}