#!/usr/bin/env python3

# gtk-example.py

import signal
import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, GLib, GObject
from gi.repository import GObject as gobject
from gi.repository import Gtk as gtk
from gi.repository import Notify
import threading
import subprocess
import time
import sys
from colorama import Fore, Back, Style
import yaml
APPID = "GTK Test"
CURRDIR = os.path.dirname(os.path.abspath(__file__))
# could be PNG or SVG as well
ICON = 'ctlos.png'

INSTALL_DATA = []
def installer():
    global INSTALL_DATA
    class GUI_Controller:
        """ Этот класс управляет графическим интерфейсом """
        def __init__(self):
            # Настраиваем главное окно
            self.root = gtk.Window()
            self.root.set_title("CTLOS Package Picker")
            self.root.set_default_size(800, 600)
            self.root.set_icon_from_file(ICON)
            self.root.connect("destroy", self.destroy_cb)
            
            # Получаем модель, и присоединяем её к представлению
            self.mdl = Store.get_model()
            self.view = Display.make_view( self.mdl )
            # Добавляем наше представление на окно
            self.root.add(self.view)
            
            self.root.show_all()
            return
        def destroy_cb(self, *kw):
            """ Закрывающий callback """
            print('--------',INSTALL_DATA)
            #gtk.main_quit()
            return
        def run(self):
            """ Запускает цикл GTK """
            gtk.main()
            return
    
    class InfoModel:
        """ Модель, содержит информацию для отображения """
        def __init__(self):
            self.names = []
            """ Sets up and populates our gtk.TreeStore """
            self.tree_store = gtk.TreeStore( gobject.TYPE_STRING,
                                            gobject.TYPE_BOOLEAN )
            # Помещаем данные о людях в список
            # создаём простое дерево.
            with open('data.yaml','r') as f:
                data_yaml = yaml.safe_load(f)
                for i in data_yaml:
                    print(Fore.GREEN, i['name'], Style.RESET_ALL)
                    pkg_name = (str(i['name']))
                    print(pkg_name)
                    row1 = self.tree_store.append(None, (str([pkg_name]).strip("[']"), None))
                    self.names.append(i['name'])
                    #row1 = self.tree_store.append(None,[pkg_name])
                    for g in i['subgroups']:
                        pkgs_name = str(g['name'])
                        row2 = self.tree_store.append(row1, (str([pkgs_name]).strip("[']"), None))
                        for f in g['packages']:
                            self.tree_store.append(row2, (str([f]).strip("[']"), None))
            print(self.names)
            return
        def get_model(self):
            """ Возвращаем модель """
            if self.tree_store:
                return self.tree_store
            else:
                return None
    
    class DisplayModel:
        """ Отображает модель в представлении """
        def make_view( self, model ):
            
            
            """ Создаём представление для Tree Model """
            self.view = gtk.TreeView( model )
            # настраиваем cell renderer и позволяем
            # редактировать все ячейки.
            self.renderer = gtk.CellRendererText()
            #self.renderer.set_property( 'editable', True )
            #self.renderer.connect( 'edited', self.col0_edited_cb, model )
    
            # Настраиваем переключатели, и позволяем
            # пользователю их переключать.
            self.renderer1 = gtk.CellRendererToggle()
            self.renderer1.set_property('activatable', True)
            self.renderer1.connect( 'toggled', self.col1_toggled_cb, model )   
    
            # Подключаем column0 к отображению столбца 0 нашей модели
            # Отрисовщик будет отображать содержимое
            # первого столбца нашей модели .
            self.column0 = gtk.TreeViewColumn("Name", self.renderer, text=0)
    
            # Статус активности ячеек находится во втором столбце
            # модели. Так, когда модель говорит True, кнопка будет
            # показана активной (включенной).
            self.column1 = gtk.TreeViewColumn("Complete", self.renderer1 )
            self.column1.add_attribute( self.renderer1, "active", 1)
            self.view.append_column( self.column0 )
            self.view.append_column( self.column1 )
            return self.view
        def col0_edited_cb( self, cell, path, new_text, model ):
            """
            Вызывается при редактировании текста. Он помещает новый текст
        в модель.
            """
            print ("Change '%s' to '%s'" % (model[path][0], new_text))
            model[path][0] = new_text
            return
        def col1_toggled_cb( self, cell, path, model ):
            """
            Устанавливает статус активности для переключателя.
            """
            model[path][1] = not model[path][1]
            
            print ("Toggle '%s' to: %s" % (model[path][0], model[path][1],))
            if model[path][1] == True:
                INSTALL_DATA.append(model[path][0])
                if model[path][0] in self.names:
                    with open('data.yaml','r') as f:
                        data_yaml.safe_load(f)
                        for i in data_yaml:
                            if i['name'] == model[path][0]:
                                print(i)
                                for g in i['subgroups']:
                                    print(g['packages'])
                            
                print(INSTALL_DATA)
            elif model[path][1] == False:
                INSTALL_DATA.remove(model[path][0])
                print(INSTALL_DATA)
            return
    
    if __name__ == '__main__':
        Store = InfoModel()
        Display = DisplayModel()
        myGUI = GUI_Controller()
        myGUI.run()






def start_point():
    global INSTALL_DATA
    class Handler:
        def __init__(self):
            self.window_is_hidden = False
        
        def installer_cb(self,button):
            print('Start Install Packages')
            progress = builder.get_object('pbar1')
            #ПРОГРЕССБАР
            def update_progress(i):
                progress.pulse()
                progress.set_text(str(i))
                return False
            
            def example_target():
                string =['pacman', '-Syy']
                print('---------------------------------',INSTALL_DATA)
                for i in INSTALL_DATA:
                    string.append(i)
                    
                string.append("--noconfirm")
                string.append("--needed")
                print(string) 
                proc = subprocess.Popen(string,stdout=subprocess.PIPE)
                
                
                while True:
                    line = proc.stdout.readline()
                    print(line.decode('utf-8'))
                    if line.decode('utf-8') != '':
                        i = 'Wait, this can take some time'
                        time.sleep(0.1) # output is too quick, slow down a little :)
                        GLib.idle_add(update_progress, i)
                    else:
                        i = 'PKgs has been installed'
                        GLib.idle_add(update_progress, i)
                        break
            thread = threading.Thread(target=example_target)
            thread.daemon = True
            thread.start()
            
        #Кнопка Установки пакетов
        def button1_clicked_cb(self, button):
           
            installer()
            Gtk.main_quit()
            data()
            
        #Кнопка обновления Зеркал и ключей
        def button2_clicked_cb(self, button):
            print('Start Mirrors and keys update')
            progress = builder.get_object('pbar1')
            #ПРОГРЕССБАР
            def update_progress(i):
                progress.pulse()
                progress.set_text(str(i))
                return False
            
            def example_target():
                proc = subprocess.Popen(['pacman-key','--init','&&',
                                         'pacman-key','--populate','&&',
                                         'pacman-key --refresh-keys','&&',
                                         'pacman', '-Syy',
                                         'reflector','-c','ru,by,ua,pl','-p','https',',','http','--sort','rate','-a','12',
                                         '-l','10','--save','/etc/pacman.d/mirrorlist'],stdout=subprocess.PIPE)
                while True:
                    line = proc.stdout.readline()
                    print(line.decode('utf-8'))
                    if line.decode('utf-8') != '':
                        i = 'Wait, this can take some time'
                        time.sleep(0.1) # output is too quick, slow down a little :)
                        GLib.idle_add(update_progress, i)
                    else:
                        i = 'Mirrors and keys updated!'
                        GLib.idle_add(update_progress, i)
                        break
            thread = threading.Thread(target=example_target)
            thread.daemon = True
            thread.start()
            
            
            
        #Кнопка обновления системы
        def button3_clicked_cb(self, button):
            print('Start Update System')
            progress = builder.get_object('pbar1')
            #Gtk.main_quit()
            
            #ПРОГРЕССБАР
            def update_progress(i):
                progress.pulse()
                progress.set_text(str(i))
                return False
            
            def example_target():
                proc = subprocess.Popen(['pacman', '-Syyu', '-y'],stdout=subprocess.PIPE)
                while True:
                    line = proc.stdout.readline()
                    print(line.decode('utf-8'))
                    if line.decode('utf-8') != '':
                        i = 'Wait, this can take some time'
                        time.sleep(0.1) # output is too quick, slow down a little :)
                        GLib.idle_add(update_progress, i)
                    else:
                        i = 'System Update is Done!'
                        GLib.idle_add(update_progress, i)
                        break




            thread = threading.Thread(target=example_target)
            thread.daemon = True
            thread.start()

        def onNotify(self, *args):
            Notify.Notification.new("Notification", "Hello!", ICON).show()

        def onShowOrHide(self, *args):
            if self.window_is_hidden:
                window.show()
            else:
                window.hide()

            self.window_is_hidden = not self.window_is_hidden

        def fuck_my_program(self,*args):
            Gtk.main_quit()
            sys.exit(1)

    # Handle pressing Ctr+C properly, ignored by default
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    builder = Gtk.Builder()
    builder.add_from_file('mainwindow.glade')
    builder.connect_signals(Handler())

    window = builder.get_object('window1')
    window.set_icon_from_file(ICON)
    window.show_all()

    entry = builder.get_object('entry1')
    menu = builder.get_object('menu1')
    Notify.init(APPID)

    Gtk.main()
start_point()

