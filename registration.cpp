#include "registration.h"
#include "ui_registration.h"
#include "login.h"

registration::registration(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::registration)
{
    ui->setupUi(this);
}

registration::~registration()
{
    delete ui;
}

void registration::on_buttonBox_accepted()
{
    this->close();
    Login *wnd = new Login(this);
    wnd->show();
}
