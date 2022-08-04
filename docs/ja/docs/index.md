# obcam

![board](./res/board-top.png)

`obcam` は能代宇宙イベント2022に参加する FTE OB チームのフライトカメラモジュールおよびプログラムです。詳細については[こちらのサイト](https://FROM-THE-EARTH.github.io/obcam/ja/)を参照してください。

## インストール

ネットワーク設定と `git` および `pip` のインストールが済んだうえで、以下のコマンドを実行します：

```bash
python -m pip install git+https://github.com/FROM-THE-EARTH/obcam.git
```

## インストールおよびフライトカメラモードの有効化

ネットワーク設定と `git` のインストールが済んだうえで、以下のコマンドを実行します：

```bash
git clone https://github.com/FROM-THE-EARTH/obcam.git
cd obcam

# glm.py に設定値を記入した後に実行
# 設定の詳細についてはドキュメントを参照
sudo ./install.sh
```

## スクリプト

`scripts` ディレクトリ内のスクリプトは `obcam` のインストールやフライトカメラの有効化・無効化などの比較的小さな処理を行う際に便利です。詳細については[こちらのページ](https://FROM-THE-EARTH.github.io/obcam/scripts/)を参照してください。

**`scripts/install.sh`**

`obcam` のインストールとフライトカメラモードの有効化を同時に行うスクリプトです。

**`scripts/activate_flightcam.sh`**

`obcam` のフライトカメラモードを有効にするスクリプトです。フライトカメラモードでは、`obcam` のプログラムは起動時に自動的に実行されます。

**`scripts/deactivate_flightcam.sh`**

フライトカメラモードを無効化するスクリプトです。

**`scripts/extend_swap.sh`**

swap ファイルの容量を変更するスクリプトです。デフォルトでは 100MB から 2048 MB に変更します。

**`scripts/install_obcam.sh`**

`pip` を使って `obcam` をインストールするスクリプトです。スクリプト実行前に `pip` がインストールされている必要があります。

**`scripts/install_pip.sh`**

`pip` をインストールするスクリプトです。`pip` は最初の起動時にはインストールされていない可能性があるため、このスクリプトを使用して `pip` をインストールすることが出来ます。

**`scripts/uninstall_obcam.sh`**

`pip` を使用して `obcam` をアンインストールするスクリプトです。
