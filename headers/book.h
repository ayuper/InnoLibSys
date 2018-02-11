#pragma once

#include "library.h"

using namespace std;

class Book: public Document {
  public:
	  void create_book(string cTitle, unsigned int cEdition, unsigned int cYear);
  
  private:
    string Title;
    unsigned int Edition;
    unsigned int Year;
};