#pragma once
#include <string>
#include <vector>
#include "date.h"
#include "patron.h"

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
	unsigned int get_ID();
	unsigned int get_type();
	bool is_owned();
	bool is_exist();
  private:
	unsigned int Type;
    string Publisher;
    Date Date;
	::Date DueDate;
	vector <string> Authors;
    string Name;
	unsigned int ID;
};

class User {
  public:
	User(string);
	User();
	string get_name();
	string get_password();
	void set_name(string);
	string get_adress();
	string get_phone_number();
	unsigned int get_ID();
	void set_adress(string);
	void set_phone_number(string);
	void set_ID(unsigned int);
	void set_password(string);
private: 
    string Name;
	string Adress;
	string PhoneNumber;
	unsigned int LibraryCardID;
	string Password;
};