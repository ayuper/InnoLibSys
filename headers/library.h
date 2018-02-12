#pragma once
#include <string>
#include <vector>
#include "date.h"

using namespace std;

class Document {  
  public:
	Document();
	Document(string, Date, vector <string>, string, unsigned int);
	Date get_date();
	vector <string> get_authors();
	string get_publisher();
	string get_title();
	unsigned int get_type();
  private:
	unsigned int Type;
    string Publisher;
    Date Date;
    vector <string> Authors;
    string Name;
};

class User {
  public:
	User(string);
	User();
	string get_name();
	void set_name(string);
private: 
    string Name;
    unsigned int ID;
};