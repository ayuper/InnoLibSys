#pragma once

#define DAY_UNDEFINED -1

using namespace std;

class Date {
public:
	Date();
	Date(unsigned int, unsigned int, unsigned int);
	unsigned int get_year();
	unsigned int get_month();
	unsigned int get_day();
	Date normalize_date(Date);
private:
	unsigned int dd;
	unsigned int mm;
	unsigned int yy;
};