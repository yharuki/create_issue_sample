# create_github_issues.py

"""
MarkdownファイルからGitHubリポジトリ名、アクセストークン、Issue情報を読み取り、
GitHub APIを使って複数のIssueを自動作成するスクリプト。
"""

import re
import requests
import sys


def parse_markdown(md_path):
    with open(md_path, encoding='utf-8') as f:
        content = f.read()

    # リポジトリ名とトークン
    repo = re.search(r'###\s*対象リポジトリ名\s*\n([\s\S]+?)\n', content)
    token = re.search(r'###\s*GitHubへのアクセストークン\s*\n([\s\S]+?)\n', content)
    repo = repo.group(1).strip() if repo else None
    token = token.group(1).strip() if token else None

    # Issueグループの抽出
    groups = []
    group_pattern = re.compile(r'####.*?\n([\s\S]*?)(?=####|\Z)', re.MULTILINE)
    for group_block in group_pattern.findall(content):
        # タイトル
        titles_match = re.search(r'タイトル:\n([\s\S]*?)(?=\n本文:)', group_block)
        titles = [t.strip() for t in titles_match.group(1).strip().split('\n') if t.strip()] if titles_match else []
        # 本文
        body_match = re.search(r'本文:\n```([\s\S]*?)```', group_block)
        body = body_match.group(1).strip() if body_match else ''
        # ラベル
        labels_match = re.search(r'ラベル:\n([\s\S]*?)(?=\n|\Z)', group_block)
        labels = []
        if labels_match:
            for l in labels_match.group(1).strip().split('\n'):
                # カンマ区切り対応
                labels.extend([x.strip() for x in l.split(',') if x.strip()])
        if titles:
            groups.append({'titles': titles, 'body': body, 'labels': labels})
    return repo, token, groups


def create_issues(repo, token, groups):
    url = f'https://api.github.com/repos/{repo}/issues'
    headers = {'Authorization': f'token {token}'}
    for group in groups:
        for title in group['titles']:
            data = {'title': title, 'body': group['body'], 'labels': group['labels']}
            r = requests.post(url, json=data, headers=headers)
            if r.status_code == 201:
                print(f'Success: {title}')
            else:
                print(f'Failed: {title} ({r.status_code}) {r.text}')


def main():
    if len(sys.argv) < 2:
        print('Usage: python create_github_issues.py <markdown file path>')
        return
    md_path = sys.argv[1]
    repo, token, groups = parse_markdown(md_path)
    if not (repo and token and groups):
        print('Markdownファイルの情報が不足しています')
        return
    create_issues(repo, token, groups)


if __name__ == '__main__':
    main()
