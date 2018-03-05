#include "login.h"
#include "ui_login.h"
#include "librariangui.h"
#include "registration.h"

Login::Login(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::Login)
{
    ui->setupUi(this);
}

Login::~Login()
{
    delete ui;
}

void Login::on_lineLogin_textChanged(const QString &arg1)
{
    ui->loginButton->setEnabled(!arg1.isEmpty());
}

void Login::on_lineReg_textChanged(const QString &arg1)
{
    ui->loginButton->setEnabled(!arg1.isEmpty());
}


void Login::on_loginButton_clicked()
{
    this->close();
    LibrarianGUI *wnd = new LibrarianGUI(this);
    wnd->show();
}

void Login::on_regButton_clicked()
{
    this->close();
    registration *wnd = new registration(this);
    wnd->show();

}
