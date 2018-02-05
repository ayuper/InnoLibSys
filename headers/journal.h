#include <string>
#include <vector>
#include "date.h"

class Journal {
  Journal(string cTitle, unsigned int Issue, vector <string> cEditors, Date cPublicationDate) {
    Title = cTitle;
    Issue = cIssue;
    Editors = cEditors;
    PublicationDate = cPublicationDate;
  }

  private:
    string Title;
    unsigned int Issue;
    vector <string> Editors;
    Date PublicationDate;
};