#include "adddocument.h"
#include "ui_adddocument.h"

addDocument::addDocument(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::addDocument)
{
    ui->setupUi(this);
}

addDocument::~addDocument()
{
    delete ui;
}
