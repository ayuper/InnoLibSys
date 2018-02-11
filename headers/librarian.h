#pragma once

#include "library.h"
#include "patron.h"

using namespace std;

class Librarian: public User {
  public:
	void add_document(Document);
	void delete_document(Document);
	void modify_document(Document);
	vector <Document> get_overdue_documents();
	void add_patron(User);
	void delete_patron(Patron);
	void edit_patron(Patron);
	Librarian();
	Librarian(const User&);
};