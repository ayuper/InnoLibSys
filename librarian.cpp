#include "headers\librarian.h"
#include "sqlite.h"

using namespace std;
string squery;
int rc;

void Librarian::add_document(Document d) {
	squery = "INSERT INTO `library` (`title`, `author`, `type`) VALUES ('" + d.get_title() + "', '" + d.get_authors()[0] + "', '" + to_string(d.get_type()) + "')";
	sqlite3_prepare(connection_handle, squery.c_str(), -1, &query, 0);
	rc = sqlite3_step(query);
}

void Librarian::add_patron(User p) {
	squery = "INSERT INTO `users` (`name`, `librarian`) VALUES ('" + p.get_name() + "', 0)";
	sqlite3_prepare(connection_handle, squery.c_str(), -1, &query, 0);
	rc = sqlite3_step(query);
}

void Librarian::delete_document(Document d) {
	squery = "DELETE FROM `users` WHERE `title` = '" + d.get_title() + "' AND `type` = '" + to_string(d.get_type()) + "'";
	sqlite3_prepare(connection_handle, squery.c_str(), -1, &query, 0);
	rc = sqlite3_step(query);
}

void Librarian::edit_patron(Patron p) {

}

vector <Document> Librarian::get_overdue_documents() {

}

Librarian::Librarian(const User& user) {
	
}