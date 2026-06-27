import { contacts, helpChoices, seedActivities, workerQueueSeed } from "../shared/data.js";

const memberList = document.querySelector("#member-list");
const queueList = document.querySelector("#queue-list");
const activityList = document.querySelector("#activity-list");
const queueFilter = document.querySelector("#queue-filter");
const metricConversations = document.querySelector("#metric-conversations");
const metricSupport = document.querySelector("#metric-support");
const metricMembers = document.querySelector("#metric-members");

const queueItems = workerQueueSeed.map((item) => ({ ...item, reviewed: false }));
const activities = seedActivities.map((item) => ({ ...item }));
let supportOnly = false;

function computeMemberSignal(contact) {
  if (contact.status.includes("방금") || contact.status.includes("오늘")) return "대화 활발";
  if (contact.status.includes("어제")) return "최근 대화";
  return "대화 대기";
}

function renderMetrics() {
  metricConversations.textContent = String(activities.length);
  metricSupport.textContent = String(queueItems.filter((item) => !item.reviewed).length);
  metricMembers.textContent = String(contacts.length);
}

function renderMembers() {
  memberList.replaceChildren();

  contacts.forEach((contact) => {
    const card = document.createElement("article");
    card.className = "member-card";
    card.innerHTML = `
      <div class="avatar" aria-hidden="true">${contact.avatar}</div>
      <div>
        <strong>${contact.id}</strong>
        <p>${contact.safeArea} · ${contact.shared}</p>
      </div>
      <span class="status-pill">${computeMemberSignal(contact)}</span>
    `;
    memberList.append(card);
  });
}

function renderQueue() {
  const visibleItems = (supportOnly
    ? queueItems.filter((item) => item.type !== helpChoices[3].workerType)
    : queueItems);

  queueList.replaceChildren();

  visibleItems.forEach((item) => {
    const card = document.createElement("article");
    card.className = `queue-card${item.reviewed ? " reviewed" : ""}`;

    const actionLabel = item.reviewed ? "검토 완료" : "검토 표시";
    card.innerHTML = `
      <div class="queue-top">
        <div>
          <strong>${item.memberId}</strong>
          <p>${item.type}</p>
        </div>
        <span class="queue-state">${item.reviewed ? "완료" : item.state}</span>
      </div>
      <p class="queue-summary">${item.summary}</p>
      <button class="queue-action" type="button" data-queue-id="${item.id}">${actionLabel}</button>
    `;

    card.querySelector(".queue-action").addEventListener("click", () => {
      item.reviewed = !item.reviewed;
      renderMetrics();
      renderQueue();
    });

    queueList.append(card);
  });
}

function renderActivities() {
  activityList.replaceChildren();

  activities.forEach((activity) => {
    const item = document.createElement("li");
    item.className = "activity-item";
    item.innerHTML = `
      <div>
        <strong>${activity.title}</strong>
        <span>${activity.detail}</span>
      </div>
      <time>${activity.time}</time>
    `;
    activityList.append(item);
  });
}

queueFilter.addEventListener("click", () => {
  supportOnly = !supportOnly;
  queueFilter.textContent = supportOnly ? "전체 보기" : "지원 요청만";
  renderQueue();
});

renderMetrics();
renderMembers();
renderQueue();
renderActivities();
