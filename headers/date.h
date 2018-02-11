#pragma once

using namespace std;

class Date {
public:
	Date();
	Date(unsigned int, unsigned int, unsigned int);
	unsigned int get_year();
	unsigned int get_month();
	unsigned int get_day();
private:
	unsigned int dd;
	unsigned int mm;
	unsigned int yy;
};