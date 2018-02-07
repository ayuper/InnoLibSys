#include "library.h"
#include "patron.h"

using namespace std;

class Librarian: public User {
  public:
	void add_document(Document d);
	void delete_document(Document d);
	void modify_document(Document d);
	vector <Document> get_overdue_documents();
	void add_patron(Patron p);
	void delete_patron(Patron p);
	void edit_patron(Patron p);
};