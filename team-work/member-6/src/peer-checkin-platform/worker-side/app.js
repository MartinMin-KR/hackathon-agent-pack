import {
  helpChoices,
  seedActivities,
  workerGroupsSeed,
  workerMemberProfiles,
  workerQueueSeed,
} from "../shared/data.js";

const groupList = document.querySelector("#group-list");
const queueList = document.querySelector("#queue-list");
const activityList = document.querySelector("#activity-list");
const signalList = document.querySelector("#signal-list");
const queueFilter = document.querySelector("#queue-filter");
const metricConversations = document.querySelector("#metric-conversations");
const metricSupport = document.querySelector("#metric-support");
const metricMembers = document.querySelector("#metric-members");
const detailGroupName = document.querySelector("#detail-group-name");
const detailGroupSummary = document.querySelector("#detail-group-summary");
const groupStatusBoard = document.querySelector("#group-status-board");
const detailMembers = document.querySelector("#detail-members");
const personName = document.querySelector("#person-name");
const personId = document.querySelector("#person-id");
const personAge = document.querySelector("#person-age");
const personPhone = document.querySelector("#person-phone");
const personArea = document.querySelector("#person-area");
const personAddress = document.querySelector("#person-address");
const personGuardian = document.querySelector("#person-guardian");
const personNote = document.querySelector("#person-note");

const queueItems = workerQueueSeed.map((item) => ({ ...item, reviewed: false }));
const activities = seedActivities.map((item) => ({ ...item }));
const groups = workerGroupsSeed.map((item) => ({ ...item }));
const profileMap = new Map(workerMemberProfiles.map((profile) => [profile.id, profile]));

let supportOnly = false;
let activeGroupId = groups[0].id;
let activeMemberId = groups[0].memberIds[0];

function getActiveGroup() {
  return groups.find((group) => group.id === activeGroupId) ?? groups[0];
}

function getProfile(memberId) {
  return profileMap.get(memberId);
}

function getQueueItemsForGroup(groupId) {
  return queueItems.filter((item) => item.groupId === groupId);
}

function getOpenSignals() {
  return queueItems.filter((item) => !item.reviewed);
}

function getSignalTone(type) {
  if (type.includes("위험")) return "danger";
  if (type.includes("미응답")) return "warn";
  return "calm";
}

function renderMetrics() {
  metricConversations.textContent = String(groups.length);
  metricSupport.textContent = String(getOpenSignals().length);
  metricMembers.textContent = String(workerMemberProfiles.length);
}

function renderSignals() {
  signalList.replaceChildren();

  getOpenSignals().slice(0, 4).forEach((item) => {
    const profile = getProfile(item.memberId);
    const signal = document.createElement("button");
    signal.type = "button";
    signal.className = `signal-card ${getSignalTone(item.type)}`;
    signal.innerHTML = `
      <div class="signal-top">
        <strong>${profile?.name ?? item.memberId}</strong>
        <span>${item.type}</span>
      </div>
      <p>${item.summary}</p>
    `;
    signal.addEventListener("click", () => {
      activeGroupId = item.groupId;
      activeMemberId = item.memberId;
      renderGroups();
      renderGroupDetail();
    });
    signalList.append(signal);
  });
}

function renderGroups() {
  groupList.replaceChildren();

  groups.forEach((group) => {
    const groupSignals = getQueueItemsForGroup(group.id).filter((item) => !item.reviewed);
    const card = document.createElement("button");
    card.type = "button";
    card.className = `group-card${group.id === activeGroupId ? " is-active" : ""}`;
    card.innerHTML = `
      <div class="group-card-top">
        <strong>${group.name}</strong>
        <span class="status-pill">${group.schedule}</span>
      </div>
      <p>${group.summary}</p>
      <div class="group-card-meta">
        <span>${group.memberIds.length}명</span>
        <span>${groupSignals.length}건 현황</span>
      </div>
    `;
    card.addEventListener("click", () => {
      activeGroupId = group.id;
      activeMemberId = group.memberIds[0];
      renderGroups();
      renderGroupDetail();
    });
    groupList.append(card);
  });
}

function renderGroupDetail() {
  const activeGroup = getActiveGroup();
  const groupSignals = getQueueItemsForGroup(activeGroup.id);

  detailGroupName.textContent = activeGroup.name;
  detailGroupSummary.textContent = `${activeGroup.summary} · 담당 ${activeGroup.worker}`;

  groupStatusBoard.replaceChildren();
  if (groupSignals.length === 0) {
    const empty = document.createElement("article");
    empty.className = "group-status-card calm";
    empty.innerHTML = `
      <strong>현재 특이 현황 없음</strong>
      <p>이 그룹은 지금 확인이 필요한 신호가 없어요.</p>
    `;
    groupStatusBoard.append(empty);
  } else {
    groupSignals.forEach((item) => {
      const profile = getProfile(item.memberId);
      const card = document.createElement("article");
      card.className = `group-status-card ${getSignalTone(item.type)}`;
      card.innerHTML = `
        <strong>${profile?.name ?? item.memberId} · ${item.type}</strong>
        <p>${item.summary}</p>
      `;
      groupStatusBoard.append(card);
    });
  }

  detailMembers.replaceChildren();
  activeGroup.memberIds.forEach((memberId) => {
    const profile = getProfile(memberId);
    if (!profile) return;
    const memberSignals = groupSignals.filter((item) => item.memberId === memberId && !item.reviewed);

    const button = document.createElement("button");
    button.type = "button";
    button.className = `detail-member-button${memberId === activeMemberId ? " is-active" : ""}`;
    button.innerHTML = `
      <div>
        <strong>${profile.name}</strong>
        <p>${profile.id} · ${profile.age}세</p>
      </div>
      <span class="detail-member-arrow">${memberSignals[0]?.type ?? "보기"}</span>
    `;
    button.addEventListener("click", () => {
      activeMemberId = memberId;
      renderGroupDetail();
    });
    detailMembers.append(button);
  });

  renderPersonDetail();
}

function renderPersonDetail() {
  const profile = getProfile(activeMemberId);
  if (!profile) return;

  personName.textContent = profile.name;
  personId.textContent = profile.id;
  personAge.textContent = `${profile.age}세`;
  personPhone.textContent = profile.phone;
  personArea.textContent = profile.area;
  personAddress.textContent = profile.addressHint;
  personGuardian.textContent = profile.guardian;
  personNote.textContent = profile.note;
}

function renderQueue() {
  const visibleItems = supportOnly
    ? queueItems.filter((item) => item.type !== helpChoices[3].workerType)
    : queueItems;

  queueList.replaceChildren();

  visibleItems.forEach((item) => {
    const card = document.createElement("article");
    card.className = `queue-card${item.reviewed ? " reviewed" : ""}`;
    const profile = getProfile(item.memberId);

    card.innerHTML = `
      <div class="queue-top">
        <div>
          <strong>${profile?.name ?? item.memberId}</strong>
          <p>${item.type}</p>
        </div>
        <span class="queue-state">${item.reviewed ? "완료" : item.state}</span>
      </div>
      <p class="queue-summary">${item.summary}</p>
      <button class="queue-action" type="button">${item.reviewed ? "검토 완료" : "검토 표시"}</button>
    `;

    card.querySelector(".queue-action").addEventListener("click", () => {
      item.reviewed = !item.reviewed;
      renderMetrics();
      renderSignals();
      renderGroups();
      renderGroupDetail();
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
renderSignals();
renderGroups();
renderGroupDetail();
renderQueue();
renderActivities();
