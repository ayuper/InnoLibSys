#include "addpatron.h"
#include "ui_addpatron.h"

addPatron::addPatron(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::addPatron)
{
    ui->setupUi(this);
}

addPatron::~addPatron()
{
    delete ui;
}
