"""index.html（応募用）から meishi.html（名刺のQR用）を作る。

index.html は クラウドワークス・ランサーズの応募にも貼るため、メールと LINE の
友だち追加を出さない（ソースにも書かない）。名刺から来た人向けの meishi.html にだけ出す。

index.html の中の目印:
  <!--apply:start--> ... <!--apply:end-->   応募用だけに出す部分（meishi では消す）
  <!--card:1--> など                         名刺用の部分を差し込む場所（中身は下の CARD）

index.html を直したら、必ずこれを実行して meishi.html を作り直す:
  python3 build_meishi.py
"""
import re
from pathlib import Path

LINE_ADD = "https://line.me/R/ti/p/%40097rylpq"
MAIL = "alphardrenjyar@gmail.com"

CARD = {
    # LINE構築の欄の説明
    1: """          <p class="work-note">自分のポートフォリオ用に構築した LINE 公式アカウントです。友だち追加すると、ボタンを押して実際に操作しながら確かめられます。売り込みの配信はしません。</p>
""",
    # LINE構築の欄のボタン
    2: f"""          <a href="{LINE_ADD}" target="_blank" rel="noopener" class="work-link">友だち追加して操作してみる →</a>
          <a href="line-design.html" target="_blank" rel="noopener" class="work-link">設計図を見る →</a>
          <p>※ スマホの方は、このボタンからそのまま友だち追加できます。パソコンで開いた場合は QR コードが出るので、スマホの LINE で読み取ってください。</p>
""",
    # 実配信の記録：Notion の詳しい記録（✉️版＝メールあり。応募用は index 側で 💬版）
    4: """          <a href="https://app.notion.com/p/Meta-402c9f561e808166b178ec2d25994beb" target="_blank" rel="noopener" class="work-link">Meta 広告の詳しい記録を見る →</a>
          <a href="https://app.notion.com/p/Google-412c9f561e80813d8253f4c0fbc0a5f2" target="_blank" rel="noopener" class="work-link">Google 検索広告の詳しい記録を見る →</a>
""",
    # お問い合わせ欄
    3: f"""    <a href="{LINE_ADD}" class="btn btn-accent" target="_blank" rel="noopener">
      LINE で相談する<small>予約とフォーム、どちらでも</small>
    </a>
    <a href="mailto:{MAIL}" class="btn btn-accent">
      メールでお問い合わせ<small>{MAIL}</small>
    </a>
""",
}

here = Path(__file__).resolve().parent
src = (here / "index.html").read_text(encoding="utf-8")

marks = [int(n) for n in re.findall(r"<!--card:(\d+)-->", src)]
assert sorted(marks) == sorted(CARD), f"index.html の目印 {marks} と CARD {sorted(CARD)} が合わない"
assert src.count("<!--apply:start-->") == src.count("<!--apply:end-->") == len(CARD)
assert MAIL not in src and "line.me" not in src, "index.html に連絡先が入っている"

out = re.sub(r"<!--apply:start-->.*?<!--apply:end-->\n?", "", src, flags=re.S)
out = re.sub(r"<!--card:(\d+)-->\n?", lambda m: CARD[int(m.group(1))], out)
out = out.replace(
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    '<meta name="robots" content="noindex">\n'
    "<!-- このファイルは build_meishi.py が index.html から作る。直接編集しない -->",
    1,
)
assert "apply:" not in out and "card:" not in out
(here / "meishi.html").write_text(out, encoding="utf-8")
print(f"meishi.html を作成（切り替え {len(CARD)} か所）")
