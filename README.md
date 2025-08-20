# TILE_CUTTER_for_RGBA
https://github.com/An-dz/tilecutter/releases/ のTileCutterの機能を再現し、透過度に対応した画像裁断アプリです。  
simutransの複数タイル建築物アドオンの画像をpak化するために分割することができます。
simutransのアドオン開発用にお使いください

## インストール方法
releaseよりTILE_CUTTER_RGBA.exeをインストールし起動してください。  
ソースコードであるTILE_CUTTER_RGBA.pyを使用しても実行できます。その場合は、python3およびnumpy,pillor,tkinterが必要です。

## 使用方法
1. TILE_CUTTER_RGBA.exeを起動します。  
2. [ファイルを選択]から、元の画像ファイルを選択します。
3. pak sizeにアドオンのpakサイズ(pakなら64、pak128/pak128.japan等なら128)を入力します。
4. 建物アドオンの画像において、もっとも下にある頂点の座標に1ずつ足した値を入力します。たとえば、(63,127)に頂点がある場合、64と128を入力します。
5. 建物の形状を入力します。東西方向のタイル数、南北方向のタイル数、高さ方向の層の数を指定します。高さを0とすると、地表タイルのみのアドオン画像とみなされ、タイル部分のみ切り取られます。

# simutrans_building_addon_maker_with_pov-ray
pov-ray (https://www.povray.org/) を使用したアドオン開発を支援するアプリです。  
pov-rayで制作したオブジェクトをsimutransの建物アドオン用に4方向に自動的に回転し配置、画像レンダー、TILE_CUTTER_for_RGBAによる裁断まで自動で行います。  
※本プログラムの使用にはpov-rayアプリケーションが必要です!

## インストール方法
1. releaseよりsimutrans_building_addon_maker_with_pov-ray.exeをインストールして下さい。  
2. https://www.povray.org/download/ よりpov-rayをダウンロードして下さい。  
3. pov-rayアプリケーションのあるフォルダにpathを通してください。  
4. simutrans_building_addon_maker_with_pov-ray.exeを起動してください。  

## 使用方法
1. pov-rayアプリケーションのあるフォルダにpathを通したことを確認してください。
2. simutrans_building_addon_maker_with_pov-ray.exeを起動します。
3. またpov-rayファイルを作成していない場合、[.povファイルを作成]からテンプレートを作成し、pov-rayオブジェクトを作成してください。  
4. [選択]からpov-rayファイルを選択します。
5. paksizeを入力します。pak64向けなら64,pak128向けなら128と入力してください。
6. 建物の形状を入力します。南向きの建物について、東西方向/南北方向/高さの順にタイル数を指定します。このとき、東西方向が南北方向より大きくなるようにしてください。
7. 積雪画像を同時に作る場合はチェックを入れてください。
8. simutransのアドオン用のdatファイルを同時に作る場合はチェックを入れてください。
9. [変換を実行]を押して、出力する統合された画像ファイルの名前を指定します。
10. 自動的にpov-rayファイルのレンダー、画像の裁断が行われます。

# 使用,改造,再配布について
改造、再配布について一切の制限はございません。
また、本アプリケーションを使用し生成したいかなる作品について、その利用および公開に関する自由は妨げられません。

# 免責事項
本プログラムおよび添付ファイルのダウンロード、インストール、起動等により発生した損失に関しましては、当方では責任を負いかねます。

使用は自己責任でお願いいたします。

# release note
2024.08.08 v0.0 TILE_CUTTER_RGBA 作成  
2024.10.23 v1.0 simutrans_building_addon_maker_with_pov-ray 作成  
2024.11.13 v1.1 Front画像自動生成機能追加  
2024.12.05 v1.2 エラー警告の修正、ディレクトリ検索システムの修正  
2024.12.06 v1.3 DATファイル出力時に画像ファイル名を相対パスに変更  
2024.12.06 v1.4 複数段の画像の生成方法を修正、pov-ray使用時のDATファイル記述を改善  
2025.08.20 v1.5 TILE_CUTTER_RGBAもDATファイル出力に対応  
2025.08.21 v2.0 TILE_CUTTER_for_RGBA_GUI リリース
