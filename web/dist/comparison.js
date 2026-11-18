const comparison = document.querySelector(".comparison");
const data = document.querySelector("#event-data");

if (comparison && data) {
  const events = JSON.parse(data.textContent);
  const fields = comparison.querySelectorAll("[data-value]");
  const relationships = comparison.querySelectorAll("[data-relationship]");
  const announcement = comparison.querySelector("#event-announcement");

  function showEvent(name, announce = false) {
    const event = events.find(item => item.name === name);
    if (!event) return;
    for (const field of fields) {
      const key = field.dataset.value;
      field.textContent = key === "iri" ? `ex:${event.name}` : event[key];
      if (field instanceof HTMLTimeElement) field.dateTime = event.startedAt;
    }
    for (const relationship of relationships) {
      relationship.classList.toggle("active", relationship.dataset.relationship === name);
    }
    if (announce) {
      announcement.textContent = `${name}, 시작 ${event.shortTime}, 거리 ${event.distanceKm}km, 탑승 ${event.passengers}명`;
    }
  }

  comparison.querySelector(".events").addEventListener("change", event => {
    showEvent(event.target.value, true);
  });
  showEvent(comparison.querySelector(".events input:checked").value);
}

// Make the narrower code and table scrollports operable from a keyboard.
const scrollports = document.querySelectorAll(".code pre, .table-scroll, .diagram-scroll");
function nameScrollports() {
  for (const element of scrollports) {
    if (element.scrollWidth > element.clientWidth) {
      element.tabIndex = 0;
      element.setAttribute("role", "region");
      const caption = element.previousElementSibling?.textContent || "표";
      element.setAttribute("aria-label", caption + " 가로 스크롤");
    } else {
      element.removeAttribute("tabindex");
      element.removeAttribute("role");
      element.removeAttribute("aria-label");
    }
  }
}
window.addEventListener("resize", nameScrollports, { passive: true });
document.addEventListener("toggle", event => {
  if (event.target.matches(".example-code")) nameScrollports();
}, true);
nameScrollports();

const parts = [...document.querySelectorAll(".part")];
const stages = [...document.querySelectorAll(".stage")];
const contentsLinks = document.querySelectorAll(".contents a");
const stageLinks = document.querySelectorAll(".steps a");
const variants = document.querySelectorAll(".variants a");
const outline = document.querySelector(".workbench .focus-note");
const stageStarts = ["", "#section-1", "#section-2", "#section-8", "#section-12"];

function currentItem(elements, offset) {
  return elements.findLast(element => element.getBoundingClientRect().top <= offset);
}

function setCurrent(links, hash) {
  for (const link of links) {
    if (link.hash === hash) link.setAttribute("aria-current", "location");
    else link.removeAttribute("aria-current");
  }
}

let scheduled = false;
function syncPosition() {
  scheduled = false;
  const readingLine = Math.min(innerHeight * 0.28, 220);
  const sample = document.querySelector("#reading-sample");
  const part = currentItem(parts, readingLine);
  const stage = currentItem(stages, readingLine);
  let hash = part ? "#" + part.id : "";
  if (sample?.getBoundingClientRect().top <= readingLine) hash = "#reading-sample";
  if (location.hash === "#compare-events" && comparison?.getBoundingClientRect().top >= 0
      && comparison.getBoundingClientRect().top <= readingLine) hash = location.hash;

  setCurrent(contentsLinks, hash);
  setCurrent(stageLinks, hash === "#reading-sample" || !stage ? "" : "#" + stage.id);
  for (const link of variants) {
    const file = link.pathname.split("/").at(-1);
    link.href = file + hash;
  }

  if (outline && part) {
    const number = Number(part.id.split("-").at(-1));
    const model = number >= 2 && number <= 6 ? "rdf" : number === 7 ? "pg" : "";
    if (comparison.dataset.focus !== model) {
      comparison.dataset.focus = model;
      outline.textContent = {
        rdf: "본문에서 RDF 표현을 읽고 있습니다.",
        pg: "본문에서 Property Graph 표현을 읽고 있습니다.",
        "": "",
      }[model];
    }
  }
}

if (parts.length) {
  const incoming = location.hash.match(/^#step-([1-5])$/);
  if (!stages.length && incoming) location.hash = stageStarts[Number(incoming[1]) - 1];
  syncPosition();
  window.addEventListener("scroll", () => {
    if (!scheduled) {
      scheduled = true;
      requestAnimationFrame(syncPosition);
    }
  }, { passive: true });
  window.addEventListener("load", syncPosition);
  document.querySelectorAll(".small-contents a").forEach(link => {
    link.addEventListener("click", () => { link.closest("details").open = false; });
  });
}
