#include <iostream>
#include "sqlite.h"
#include "headers\library.h"
#include "headers\librarian.h"
#include <string>

using namespace std;

void proceed_command(string command, bool usertype) {
	if (usertype) {
		Librarian lb = Librarian();
		if (command == "add_patron") {
			string name;
			cout << "Enter a name: ";
			cin >> name;
			lb.add_patron(User(name));
		}
		if (command == "delete_document") {
			string title;
			cout << "Enter a title: ";
			cin >> title;
			cout << "Enter a year: ";
			unsigned int year;
			cin >> year;
			unsigned int month;
			cout << "Enter a month: ";
			cin >> month;
			unsigned int day;
			cout << "Enter a day: ";
			cin >> day;
			string publisher;
			cout << "Enter a publisher: ";
			cin >> publisher;
		}
		if (command == "edit_patron") {
			string name;
			cout << "Enter a name: ";
			cin >> name;
		}
		if (command == "get_overdue_documents") {
			vector <Document> documents = lb.get_overdue_documents();
			for (int i = 0; i < documents.size(); i++) {
				cout << "Type: ";
			}
		}
		if (command == "add_document") {
			Document new_document;
			string title;
			cout << "Enter a title: ";
			cin >> title;
			string author;
			vector <string> authors;
			cout << "Enter author's name: ";
			cin >> author;
			authors.push_back(author);
			unsigned int type;
			cout << "Supported types: 0 - book, 1 - journal article, 2 - audio-video\n";
			cout << "Enter a type: ";
			cin >> type;
			string publisher;
			cout << "Enter a publisher: ";
			cin >> publisher;
			unsigned int year, month, day;
			cout << "Enter a year: ";
			cin >> year;
			cout << "Enter a month: ";
			cin >> month;
			cout << "Enter a day: ";
			cin >> day;
			Date date = Date(day, month, year);
			new_document = Document(publisher, date, authors, title, type);
			lb.add_document(new_document);
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

	User current = User(login);
	
	while (command != "exit") {
		cin >> command;
		proceed_command(command, librarian);
	}
	
	sqlite3_close(connection_handle);
	system("pause");
	return 0;
}