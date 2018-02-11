#include "headers\book.h"

using namespace std;

void Book::create_book(string cTitle, unsigned int cEdition, unsigned int cYear) {
	Title = cTitle;
	Edition = cEdition;
	Year = cYear;
}