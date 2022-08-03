# スクリプト

リポジトリ内にはいくつかの実行可能なシェルスクリプトがあります。これらはリポジトリをダウンロードした場合に使用できます。これらのスクリプトは多くの場合、ルート権限で実行される必要があります。

## `install.sh`

`obcam` のインストールとフライトカメラモードの有効化を同時に行うスクリプトです。このスクリプトは以下に挙げる他のスクリプトを組み合わせて実行されるので、他のスクリプトを削除しないよう注意してください。このスクリプトの実行にはネットワーク環境が必要です。

```bash
sudo ./install.sh
```

## `scripts/activate_flightcam.sh`

フライトカメラモードの有効化を行うスクリプトです。

```bash
sudo scripts/activate_flightcam.sh
```

## `scripts/deactivate_flightcam.sh`

フライトカメラモードの無効化を行うスクリプトです。

```bash
sudo scripts/deactivate_flightcam.sh
```

## `scripts/install_obcam.sh`

`pip` で `obcam` モジュールをインストールするスクリプトです。このスクリプトはフライトカメラモードの有効化を行いません。このスクリプトの実行にはネットワーク環境が必要です。

```bash
sudo scripts/install_obcam.sh
```

## `scripts/install_pip.sh`

`pip` のインストールを行うスクリプトです。このスクリプトの実行にはネットワーク環境が必要です。

```bash
sudo scripts/install_pip.sh
```

## `scripts/uninstall_obcam.sh`

`pip` を使用して `obcam` をアンインストールするスクリプトです。

```bash
sudo scripts/uninstall_obcam.sh
```
