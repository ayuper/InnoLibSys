#include "headers\library.h"

User::User(string cName, unsigned int cID) {
	User::Name = cName;
	User::ID = cID;
}

Document::Document(string cPublisher, string cDate, vector <string> cAuthors, string cName) {
	Document::Publisher = cPublisher;
	Document::Date = cDate;
	Document::Authors = cAuthors;
	Document::Name = cName;
}

/**/