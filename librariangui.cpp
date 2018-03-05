#include "librariangui.h"
#include "ui_librariangui.h"
#include "addpatron.h"
#include "adddocument.h"

LibrarianGUI::LibrarianGUI(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::LibrarianGUI)
{
    ui->setupUi(this);
}

LibrarianGUI::~LibrarianGUI()
{
    delete ui;
}

void LibrarianGUI::on_actionAdd_patron_triggered()
{
    addPatron *wnd = new addPatron(this);
    wnd->show();
}

void LibrarianGUI::on_actionAdd_document_triggered()
{
    addDocument *wnd = new addDocument(this);
    wnd->show();
}
