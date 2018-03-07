#pragma once

#include "library.h"

using namespace std;

class Patron: public User {
  public:
	Document search_document_by_name(string name);
	void check_out_document(Document d);
	void return_document(Document d);
	void add_document(Document d);
};