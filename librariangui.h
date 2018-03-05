#ifndef LIBRARIANGUI_H
#define LIBRARIANGUI_H

#include <QMainWindow>

namespace Ui {
class LibrarianGUI;
}

class LibrarianGUI : public QMainWindow
{
    Q_OBJECT

public:
    explicit LibrarianGUI(QWidget *parent = 0);
    ~LibrarianGUI();

private slots:
    void on_actionAdd_patron_triggered();

    void on_actionAdd_document_triggered();

private:
    Ui::LibrarianGUI *ui;
};

#endif // LIBRARIANGUI_H
