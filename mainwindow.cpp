#include "mainwindow.h"
#include "./ui_mainwindow.h"
#include "QPixmap"
#include <iostream>
#include <QMessageBox>
#include "secondwindow.h"
#include "daki.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    QPixmap pix("/home/twelve/CTLOSPI/img/icon.png");
    ui ->label_pic->setPixmap(pix);


}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_updatekeys_clicked()
{
    system("mv ~/test2/data.txt ~/test1/");
    QMessageBox msgBox;
    msgBox.setText("Процесс обновления ключей...\n   успешно завершился!");
    msgBox.setStandardButtons(QMessageBox::Ok);
    msgBox.setIcon(QMessageBox::Information);
    msgBox.setDefaultButton(QMessageBox::Ok);
    int res = msgBox.exec();

}



void MainWindow::on_pkgsinstall_clicked()
{
    SecondWindow window;
    window.setModal(true);
    this->close();
    window.exec();


}

void MainWindow::on_updatesystem_clicked()
{
    system("sudo pacman -Syuu");
}

void MainWindow::on_pushButton_clicked()
{
    system("sudo reflector -c ru,by,ua,pl -p https,http -l 20 --sort rate --save /etc/pacman.d/mirrorlist");
}

void MainWindow::on_nvidiaanddrivers_clicked()
{
    DaKI window;
    window.setModal(true);
    this->close();
    window.exec();
}
