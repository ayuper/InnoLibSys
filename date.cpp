#include "headers\date.h"

using namespace std;

Date::Date(unsigned int c_dd, unsigned int c_mm, unsigned int c_yy) {
	dd = c_dd;
	mm = c_mm;
	yy = c_yy;
}

Date::Date() {};

unsigned int Date::get_day() {
	return dd;
}

unsigned int Date::get_month() {
	return mm;
}

unsigned int Date::get_day() {
	return dd;
}