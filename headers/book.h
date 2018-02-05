#include "library.h"

using namespace std;

class Book: public Document {
  public:
    void create_book(string cTitle, unsigned int cEdition, unsigned int cYear) {
      Title = cTitle;
      Edition = cEdition;
      Year = cYear;
    }
  
  private:
    string Title;
    unsigned int Edition;
    unsigned int Year;
}