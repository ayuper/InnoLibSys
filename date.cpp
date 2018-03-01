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

unsigned int Date::get_year() {
	return yy;
}

Date Date::normalize_date(Date date) {
	int dd = date.get_day();
	int mm = date.get_month();
	int yy = date.get_year();

	int months[12] = { 31, 28 + (yy % 400 == 0 || (yy % 4 == 0 && yy % 100 != 0)), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };
	int tmp = (dd / months[mm] >= 1) ? dd % months[mm]:0;
	dd %= months[mm];
	mm += tmp;
	tmp = (mm / 12 >= 1) ? mm % 12:0;
	mm %= 12;
	yy += tmp;
	return Date(dd, mm, yy);
}