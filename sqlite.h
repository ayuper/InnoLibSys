#pragma once

#include "sqlite3.h"

sqlite3* connection_handle;
sqlite3_stmt *query;

#define COLUMN_ADMIN 1

bool logged_in = false;
bool librarian = false;