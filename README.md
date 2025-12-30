# create_issue_sample

## 概要
MarkdownファイルからGitHubリポジトリに複数のIssueを自動作成するPythonスクリプトです。

## 使い方

### 1. 仮想環境の作成（推奨）
#### Linux/Mac
```bash
python3 -m venv .venv
source .venv/bin/activate
```
#### Windows
```bat
python -m venv .venv
.venv\Scripts\activate
```

### 2. 必要なライブラリのインストール
```bash
pip install -r requirements.txt
```

### 3. Markdownファイルの準備
`create_issues.md` のサンプル構成：

````markdown
### 対象リポジトリ名
your-username/your-repo

### GitHubへのアクセストークン
your_github_pat

### Issueグループ

#### グループ名（任意）
タイトル:
タイトル1
タイトル2

本文:
```
本文内容
```

ラベル:
label1,label2

#### ...（グループを必要なだけ繰り返し）
````

- タイトル: 各Issueのタイトル（複数行OK）
- 本文: グループ内で共通の本文（```で囲む）
- ラベル: カンマ区切りで複数指定可

### 4. スクリプトの実行
```bash
python create_github_issues.py create_issues.md
```

## 注意事項
- アクセストークンは権限に注意し、漏洩しないよう管理してください。
- ラベルは事前にGitHubリポジトリ側で作成しておくと確実です。
- 1グループ内のすべてのタイトルに、同じ本文・ラベルが適用されます。

---

何か問題があればチームで相談してください。
