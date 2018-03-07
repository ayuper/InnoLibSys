#include <iostream>
#include "sqlite.h"
#include "headers\library.h"
#include "headers\librarian.h"
#include <string>

using namespace std;

string login, password;

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
				cout << "Type: " << documents[i].get_type() << endl;
				cout << "Title: " << documents[i].get_title() << endl;
				cout << "Author: " << documents[i].get_authors().back() << endl;
				cout << "Date: " << documents[i].get_date().get_day() << '.' << documents[i].get_date().get_month() << '.' << documents[i].get_date().get_year() << endl;
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
			Date due_date = Date(day + 30, month, year);
			due_date = due_date.normalize_date(due_date);
			new_document = Document(publisher, date, authors, title, type, due_date);
			lb.add_document(new_document);
		}
	}
	else {
		Patron p = Patron();
		if (command == "check_out_document") {
			string title;
			cout << "Enter a title: ";
			cin >> title;
			string authors;
			cout << "Enter authors: ";
			cin >> authors;
			string publisher;
			cout << "Enter publisher: ";
			cin >> publisher;
			unsigned int year;
			cout << "Enter a year: ";
			cin >> year;
			bool best;
			cout << "Bestseller? (0 - no, 1 - yes): ";
			cin >> best;
			int type;
			cout << "Supported types: 0 - book, 1 - journal article, 2 - audio-video\n";
			cout << "Enter a type: ";
			cin >> type;
			p.check_out_document(Document(publisher, Date(year, -1, -1), vector <string>(1, authors), title, type, Date(-1, -1, -1)));
		}
	}
}

bool check_login_existence(string login) {
	int rc;
	string squery = "SELECT * FROM `users` WHERE `name` = '" + login + "'";
	sqlite3_prepare(connection_handle, squery.c_str(), -1, &query, 0);
	rc = sqlite3_step(query);
	return (rc != SQLITE_DONE);
}

int login_request(string login, string password) {
	string squery = "SELECT * FROM `users` WHERE `name` = '" + login + "' AND `password` = '" + password + "'";
	sqlite3_prepare(connection_handle, squery.c_str(), -1, &query, 0);
	int rc = sqlite3_step(query);
	return (rc != SQLITE_DONE);
}

void try_login() {
	cout << "Welcome to Innopolis University Library System.\n";
	cout << "Please, sign in using login: ";

	cin >> login;

	char *errMsg = 0;
	int rc;
	string squery;
	if (check_login_existence(login)) {
		cout << "Login does not exist. Try again\n";
	}
	else {
		cout << "Welcome back, " << login << '\n';
		cout << "Enter password: ";
		cin >> password;
		if (login_request(login, password)) {
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

int main() {
	sqlite3_open("library.db", &connection_handle);

	while (!logged_in) {
		try_login();
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