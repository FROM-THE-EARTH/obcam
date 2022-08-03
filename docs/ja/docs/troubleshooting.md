# トラブルシューティング

## SD カードが壊れた場合

1. PC にその SD カードを差し込んでください。
2. [このセクション](./setup.md#os)を参考にして OS イメージの再書き込みを行ってみてください。もし書き込みが出来なかった場合は、新しい SD カードに交換する必要があります。

## カメラが検知されない場合

1. [こちらのセクション](./setup.md#legacy-camera-support)を参考にして「legacy camera support」が有効になっているかどうか確認してください。
2. カメラケーブルが正しく接続されているか確認してください。
3. これらの方法でも問題が解消されない場合、カメラもしくは Raspberrry Pi を交換する必要がある可能性があります。

## フライトカメラモードを有効化しても `obcam` が正常に実行されない場合

1. モニターとキーボードを Raspberry Pi に接続し、 `obcam` のログ出力を確認してください。
2. ターミナル上で `obcam` を実行し、反応を確認してください。
    ```bash
    sudo obcam /usr/local/src/obcam/glm.py
    ```
3. `obcam` がインストールされていない場合、 [こちらのセクション](./setup.md#_3)を参考にして `obcam` をインストールし、フライトカメラモードを有効化してください。
4. もしこの方法でも `obcam` が上手く動作しない場合、フライトカメラモードが有効化されていない場合があります。以下のコマンドでフライトカメラモードを有効化してください：
    ```bash
    sudo /usr/local/src/obcam/scripts/activate_flightcam.sh
    ```
5. 上記の操作で `/usr/local/src/obcam/glm.py` がないという出力が出た場合、フライトカメラモードが1度も有効化されたことがない可能性があります。`git clone` でダウンロードしたリポジトリ下にある `scripts/activate_flightcam.sh` を実行してください：
    ```bash
    sudo ./scripts/activate_flightcam.sh
    ```
