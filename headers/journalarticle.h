#include "library.h"
#include "journal.h"

using namespace std;

class JournalArticle: public Document {
  JournalArticle(string cTitle, Journal cPublishedJournal) {
    Title = cTitle;
    PublishedJournal = cPublishedJournal;
  }
  private:
    string Title;
    Journal PublishedJournal;
}