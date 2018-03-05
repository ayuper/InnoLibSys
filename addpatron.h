#ifndef ADDPATRON_H
#define ADDPATRON_H

#include <QDialog>

namespace Ui {
class addPatron;
}

class addPatron : public QDialog
{
    Q_OBJECT

public:
    explicit addPatron(QWidget *parent = 0);
    ~addPatron();

private:
    Ui::addPatron *ui;
};

#endif // ADDPATRON_H
