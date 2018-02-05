#include <string>
#include <vector>

using namespace std;

class Document {  
  Document(string cPublisher, string cDate, vector <string> cAuthors, string cName) {
    Publisher = cPublisher;
    Date = cDate;
    Authors = cAuthors;
    Name = cName;
  }
  private:
    string Publisher;
    string Date;
    vector <string> Authors;
    string Name;
};

class User {
  User(string cName, unsigned int cID) {
    Name = cNmae;
    ID = cID;
  }
  private: 
    string Name;
    unsigned int ID;
};