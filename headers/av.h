#include "library.h"

class AVMaterial: public Document {
  AVMaterial(string cTitle) {
    Title = cTitle;
  }
  private:
   string Title;
};