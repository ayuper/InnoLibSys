#ifndef ADDDOCUMENT_H
#define ADDDOCUMENT_H

#include <QDialog>

namespace Ui {
class addDocument;
}

class addDocument : public QDialog
{
    Q_OBJECT

public:
    explicit addDocument(QWidget *parent = 0);
    ~addDocument();

private:
    Ui::addDocument *ui;
};

#endif // ADDDOCUMENT_H
