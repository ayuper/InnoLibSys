#include "headers\journal.h"
#include "headers\date.h"

using namespace std;

Journal::Journal(string cTitle, unsigned int cIssue, vector <string> cEditors, Date cPublicationDate) {
	Title = cTitle;
	Issue = cIssue;
	Editors = cEditors;
	PublicationDate = cPublicationDate;
}

Journal::Journal() {}