"""Build the three offline reading screens from their shared lesson sources."""

from html import escape
import json
from os.path import relpath
from pathlib import Path
import re

from markdown_it import MarkdownIt


HERE = Path(__file__).resolve().parent
UNITS = HERE.parents[1] / "learning-v2" / "units"
LESSON = UNITS / "U04/02-events-and-property-graphs.md"
INTRO_LESSON = UNITS / "U04/01-rdf-language.md"

OPTIONS = {
    "a": ("긴 글 중심", "목차와 여백 설명을 따라 본문을 읽고, 넓은 그림에서 두 모델을 비교합니다."),
    "b": ("설명과 예제 나란히", "본문을 읽는 동안 곁에 있는 예제에서 같은 사건의 코드와 그래프를 대조합니다."),
    "c": ("문제부터 검증까지", "문제, 기록, 표현, 비교, 확인의 흐름을 따라 본문과 예제를 읽습니다."),
}
TOC = (
    "운전 기록 세 건", "RDF의 한 문장", "같은 트리플 세 줄",
    "사건에 이름 붙이기", "운전 한 건의 트리플", "세 사건을 모두 적기",
    "Property Graph의 관계", "RDB의 행", "같은 질문과 결과",
    "같은 그래프의 두 표기", "반도체 작업으로 옮기기", "이해 확인",
)
STEPS = ("문제", "기록", "표현", "비교", "확인")

markdown = MarkdownIt("commonmark", {"html": False}).enable("table")
table_open = markdown.renderer.rules.get("table_open")
table_close = markdown.renderer.rules.get("table_close")
fence = markdown.renderer.rules["fence"]


def render_table_open(tokens, idx, options, env):
    table = (
        table_open(tokens, idx, options, env) if table_open
        else markdown.renderer.renderToken(tokens, idx, options, env)
    )
    return '<div class="table-scroll">' + table


def render_table_close(tokens, idx, options, env):
    table = (
        table_close(tokens, idx, options, env) if table_close
        else markdown.renderer.renderToken(tokens, idx, options, env)
    )
    return table + "</div>\n"


def render_fence(tokens, idx, options, env):
    kind = tokens[idx].info or "text"
    return (
        '<figure class="code">'
        f'<figcaption>{escape(kind.upper() if kind != "text" else "텍스트")}</figcaption>'
        f'{fence(tokens, idx, options, env)}</figure>\n'
    )


def source_link(path):
    return Path(relpath(path, HERE)).as_posix()


def render_link_open(tokens, idx, options, env):
    token = tokens[idx]
    target = token.attrGet("href")
    if target and target.split("#", 1)[0].endswith(".md") and ":" not in target:
        filename, separator, fragment = target.partition("#")
        token.attrSet("href", source_link(env["source"].parent / filename) + separator + fragment)
    return markdown.renderer.renderToken(tokens, idx, options, env)


markdown.renderer.rules.update(
    table_open=render_table_open, table_close=render_table_close,
    fence=render_fence, link_open=render_link_open,
)


def read_lesson(path):
    title, lead = path.read_text(encoding="utf-8").strip().split("\n", 1)
    lead, *sections = re.split(r"(?m)^## ", lead)
    return title.removeprefix("# "), lead.strip(), sections


def events_from_turtle(source):
    """Use the expanded lesson code as the source of the illustrated events."""
    sample = max(re.findall(r"~~~turtle\n(.*?)\n~~~", source, re.S), key=len)
    events = []
    for match in re.finditer(
        r'^ex:(drive\d+) rdf:type ex:Drive \.\n'
        r'ex:\1 ex:driver ex:Minsu \.\n'
        r'ex:\1 ex:vehicle ex:CarA \.\n'
        r'ex:\1 ex:startedAt "([^"]+)"\^\^xsd:dateTime \.\n'
        r'ex:\1 ex:distanceKm "(\d+)"\^\^xsd:integer \.\n'
        r'ex:\1 ex:passengers "(\d+)"\^\^xsd:integer \.$',
        sample,
        re.M,
    ):
        name, started_at, distance, passengers = match.groups()
        events.append({
            "name": name,
            "startedAt": started_at,
            "shortTime": f"{started_at[5:10].replace('-', '/')} {started_at[11:16]}",
            "distanceKm": int(distance),
            "passengers": int(passengers),
            "triples": match[0],
        })
    if len(events) != 3:
        raise ValueError("The comparison expects three six-triple drive events.")
    return events


def graph_node(x, y, w, label, *, role="", key=""):
    data_key = f' data-value="{key}"' if key else ""
    return (
        f'<g class="node {role}"><rect x="{x}" y="{y}" width="{w}" height="30" rx="7"/>'
        f'<text x="{x + w / 2}" y="{y + 19}"{data_key}>{label}</text></g>'
    )


def rdf_graph(event):
    paths = []
    for i, (left, right) in enumerate(zip(
        ("rdf:type", "driver", "vehicle"),
        ("startedAt", "distanceKm", "passengers"),
    )):
        y = 29 + i * 52
        origin = 74 + i * 7
        paths.append(
            f'<path class="triple" d="M202 {origin} C164 {origin} 157 {y} 116 {y}"/>'
            f'<text class="edge-label" x="162" y="{(origin + y) / 2 - 7}">{left}</text>'
            f'<path class="triple" d="M298 {origin} C337 {origin} 346 {y} 385 {y}"/>'
            f'<text class="edge-label" x="345" y="{(origin + y) / 2 - 7}">{right}</text>'
        )
    return (
        '<svg class="diagram rdf" viewBox="0 0 500 164" role="img" aria-labelledby="rdf-title">'
        '<title id="rdf-title">선택한 운전 사건에서 나가는 RDF 트리플 여섯 개</title>'
        '<defs><marker id="rdf-tip" viewBox="0 0 8 8" refX="7" refY="4" '
        'markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L8 4 L0 8 Z"/></marker></defs>'
        + "".join(paths)
        + graph_node(8, 14, 105, "ex:Drive")
        + graph_node(8, 66, 105, "ex:Minsu")
        + graph_node(8, 118, 105, "ex:CarA")
        + graph_node(202, 66, 96, f'ex:{event["name"]}', role="selected", key="iri")
        + graph_node(389, 14, 105, event["shortTime"], role="literal", key="shortTime")
        + graph_node(389, 66, 105, str(event["distanceKm"]), role="literal", key="distanceKm")
        + graph_node(389, 118, 105, str(event["passengers"]), role="literal", key="passengers")
        + "</svg>"
    )


def property_graph(events):
    curves = (
        "M119 56 C166 0 334 0 377 56",
        "M119 65 H377",
        "M119 74 C166 130 334 130 377 74",
    )
    edges = "".join(
        f'<g class="relationship{" active" if i == 0 else ""}" data-relationship="{event["name"]}">'
        f'<path d="{curves[i]}"/>'
        f'<text class="edge-label" x="249" y="{13 + 48 * i}">:DROVE · {event["name"]}</text></g>'
        for i, event in enumerate(events)
    )
    return (
        '<svg class="diagram pg" viewBox="0 0 500 127" role="img" aria-labelledby="pg-title">'
        '<title id="pg-title">민수에서 CarA로 향하는 서로 다른 운전 관계 세 개</title>'
        '<defs><marker id="pg-tip" viewBox="0 0 8 8" refX="7" refY="4" '
        'markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L8 4 L0 8 Z"/></marker>'
        '<marker id="pg-tip-selected" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5" '
        'markerHeight="5" orient="auto"><path d="M0 0 L8 4 L0 8 Z"/></marker></defs>'
        + edges
        + graph_node(8, 50, 109, "민수 · Person")
        + graph_node(381, 50, 113, "CarA · Car")
        + "</svg>"
    )


def comparison(events):
    event = events[0]
    choices = "".join(
        f'<label><input type="radio" name="event" value="{item["name"]}"'
        f'{" checked" if i == 0 else ""}><span>{item["name"]}</span></label>'
        for i, item in enumerate(events)
    )
    return f"""<section class="comparison" id="compare-events" aria-labelledby="compare-title">
  <header class="comparison-head">
    <h2 id="compare-title">같은 운전, 다른 그래프</h2>
    <p>운전 기록을 선택하고 같은 사건이 어디에 있는지 확인해 보세요.</p>
  </header>
  <fieldset class="events"><legend class="sr-only">운전 기록 선택</legend>{choices}</fieldset>
  <p class="focus-note" aria-hidden="true"></p>
  <p class="diagram-scroll-note">그림을 좌우로 밀어 양쪽 끝을 볼 수 있습니다.</p>
  <div class="paired-graphs">
    <figure class="graph-panel rdf-panel">
      <figcaption><strong>RDF</strong> 사건과 트리플</figcaption>
      <div class="diagram-scroll">{rdf_graph(event)}</div>
      <p>사건 <code data-value="iri">ex:{event["name"]}</code>에서 트리플 여섯 개가 나갑니다. 점선 칸은 리터럴 값입니다. 화살표의 <code>ex:</code>는 생략했습니다.</p>
    </figure>
    <figure class="graph-panel pg-panel">
      <figcaption><strong>Property Graph</strong> 두 노드 사이의 관계</figcaption>
      <div class="diagram-scroll">{property_graph(events)}</div>
      <p>강조된 <code>DROVE</code> 관계에 속성이 붙습니다. <code>drive1</code> 등은 그림에서 사용하는 기록 이름입니다.</p>
    </figure>
  </div>
  <div class="event-data">
    <span><code>startedAt</code> <time data-value="startedAt" datetime="{event["startedAt"]}">{event["startedAt"]}</time></span>
    <span><code>distanceKm</code> <strong data-value="distanceKm">{event["distanceKm"]}</strong> km</span>
    <span><code>passengers</code> <strong data-value="passengers">{event["passengers"]}</strong>명</span>
  </div>
  <details class="example-code">
    <summary>선택한 사건의 Turtle과 관계 속성 보기</summary>
    <div class="record-code">
      <figure class="code"><figcaption>Turtle 트리플</figcaption><pre><code data-value="triples">{escape(event["triples"])}</code></pre></figure>
      <figure class="code"><figcaption>Cypher 관계 속성</figcaption><pre><code data-value="cypher">{escape(cypher_props(event))}</code></pre></figure>
    </div>
  </details>
  <p class="sr-only" id="event-announcement" aria-live="polite"></p>
</section>"""


def cypher_props(event):
    return (
        "{\n"
        f"  startedAt: datetime('{event['startedAt']}'),\n"
        f"  distanceKm: {event['distanceKm']}, passengers: {event['passengers']}\n"
        "}"
    )


def nav(active):
    links = "".join(
        f'<a class="variant-link" href="{key}.html"'
        + (' aria-current="page"' if active == key else "")
        + f' aria-label="{key.upper()} · {label}">{key.upper()}</a>'
        for key, (label, _) in OPTIONS.items()
    )
    return f"""<a class="skip" href="#main">본문으로 건너뛰기</a>
<header class="topbar"><div class="topbar-inner">
  <a href="index.html" class="brand">Enterprise Brain 교재</a>
  <nav class="variants" aria-label="다른 읽기 화면">{links}</nav>
</div></header>"""


def page(title, active, main, event_data=""):
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)} | Enterprise Brain</title>
  <link rel="stylesheet" href="reading.css">
  <script src="reading.js" defer></script>
</head>
<body class="view-{active}">{nav(active)}
{main}
{event_data}
</body>
</html>
"""


def contents():
    links = "".join(
        f'<li><a href="#section-{i}">{label}</a></li>'
        for i, label in enumerate(TOC, 1)
    )
    links += '<li><a href="#reading-sample">이어서 읽기</a></li>'
    return f'<nav class="contents" aria-label="수업 목차"><h2>수업 목차</h2><ol>{links}</ol></nav>'


def mobile_contents():
    return '<details class="small-contents"><summary>수업 목차</summary>' + contents() + '</details>'


def lesson_parts(sections, variant):
    if len(sections) != len(TOC):
        raise ValueError("Update the prototype's contents to match the lesson sections.")
    parts = []
    for number, source in enumerate(sections, 1):
        tip = ""
        if variant == "a" and number == 4:
            tip = '<aside class="margin-note"><strong>두 이름 읽기</strong><p><code>ex:drive1</code>은 구체적인 사건을, <code>ex:Drive</code>는 사건의 종류를 가리킵니다.</p></aside>'
        parts.append(
            f'<section class="part" id="section-{number}" style="--row:{number}">'
            f'{tip}{markdown.render("## " + source, {"source": LESSON})}</section>'
        )
    return parts


def reading_sample():
    ontology = sorted((UNITS / "U05").glob("0*.md"))
    rag = sorted((UNITS / "U13").glob("0*.md"))
    sample_paths = [INTRO_LESSON, *(ontology or rag)[:1]]
    samples = []
    for path in sample_paths:
        title, lead, sections = read_lesson(path)
        excerpt = "\n## ".join(["", *sections[:3]]).strip()
        # The reading sample is subordinate to the main lesson.
        excerpt = re.sub(r"(?m)^## ", "### ", excerpt)
        content = markdown.render(lead + "\n\n" + excerpt, {"source": path})
        samples.append(
            f'<section class="sample"><small>{path.parent.name} 발췌</small>'
            f'<h2>{escape(title)}</h2>{content}'
            f'<p><a href="{source_link(path)}">이 수업의 전체 원문</a></p></section>'
        )
    return (
        '<div class="samples" id="reading-sample">'
        '<p class="sample-label">이어서 읽기</p>' + "".join(samples) + '</div>'
    )


def lesson(variant, title, lead, sections, events):
    parts = lesson_parts(sections, variant)
    head = f"""<header class="lesson-head">
  <p class="context">U04 <span>Semantic Web · W3C · RDF</span></p>
  <h1>{escape(title)}</h1>
  <div class="lesson-lead">{markdown.render(lead, {"source": LESSON})}</div>
</header>"""
    figure = comparison(events)
    samples = reading_sample()
    if variant == "a":
        body = f"""<div class="reading-a">
  <aside class="sidebar">{contents()}</aside>
  <article class="essay">{head}{mobile_contents()}
    {"".join(parts[:7])}{figure}{"".join(parts[7:])}{samples}
  </article>
</div>"""
    elif variant == "b":
        body = f"""<div class="reading-b">
  {head}{mobile_contents()}
  {"".join(parts[:5])}
  <aside class="workbench" aria-label="운전 그래프 예제">{figure}</aside>
  {"".join(parts[5:])}{samples}
</div>"""
    else:
        steps = "".join(
            f'<li><a href="#step-{i}">{label}</a></li>'
            for i, label in enumerate(STEPS, 1)
        )
        stage_content = (
            head,
            parts[0],
            "".join(parts[1:7]) + figure,
            "".join(parts[7:11]),
            parts[11],
        )
        stages = "".join(
            f'<section class="stage" id="step-{i}" aria-label="{label}">'
            f'<p class="stage-name"><span>{i}</span>{label}</p>{content}</section>'
            for i, (label, content) in enumerate(zip(STEPS, stage_content), 1)
        )
        body = f"""<nav class="steps" aria-label="학습 단계"><ol>{steps}</ol></nav>
<article class="reading-c">{stages}{samples}</article>"""
    foot = (
        '<footer class="lesson-footer"><a href="index.html">세 가지 읽기 화면 비교</a>'
        f'<a href="{source_link(LESSON)}">U04 수업 원문</a><a href="#main">본문 처음</a></footer>'
    )
    event_data = json.dumps(
        [dict(event, cypher=cypher_props(event)) for event in events], ensure_ascii=False
    )
    return page(
        f"{OPTIONS[variant][0]} | {title}",
        variant,
        f'<main id="main" class="main-reading" tabindex="-1">{body}{foot}</main>',
        f'<script id="event-data" type="application/json">{event_data}</script>',
    )


def comparison_index(title):
    cards = "".join(
        f"""<article class="choice choice-{key}">
  <a href="{key}.html" class="choice-preview" aria-label="{label} 화면 열기">
    <div class="wireframe" aria-hidden="true">
      <i class="wire-rail"></i><i class="wire-title"></i><i class="wire-text"></i><i class="wire-diagram"></i><i class="wire-end"></i>
    </div>
  </a>
  <h2><a href="{key}.html">{key.upper()} · {label}</a></h2>
  <p>{reason}</p>
</article>"""
        for key, (label, reason) in OPTIONS.items()
    )
    return page(
        "읽기 화면 비교",
        "index",
        f"""<main id="main" class="index-main" tabindex="-1">
  <header class="index-lead">
    <h1>읽기 화면 비교</h1>
    <p>같은 수업을 세 화면에서 읽고 편한 방식을 골라 보세요.</p>
    <p class="index-lesson">{escape(title)}</p>
  </header>
  <div class="choices">{cards}</div>
</main>""",
    )


def main():
    title, lead, sections = read_lesson(LESSON)
    events = events_from_turtle(LESSON.read_text(encoding="utf-8"))
    for variant in OPTIONS:
        (HERE / f"{variant}.html").write_text(
            lesson(variant, title, lead, sections, events), encoding="utf-8"
        )
    (HERE / "index.html").write_text(comparison_index(title), encoding="utf-8")


if __name__ == "__main__":
    main()
