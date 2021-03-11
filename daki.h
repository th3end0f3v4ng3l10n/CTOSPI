#ifndef DAKI_H
#define DAKI_H

#include <QDialog>

namespace Ui {
class DaKI;
}

class DaKI : public QDialog
{
    Q_OBJECT

public:
    explicit DaKI(QWidget *parent = nullptr);
    ~DaKI();

private:
    Ui::DaKI *ui;
};

#endif // DAKI_H
