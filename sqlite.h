#pragma once

#include "sqlite3.h"

static sqlite3* connection_handle;
static sqlite3_stmt *query;

#define COLUMN_ADMIN 1

static bool logged_in = false;
static bool librarian = false;