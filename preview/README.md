# preview/ ─ スマホから即見るためのビルド成果物

GitHub Pages のセットアップが完了するまでの間、`raw.githack.com` 経由で
スマホから直接スライドを閲覧できるようにする目的で、ビルド済み HTML を
このフォルダにコミットしています。

## URL（スマホ用）

ランディング（最新ハッシュ・キャッシュなし版）：
```
https://raw.githack.com/kenjisakuragi/aiforpro/claude/ai-consulting-professionals-g6QwX/preview/index.html
```

Pages の自動公開が動き出したら、このフォルダは削除して構いません。
（その時点で `https://kenjisakuragi.github.io/aiforpro/` が正となる）

## 再生成

```bash
bash scripts/build-pages.sh preview
git add preview && git commit -m "Update preview"
git push
```
