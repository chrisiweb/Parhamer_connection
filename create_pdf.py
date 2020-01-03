import sys
import os
import subprocess
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
from config import logo_path, path_programm


def create_pdf(path_file, index, maximum, typ=0):
    if sys.platform.startswith("linux"):
        pass
    else:
        msg = QtWidgets.QMessageBox()
        msg.setWindowIcon(QtGui.QIcon(logo_path))
        msg.setWindowTitle("Lade...")
        msg.setStandardButtons(QtWidgets.QMessageBox.NoButton)
        if path_file == "Teildokument" or path_file == "Schularbeit_Vorschau":
            rest = ""
        else:
            rest = " ({0}|{1})".format(index + 1, maximum)
        msg.setText("Die PDF Datei wird erstellt..." + rest)

        msg.show()
        QApplication.processEvents()
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
    if path_file == "Teildokument":
        dateiname = path_file + "_" + typ

        # save_file=os.path.join(path_programm, 'Teildokument')
        # print(dateiname)
    # elif dateiname=='Schularbeit_Vorschau':
    # 	save_file=os.path.join(path_programm, 'Teildokument')

    else:
        head, tail = os.path.split(path_file)
        save_file = head
        dateiname = tail

    # chosen_aufgabenformat=self.label_aufgabentyp.text()[-1]

    if dateiname == "Schularbeit_Vorschau" or dateiname.startswith("Teildokument"):
        if sys.platform.startswith("linux"):
            subprocess.Popen(
                'cd "{0}/Teildokument" ; latex --synctex=-1 {1}.tex ; dvips {1}.dvi ; ps2pdf -dNOSAFER {1}.ps'.format(
                    path_programm, dateiname
                ),
                shell=True,
            ).wait()
            subprocess.run(
                [
                    "xdg-open",
                    "{0}/Teildokument/{1}.pdf".format(path_programm, dateiname),
                ]
            )
        elif sys.platform.startswith("darwin"):
            subprocess.Popen(
                'cd "{0}/Teildokument" ; latex --synctex=-1 {1}.tex ; dvips {1}.dvi ; ps2pdf -dNOSAFER {1}.ps'.format(
                    path_programm, dateiname
                ),
                shell=True,
            ).wait()
            subprocess.run(
                ["open", "{0}/Teildokument/{1}.pdf".format(path_programm, dateiname),]
            )
        else:
            if os.path.isfile(
                os.path.join("C:\\", "Program Files", "SumatraPDF", "SumatraPDF.exe")
            ):
                sumatrapdf = os.path.join(
                    "C:\\", "Program Files", "SumatraPDF", "SumatraPDF.exe"
                )
            elif os.path.isfile(
                os.path.join(
                    "C:\\", "Program Files (x86)", "SumatraPDF", "SumatraPDF.exe"
                )
            ):
                sumatrapdf = os.path.join(
                    "C:\\", "Program Files (x86)", "SumatraPDF", "SumatraPDF.exe"
                )
            else:
                sumatrapdf = ""

            # print(os.path.splitdrive(path_programm)[0])
            subprocess.Popen(
                'cd "{0}/Teildokument" & latex --synctex=-1 "{1}.tex"& dvips "{1}.dvi" & ps2pdf -dNOSAFER "{1}.ps"'.format(
                    path_programm, dateiname
                ),
                cwd=os.path.splitdrive(path_programm)[0],
                shell=True,
            ).wait()
            if sumatrapdf != "":
                subprocess.Popen(
                    'cd "{0}/Teildokument" &"{1}" "{2}.pdf"'.format(
                        path_programm, sumatrapdf, dateiname
                    ),
                    cwd=os.path.splitdrive(path_programm)[0],
                    shell=True,
                ).poll()
            else:
                subprocess.Popen(
                    'cd "{0}/Teildokument" &"{1}.pdf"'.format(path_programm, dateiname),
                    cwd=os.path.splitdrive(path_programm)[0],
                    shell=True,
                ).poll()

        os.unlink("{0}/Teildokument/{1}.aux".format(path_programm, dateiname))
        os.unlink("{0}/Teildokument/{1}.log".format(path_programm, dateiname))
        os.unlink("{0}/Teildokument/{1}.dvi".format(path_programm, dateiname))
        os.unlink("{0}/Teildokument/{1}.ps".format(path_programm, dateiname))

    else:
        if sys.platform.startswith("linux"):
            subprocess.Popen(
                'cd "{0}" ; latex --synctex=-1 {1}.tex ; dvips {1}.dvi ; ps2pdf -dNOSAFER {1}.ps'.format(
                    save_file, dateiname
                ),
                shell=True,
            ).wait()
        elif sys.platform.startswith("darwin"):
            # print(dateiname)
            subprocess.Popen(
                'cd "{0}" ; latex --synctex=-1 "{1}.tex" ; dvips "{1}.dvi" ; ps2pdf -dNOSAFER "{1}.ps"'.format(
                    save_file, dateiname
                ),
                shell=True,
            ).wait()
        else:
            subprocess.Popen(
                'cd "{0}" & latex --synctex=-1 "{1}.tex"& dvips "{1}.dvi" & ps2pdf -dNOSAFER "{1}.ps"'.format(
                    save_file, dateiname
                ),
                cwd=os.path.splitdrive(path_file)[0],
                shell=True,
            ).wait()

        os.unlink("{0}/{1}.aux".format(save_file, dateiname))
        os.unlink("{0}/{1}.log".format(save_file, dateiname))
        os.unlink("{0}/{1}.dvi".format(save_file, dateiname))
        os.unlink("{0}/{1}.ps".format(save_file, dateiname))
        os.unlink("{0}/{1}.synctex".format(save_file, dateiname))

    if sys.platform.startswith("linux"):
        pass
    else:
        msg.close()

    QtWidgets.QApplication.restoreOverrideCursor()
