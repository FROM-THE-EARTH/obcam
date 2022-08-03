# チェックリスト

## 事前準備

- [ ] [こちらのセクション](./setup.md#os)を参考にして Raspberry Pi OS Lite (32bit) のイメージが書き込まれた SD カードを3個以上準備しておきます。
- [ ] Raspberry Pi にモニターとキーボードを接続します。
- [ ] Raspberry Pi を起動します。
- [ ] キーボード設定を行います。
- [ ] [こちらのセクション](./setup.md#raspi-config)を参考にして `raspi-config` を使ったシステム設定を行います。
    - [ ] WiFi 設定
    - [ ] 「legacy camera support」の有効化
- [ ] `git` のインストールを行います。
    ```bash
    sudo apt update
    sudo apt install -y git
    ```
- [ ] `obcam` リポジトリのダウンロードを行います。
    ```bash
    git clone https://github.com/FROM-THE-EARTH/obcam.git
    cd obcam
    ```
- [ ] リポジトリ下の `glm.py` を確認し、必要があれば編集します。
    ```bash
    # Confirm the content
    less glm.py

    # Change the content
    vi glm.py
    ```
- [ ] `obcam` のインストールとフライトカメラモードの有効化を行います。
    ```bash
    sudo ./install.sh
    ```
- [ ] Raspberrry Pi を再起動します。
    ```bash
    sudo reboot
    ```
- [ ] LED の点滅を確認します（LED の点滅はフライトピンの接続待ち状態を意味します）。もし LED が点滅している場合は全ての事前準備が完了した状態です。そうでなければ、モニターとキーボードを Raspberrry Pi に接続し、プログラムのログ出力を確認してください。詳細なログ出力を行いたい場合は `/usr/local/src/obcam/glm.py` 内の `log_level` パラメータを `logging.DEBUG` に変更します：
    ```bash
    sudo vi /usr/local/src/obcam/glm.py

    # in the file
    #
    # ...
        - log_level=logging.INFO,
        + log_level=logging.DEBUG,
    ```

## 射場にて

- [ ] セットアップされた Raspberrry Pi とフライトピン用ケーブル、9V バッテリーを基板に接続します。
- [ ] ステータス LED の点滅を確認します。もしフライトピンが接続されている場合は、LED は点滅せず消灯状態になります。フライトピンが接続されているにも関わらず LED が消灯している場合は、モニターとキーボードを Raspberrry Pi  に接続してログ出力を確認してください。もしカメラの接続が検知されていなかった場合は、[こちらのセクション](./setup.md#legacy-camera-support)を参考にして「legacy camera support」を有効化するとともに、カメラ用ケーブルを再接続してください。
- [ ] プログラムが正常に起動している場合、基板をジップロックに入れます。
- [ ] 養生テープでジッパー部分を閉めます。
- [ ] もう1つのジップロックに基板を入れたジップロックを入れ、再度養生テープでジッパー部分を閉めます。
- [ ] 発泡スチロールのブロックをノーズコーンに入れます。
- [ ] カメラをノーズコーン内に入れ、養生テープで固定します。
- [ ] 基板を入れたジップロックをノーズコーンに入れます。
- [ ] カメラ基板から出ているフライトピン用ケーブルをメイン電装のフライトピン用ケーブルと接続します。
- [ ] フライトピンを接続します。
- [ ] 必要があれば[コマンド](./flightcam.md#_8)を実行します。

## 回収後

- [ ] SD カードを Raspberrry Pi から取り出し汚れをふき取ります。
- [ ] PC に SD カードを差し込みます。
- [ ] [こちらのセクション](./flightcam.md#sd)を参考にして動画ファイルとログファイルを取り出します。
- [ ] 動画とログを確認します。
