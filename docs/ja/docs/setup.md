# セットアップ

## 環境

- Raspberry Pi Zero
- Raspberry Pi Camera V2
- Raspberry Pi OS Lite

## OS のセットアップ

[Raspberry Pi Imager](https://www.raspberrypi.com/software/) は Raspberry Pi OS のイメージを SD カードに簡単に書き込むことが出来るツールです。

**micro SD カードに OS イメージを書き込む手順**

1. [Raspberry Pi Imager](https://www.raspberrypi.com/software/) をインストール。
2. Raspberrry Pi Imager を起動。
3. 「Raspberry Pi OS Lite (32bit)」を OS として選択.
4. 書き込む SD カードを選択.
5. *書き込む* をクリック.

![raspi-imager](./res/raspi-imager.gif)

## `raspi-config` によるシステム設定

`raspi-config` はシステム設定を対話的に行うことが出来る CLI ツールです。 `raspi-config` は以下のコマンドで実行できます（ルート権限で実行する必要があります）:

```bash
sudo raspi-config
```

すると以下のようなインターフェースが表示されます:

![raspi-config](./res/raspi-config.png)

`obcam` を使用するためには、以下の設定が必要になります：

1. WiFi 設定
2. 「legacy camera support」を有効化

!!!note "設定後の再起動"
    `raspi-config` での設定変更の多くは再起動を要求しますので、フライトカメラモードの実行前には再起動をしておく必要があります。

### WiFi 設定

`raspi-config` インターフェース上で、

1. *System Options* を選択。
2. *Wireless LAN* を選択。
3. 国/地域を選択 (e.g. *JP Japan*)。
4. SSID を入力。
5. パスワードを入力。

!!!info "テザリング"
    スマートフォンによるテザリングは多くの場合 WiFi のアクセスポイント兼ルーターとしての良い選択の1つです。テザリングを利用する場合は、その SSID とパスワードを上記の設定時に入力してください。

### 「legacy camera support」の有効化

`raspi-config` インターフェース上で、

1. *Interface Options* を選択。
2. *Legacy Camera* を選択。
3. *Yes* を選択。
4. *OK* を選択。

!!!info "Legacy camera support"
    Raspberrry Pi OS の最新版では `libcamera` を使ったカメラインターフェースが採用されており、以前から使われていたレガシーなカメラサポートは非推奨になっています。しかし Raspberry Pi Camera の制御のために `obcam` で使用している `picamera` という Python モジュールは、このレガシーなカメラインターフェースを使用しています。それが理由で「legacy camera support」を有効化する必要があります。

## フライトカメラモードの簡単設定

この方法を用いると `obcam` のインストールおよびフライトカメラモードの有効化を同時に行うことが出来ます。この簡単設定は[リポジトリ上](https://github.com/FROM-THE-EARTH/obcam/blob/main/install.sh) `install.sh` を実行することで行えます。詳細が気になる場合は[こちらのセクション](#_7)を参照してください。

まずは `git clone` を使用してリポジトリをダウンロードします（ネットワーク環境が必要です）：

```bash
git clone https://github.com/FROM-THE-EARTH/obcam.git
```

その後、簡単設定を行うことが出来ます：

```bash
cd obcam
sudo ./install.sh
```

これで `obcam` のフライトカメラモードの有効化は完了です。次に起動されるときからフライトカメラモードでプログラムが自動実行されます。

!!!info "`git` のインストール"
    もし `git` がインストールされていなければ、以下のようにして `git` をインストール出来ます：

    ```bash
    sudo apt update
    sudo apt install git
    ```

## `obcam` モジュールのみのインストール

`obcam` は `pip` を使用してインストール出来ます。

```bash
pip install git+https://github.com/FROM-THE-EARTH/obcam.git
```

インストール後、フライトカメラプログラムを実行する `obcam` コマンドが使用可能になります。

!!!info "`pip` がインストールされていない場合"
    Raspberry Pi の最初の起動直後は `pip` がインストールされていない可能性があります。このような場合、以下の方法で `pip` をインストール出来ます。

    1. まずは `pip` をインストールするためのスクリプトをダウンロードします。以下のコマンドの実行後、`get-pip.py` というスクリプトがカレントディレクトリにダウンロードされます。
        ```bash
        wget https://bootstrap.pypa.io/get-pip.py
        ```
    2. `get-pip.py` を実行します。
        ```bash
        python get-pip.py
        ```

## フライトカメラモードの有効化

### フライトカメラモードについて

フライトカメラモードでは、フライトカメラプログラムは Raspberrry Pi の起動時に自動実行されます。フライトカメラモードを有効化は、以下の手順で行えます：

1. [ネットワークとカメラ設定](#raspi-config)
2. [`obcam` のインストール](#obcam)
3. [gileum ファイルを書く](#gileum)
4. [フライトカメラモードのみの有効化](#_6)

### gileum ファイルを書く

gileum ファイルはこのアプリケーションの設定ファイルのようなものです。`glm.py` は1つの gileum ファイルであり、フライトカメラモードの有効化前に設定しておく必要があります。`glm.py` はリポジトリ直下においてあり、ダウンロード後に上書きして利用できます。設定パラメータの詳細については[こちらのページ](./setting.md)を参照してください。ただし、設定パラメーターはダウンロード時に最適な値に設定されているため、**デバッグなどの理由がない限りパラメーターを変更する必要はありません**。

### フライトカメラモードのみの有効化

`scripts/activate_flightcam.sh` というスクリプトを使用すれば、フライトカメラモードのみを有効化できます。`scripts/activate_flihgtcam.sh` は[リポジトリ上]((https://github.com/FROM-THE-EARTH/obcam/blob/main/scripts/activate_flightcam.sh)に置いてあります。

```bash
sudo ./scripts/activate_flightcam.sh
```

## フライトカメラモードの有効化の詳細

ここではフライトカメラモードの有効化のプロセスについて説明します。そのプロセス自体はそこまで複雑ではありません。ポイントは `/etc/rc.local` を設定するという点です。 `/etc/rc.local` はシェルスクリプトであり、OS の起動時に自動実行されるスクリプトです。

`scripts/activate_flightcam.sh` というスクリプトは `/etc/rc.local` に `obcam` プログラムを実行される以下の一行を挿入します:

```
# /etc/rc.local

# Some lines ...

/usr/bin/python -m obcam /usr/local/src/obcam/glm.py
exit 0
```

上のコードからわかるように、フライトカメラモードでは `/usr/local/src/obcam/glm.py` という `scripts/activate_flightcam.sh` が実行された際にコピーされた gileum ファイルを使用して実行されます。したがって、コピー前の gileum ファイルであるダウンロードしたリポジトリ下にある `glm.py` の内容を変更しても、フライトカメラモードの実行には影響がありません。もし gileum ファイルの内容を変更してフライトカメラモードを実行したい場合は、 `/usr/local/src/obcam/glm.py` を直接修正するか、リポジトリ下にある `glm.py` を `/usr/local/src/obcam/glm.py` に再度コピーしてください。
