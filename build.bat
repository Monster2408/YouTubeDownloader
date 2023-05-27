chcp 65001

rem buildフォルダがなければ作成
if not exist build mkdir build
rem main.pyをbuildフォルダへ移動する
copy main.py build
rem buildフォルダへ移動
cd build
rem pyinstallerでexe化
pyinstaller main.py --onefile --noconsole