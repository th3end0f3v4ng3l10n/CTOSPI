#include "mainwindow.h"
#include <QApplication>
#include <QLabel>
#include <iostream>
#include <QDebug>
void update_keys(){

}
void pkgsinstall(){

}
int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.setWindowIcon(QIcon(":/images/logo.png"));
    w.show();
    //QObject::connect(updatekeys, SIGNAL(clicked()), &a, SLOT());


    return a.exec();
}
