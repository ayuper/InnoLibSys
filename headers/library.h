#include <string>
#include <vector>

using namespace std;

class Document {  
  public:
	Document(string cPublisher, string cDate, vector <string> cAuthors, string cName);
  private:
    string Publisher;
    string Date;
    vector <string> Authors;
    string Name;
};

class User {
  public:
	User(string cName, unsigned int cID);
  private: 
    string Name;
    unsigned int ID;
};