#include "headers\librarian.h"
#include "sqlite.h"

using namespace std;

void Librarian::add_document(Document d) {

}

void Librarian::add_patron(User p) {
	string squery;
	int rc;
	squery = "INSERT INTO `users` (`name`, `librarian`) VALUES ('" + p.get_name() + "', 0)";
	sqlite3_prepare(connection_handle, squery.c_str(), -1, &query, 0);
	rc = sqlite3_step(query);
}

void Librarian::delete_document(Document d) {

}

void Librarian::edit_patron(Patron p) {

}

vector <Document> Librarian::get_overdue_documents() {

}

Librarian::Librarian(const User& user) {
	
}