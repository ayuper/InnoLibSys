#include "headers\library.h"
#include "headers\date.h"
#include <string>

using namespace std;

string document_types[3] = {
	"Book",
	"Journal Article",
	"Audio-Video"
};

User::User(string cName) {
	set_name(cName);
}

User::User() {}

void User::set_name(string cName) {
	Name = cName;
}

string User::get_name() {
	return Name;
}

Document::Document() {}

Document::Document(string cPublisher, ::Date cDate, vector <string> cAuthors, string cTitle, unsigned int cType) {
	Publisher = cPublisher;
	Date = cDate;
	Authors = cAuthors;
	Name = cTitle;
	Type = cType;
}

unsigned int Document::get_type() {
	return Type;
}

vector <string> Document::get_authors() {
	return Authors;
}

Date Document::get_date() {
	return Date;
}

string Document::get_publisher() {
	return Publisher;
}

string Document::get_title() {
	return Name;
}