#pragma once
#include <string>
#include <vector>
#include "date.h"

using namespace std;

class Document {  
  public:
	Document();
	Document(string, Date, vector <string>, string, unsigned int, Date);
	Date get_date();
	Date get_due_date();
	vector <string> get_authors();
	string get_publisher();
	string get_title();
	unsigned int get_type();
	bool is_owned();
  private:
	unsigned int Type;
    string Publisher;
    Date Date;
	::Date DueDate;
	vector <string> Authors;
    string Name;
};

class User {
  public:
	User(string);
	User();
	string get_name();
	string get_password();
	void set_name(string);
private: 
    string Name;
	string Password;
};