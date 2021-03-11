#include "daki.h"
#include "ui_daki.h"

DaKI::DaKI(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::DaKI)
{
    ui->setupUi(this);
}

DaKI::~DaKI()
{
    delete ui;
}
