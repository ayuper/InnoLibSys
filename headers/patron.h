#include "library.h"

using namespace std;

class Patron: public User {
  public:
    Document search_document_by_name(string name) {
      // implementation of searching in db
    }
    void check_out_document(Document &d) {
      // implementation of checking out a book stored in library
    }
    void return_document(Document d) {
      // implementation - return a document to a library (db)
    }
};

class Faculty: public Patron {
  Faculty(unsigned int cType) {
    Type = cType;
  }
  private:
    unsigned int Type;
};