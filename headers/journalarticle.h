#pragma once

#include "library.h"
#include "journal.h"

using namespace std;

class JournalArticle: public Document {
  public:	
	  JournalArticle(string, Journal);
  private:
    string Title;
    Journal PublishedJournal;
};