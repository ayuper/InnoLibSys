#include "headers\librarian.h"
#include "sqlite.h"

using namespace std;
string squery;
int rc;

void Librarian::add_document(Document d) {
	squery = "INSERT INTO `documents` (`title`, `author`, `type`) VALUES ('" + d.get_title() + "', '" + d.get_authors()[0] + "', '" + to_string(d.get_type()) + "')";
	sqlite3_prepare(connection_handle, squery.c_str(), -1, &query, 0);
	rc = sqlite3_step(query);
}

void Librarian::add_patron(User p) {
	squery = "INSERT INTO `users` (`name`, `librarian`) VALUES ('" + p.get_name() + "', 0)";
	sqlite3_prepare(connection_handle, squery.c_str(), -1, &query, 0);
	rc = sqlite3_step(query);
}

void Librarian::delete_document(Document d) {
	squery = "DELETE FROM `documents` WHERE `title` = '" + d.get_title() + "' AND `type` = '" + to_string(d.get_type()) + "'";
	sqlite3_prepare(connection_handle, squery.c_str(), -1, &query, 0);
	rc = sqlite3_step(query);
}

void Librarian::edit_patron(Patron p, Patron edited) {
	squery = "UPDATE `users` SET `name` = '" + edited.get_name() + "' WHERE `name` = '" + p.get_name() + "'";
	sqlite3_prepare(connection_handle, squery.c_str(), -1, &query, 0);
	rc = sqlite3_step(query);
}

vector <Document> Librarian::get_overdue_documents() {
	vector <Document> v;
	return v;
}

void Librarian::delete_patron(Patron p) {
	squery = "DELETE FROM `users` WHERE `name` = '" + p.get_name() + "'";
	sqlite3_prepare(connection_handle, squery.c_str(), -1, &query, 0);
	rc = sqlite3_step(query);
}

void Librarian::modify_document(Document d, Document edited) {
	squery = "UPDATE `users` SET `title` = '" + edited.get_title() + "', `type` = '" + to_string(edited.get_type()) + "', `dd_p` = '" + to_string(edited.get_date().get_day()) + "', `mm_p` = '" + to_string(edited.get_date().get_month()) + "', `yy_p` = '" + to_string(edited.get_date().get_year()) + "', `dd_d` = '" + to_string(edited.get_due_date().get_day()) + "', `mm_d` = '" + to_string(edited.get_due_date().get_month()) + "', `yy_d` = '" + to_string(edited.get_due_date().get_year()) + "', `publisher` = '" + edited.get_publisher() + "' WHERE `title` = '" + d.get_title() + "'";
	sqlite3_prepare(connection_handle, squery.c_str(), -1, &query, 0);
	rc = sqlite3_step(query);
}

Librarian::Librarian() {};