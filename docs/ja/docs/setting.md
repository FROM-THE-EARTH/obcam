# 設定

## gileum ファイル

gileum ファイルはこのアプリケーションの設定ファイルです。 gileum ファイル内には1つの `OBCamGileum` オブジェクトが生成されている必要があります。デフォルトの gileum ファイルはリポジトリ下に用意されています。必要であれば、フライトカメラモードの有効化前にデフォルトの gileum ファイルを編集して、パラメーターの変更を反映させることが出来ます。

## `OBCamGileum`

このアプリケーションの設定用クラスです。以下のパラメータが指定されたオブジェクトを生成する必要があります。

### `timeout`

録画時間の長さ（秒）。

### `pin_flight`

フライトピンのピン番号（BCM）。デフォルトは `22`。

### `pin_led`

ステータス LED 用のピン番号（BCM）。デフォルトは `12`。

### `file_mov`

録画されるビデオファイルのパス。デフォルトは `None`。

### `file_log`

出力されるログファイルのパス。デフォルトは `None`。

### `parent_dir`

出力されるファイルの親ディレクトリのパス。デフォルトは `None`。もし指定されたディレクトリが存在しない場合は実行時に作成されます。

### `resolution`

録画されるビデオの解像度。デフォルトは `(1920, 1080)`。  `(1920, 1080)` は最大の解像度であるため、これ以上の値を指定することは出来ません。

### `framerate`

録画されるビデオのフレームレート（fps）。デフォルトは `30`。`30` fps が最大値であるので、これ以上の値を指定することが出来ません。

### `interval_recording`

録画時の待機時間（秒）。デフォルトは `0.1`。

### `led_blink_freq`

LED 点滅時の周波数（Hz）。デフォルトは `2.`。

### `log_level`

出力するログのログレベル。デフォルトは `logging.INFO` (`20`)。

### `check_waiting_time`

フライトピン離脱までの待機時にログを出力するかどうかの真偽値。デフォルトは `False`。

### `interval_waiting_time`

フライトピン離脱までの待機時のインターバル（秒）。デフォルトは `0.1`。このパラメータは `check_waiting_time` が `False` の場合は無効。

### `shutdown_after_recording`

録画終了後にシャットダウンするかどうかの真偽値。デフォルトは `True`。

### `interval_watching`

他スレッドでの状態監視プロセスのインターバル（秒）。デフォルトは `0.1`。

### `threshold_restart`

`RESTART` コマンドを有効にする時間の閾値（秒）。デフォルトは `5.`。`RESTART` コマンドは、録画中にフライトピンが再度接続され `threshold_restart` に設定した秒数だけ経過した場合に有効化される。

### `threshold_exit`

`EXIT` コマンドを有効にする時間の閾値（秒）。デフォルトは `2.`。`EXIT` コマンドは、録画中にフライトピンが再度接続され、 `threshold_exit` に設定した秒数が経過する前に再度抜かれ、その状態で `threshold_exit` に設定した秒数が経過した際に有効化される。

## 例

```python
import logging
from obcam import OBCamGileum

glm = OBCamGileum(
    # Make the timeout shorter for tests。
    timeout=10,

    # Change path to the movie file。
    file_mov="test。h254",

    # Change path to the log file。
    flie_log="test。log",

    # Set the parent directory of the output files。
    parent_dir="/obcam-out"

    # Make the frequency smaller。
    led_blink_freq=1。,

    # Make verbose log outputs for tests。
    log_level=logging。DEBUG,

    # Observe waiting time until the flight pin is disconnected。
    check_waiting_time=True,

    # Use the default settings。
    # To use defualt values, you don't have to give corresponding arguments。
    pin_flight=22,
    pin_led=12,
    resolution=(1920, 1080),
    framerate=30,
    interval_recording=0。1,
    interval_waiting_time=0。1,
    shutdown_after_recording=True,
    interval_watching=0。1,
    threshold_restart=5。,
    threshold_exit=2。,
)
```
