<div align="center">

![](aseets/header.svg)

## 🌦️ weather_service MCP サーバー

</div>

## 🧩 コンポーネント

### 📚 リソース

このサーバーは、シンプルなノート保存システムを実装しています：
- カスタム note:// URIスキームで個別のノートにアクセス
- 各ノートリソースには、名前、説明、text/plainのマイムタイプがあります

### 💡 プロンプト

サーバーは単一のプロンプトを提供します：
- summarize-notes：保存されている全てのノートの要約を作成
  - オプションの"style"引数で詳細レベルを制御（brief/detailed）
  - 全ての現在のノートとスタイル設定を組み合わせてプロンプトを生成

### 🛠️ ツール

サーバーは1つのツールを実装しています：
- add-note：新しいノートをサーバーに追加
  - "name"と"content"を必須の文字列引数として受け取り
  - サーバーの状態を更新し、リソースの変更をクライアントに通知


## 🚀 クイックスタート

### 📥 インストール

#### Claude Desktop

MacOSの場合: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
Windowsの場合: `%APPDATA%/Claude/claude_desktop_config.json`

<details>
  <summary>開発/未公開サーバーの設定</summary>
  ```
  "mcpServers": {
    "weather_service": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\Prj\weather_service",
        "run",
        "weather_service"
      ]
    }
  }
  ```
</details>

<details>
  <summary>公開サーバーの設定</summary>
  ```
  "mcpServers": {
    "weather_service": {
      "command": "uvx",
      "args": [
        "weather_service"
      ]
    }
  }
  ```
</details>

## 👨‍💻 開発

### 🏗️ ビルドと公開

パッケージを配布用に準備するには：

1. 依存関係を同期しロックファイルを更新：
```bash
uv sync
```

2. パッケージのディストリビューションをビルド：
```bash
uv build
```

これにより、`dist/`ディレクトリにソースとホイールのディストリビューションが作成されます。

3. PyPIに公開：
```bash
uv publish
```

注意：PyPIの認証情報は環境変数またはコマンドフラグで設定する必要があります：
- トークン：`--token`または`UV_PUBLISH_TOKEN`
- またはユーザー名/パスワード：`--username`/`UV_PUBLISH_USERNAME`と`--password`/`UV_PUBLISH_PASSWORD`

### 🔍 デバッグ

MCPサーバーはstdioを介して実行されるため、デバッグが難しい場合があります。最適なデバッグ体験のために、[MCP Inspector](https://github.com/modelcontextprotocol/inspector)の使用を強く推奨します。

[`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)を使用して、次のコマンドでMCP Inspectorを起動できます：

```bash
npx @modelcontextprotocol/inspector uv --directory C:\Prj\weather_service run weather-service
```

起動時、InspectorはブラウザでアクセスできるURLを表示し、デバッグを開始できます。
