#pragma once

#include <string>
#include <vector>
#include "date.h"

class Journal {
  public:
	Journal(string, unsigned int, vector <string>, Date);
	Journal();
	Journal& operator=(const Journal&);
  private:
    string Title;
    unsigned int Issue;
    vector <string> Editors;
    Date PublicationDate;
};