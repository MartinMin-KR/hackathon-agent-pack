const views = ["direct", "network", "group", "help"];

const privateQuickMessages = [
  "약은 챙기셨어요?",
  "오늘 컨디션은 어떠세요?",
  "식사는 하셨어요?",
];

const groupQuickMessages = [
  "오늘 다들 어떠세요?",
  "식사 챙기셨어요?",
  "저도 잠깐 들렀어요",
];

const replyRecommendationSets = [
  {
    keywords: ["약", "챙기"],
    type: "약 확인 질문",
    guide: "상대가 약을 챙겼는지 물었어요. 상태를 숨기지 않고 짧게 답할 수 있어요.",
    replies: ["네, 챙겼어요", "아직이에요. 곧 챙길게요", "물어봐줘서 고마워요"],
  },
  {
    keywords: ["컨디션", "몸", "기분"],
    type: "컨디션 질문",
    guide: "상대가 오늘 몸 상태를 물었어요. 괜찮은지, 힘든지 편하게 고르면 돼요.",
    replies: ["괜찮아요", "조금 힘들어요", "물어봐줘서 고마워요"],
  },
  {
    keywords: ["식사", "밥", "드셨어요"],
    type: "식사 질문",
    guide: "상대가 식사를 챙겼는지 물었어요. 부담 없이 현재 상태만 답해도 돼요.",
    replies: ["네, 먹었어요", "아직이에요", "덕분에 챙겨 먹을게요"],
  },
  {
    keywords: ["잠", "주무"],
    type: "수면 질문",
    guide: "상대가 잠을 잘 잤는지 물었어요. 자세히 설명하지 않아도 짧게 답할 수 있어요.",
    replies: ["잘 잤어요", "조금 설쳤어요", "걱정해줘서 고마워요"],
  },
  {
    keywords: ["아픈", "통증", "불편"],
    type: "몸 불편 질문",
    guide: "상대가 아픈 곳이 있는지 물었어요. 의료 판단이 아니라 안부 답변만 도와줘요.",
    replies: ["괜찮아요", "조금 불편해요", "심하면 119에 연락할게요"],
  },
];

const contacts = [
  {
    id: "다정-102",
    avatar: "102",
    shared: "산책 관심",
    status: "오늘 대화 있음",
    privacy: "실명, 정확한 주소, 전화번호는 서로 보이지 않아요.",
    messages: [
      { author: "다정-102", text: "오늘 컨디션은 어떠세요?", mine: false },
      { author: "나", text: "조금 힘들지만 괜찮아요.", mine: true },
    ],
  },
  {
    id: "마음-214",
    avatar: "214",
    shared: "화분 관심",
    status: "새 안부 가능",
    privacy: "상대에게는 아이디만 보여요.",
    messages: [
      { author: "마음-214", text: "식사는 하셨어요?", mine: false },
      { author: "나", text: "물어봐줘서 고마워요.", mine: true },
    ],
  },
  {
    id: "온기-330",
    avatar: "330",
    shared: "트로트 관심",
    status: "어제 대화",
    privacy: "정확한 동호수, 연락처, 실명은 공개하지 않아요.",
    messages: [
      { author: "나", text: "오늘도 좋은 노래 들으셨어요?", mine: true },
      { author: "온기-330", text: "네, 덕분에 기분이 좋아요.", mine: false },
    ],
  },
  {
    id: "이웃-417",
    avatar: "417",
    shared: "바둑 관심",
    status: "대화 대기",
    privacy: "서로 동의하기 전에는 개인 신상을 더 열지 않아요.",
    messages: [
      { author: "이웃-417", text: "잠은 잘 주무셨어요?", mine: false },
    ],
  },
];

const helpChoices = [
  {
    label: "앱 사용이 어려워요",
    title: "앱 사용 문의",
    actions: ["문의하기"],
  },
  {
    label: "긴급 상황 안내",
    title: "긴급 상황 선택",
    actions: ["팀원이 위험해요", "도움이 필요해요"],
  },
  {
    label: "기타 문의",
    title: "기타 문의",
    actions: ["문의하기"],
  },
];

const groupMessages = [
  { author: "마음-214", text: "오늘 시장에 다녀왔어요.", mine: false },
  { author: "온기-330", text: "저녁은 따뜻하게 챙겨 드세요.", mine: false },
  { author: "나", text: "물어봐줘서 고마워요.", mine: true },
];

const activities = [
  { title: "다정-102님과 1대1 대화", detail: "오늘 컨디션은 어떠세요?", time: "방금" },
  { title: "마음-214님에게 답했어요", detail: "물어봐줘서 고마워요", time: "10분 전" },
  { title: "단체방에 글을 남겼어요", detail: "저도 잠깐 들렀어요", time: "25분 전" },
];

const actionButtons = document.querySelectorAll(".action-button");
const activityBand = document.querySelector(".activity-band");
const directListScreen = document.querySelector("#direct-list-screen");
const directChatScreen = document.querySelector("#direct-chat-screen");
const contactList = document.querySelector("#contact-list");
const networkList = document.querySelector("#network-list");
const privateChatBack = document.querySelector("#private-chat-back");
const privateChatTitle = document.querySelector("#private-chat-title");
const privateChatMeta = document.querySelector("#private-chat-meta");
const privateChatStatus = document.querySelector("#private-chat-status");
const privatePrivacyNote = document.querySelector("#private-privacy-note");
const privateChatWindow = document.querySelector("#private-chat-window");
const aiReplyList = document.querySelector("#ai-reply-list");
const privateQuickActions = document.querySelector("#private-quick-actions");
const privateChatInput = document.querySelector("#private-chat-input");
const privateChatSend = document.querySelector("#private-chat-send");
const groupChatWindow = document.querySelector("#group-chat-window");
const groupReplyList = document.querySelector("#group-reply-list");
const groupQuickActions = document.querySelector("#group-quick-actions");
const groupChatInput = document.querySelector("#group-chat-input");
const groupChatSend = document.querySelector("#group-chat-send");
const groupVoiceButton = document.querySelector("#group-voice-button");
const groupVoiceStatus = document.querySelector("#group-voice-status");
const helpListScreen = document.querySelector("#help-list-screen");
const helpDetailScreen = document.querySelector("#help-detail-screen");
const helpDetailBack = document.querySelector("#help-detail-back");
const helpDetailTitle = document.querySelector("#help-detail-title");
const helpActionList = document.querySelector("#help-action-list");
const voiceButton = document.querySelector("#voice-button");
const voiceStatus = document.querySelector("#voice-status");
const micCheck = document.querySelector("#mic-check");
const micSelect = document.querySelector("#mic-select");
const micDeviceStatus = document.querySelector("#mic-device-status");
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let activeContactId = contacts[0].id;
let isPrivateChatOpen = false;
let speechRecognition = null;
let isListening = false;
let activeVoiceTarget = "private";
let selectedMicId = "";
let activeHelpChoiceLabel = helpChoices[0].label;

function getActiveContact() {
  return contacts.find((contact) => contact.id === activeContactId) ?? contacts[0];
}

function getLastIncomingMessage(contact) {
  return [...contact.messages].reverse().find((message) => !message.mine);
}

function getLastIncomingGroupMessage() {
  return [...groupMessages].reverse().find((message) => !message.mine);
}

function getReplyRecommendation(messageText) {
  const normalizedText = messageText.replace(/\s/g, "");
  const matchedSet = replyRecommendationSets.find((set) =>
    set.keywords.some((keyword) => normalizedText.includes(keyword)),
  );

  return matchedSet ?? {
    type: "일반 안부",
    guide: "상대가 안부를 건넸어요. 따뜻하고 짧은 답을 고를 수 있어요.",
    replies: ["고마워요", "저도 반가워요", "오늘도 잘 지내보려고 해요"],
  };
}

function getGroupReplyRecommendation(messageText) {
  const normalizedText = messageText.replace(/\s/g, "");

  if (normalizedText.includes("시장") || normalizedText.includes("다녀")) {
    return ["다녀오시느라 수고하셨어요", "오늘도 조심히 다녀오셨어요?", "저도 반가워요"];
  }

  if (normalizedText.includes("저녁") || normalizedText.includes("식사") || normalizedText.includes("따뜻")) {
    return ["네, 따뜻하게 챙길게요", "다들 식사 챙기세요", "말해줘서 고마워요"];
  }

  if (normalizedText.includes("응원") || normalizedText.includes("고마")) {
    return ["고마워요", "저도 응원할게요", "덕분에 힘이 나요"];
  }

  return ["고마워요", "저도 함께할게요", "오늘도 잘 지내봐요"];
}

function setView(nextView) {
  views.forEach((view) => {
    document.querySelector(`#view-${view}`).classList.toggle("is-visible", view === nextView);
  });

  actionButtons.forEach((button) => {
    button.classList.toggle("is-active", button.dataset.view === nextView);
  });

  if (nextView === "direct") {
    showPrivateList();
  } else if (nextView === "help") {
    showHelpList();
    activityBand.hidden = true;
  } else {
    isPrivateChatOpen = false;
    activityBand.hidden = nextView === "network";
  }
}

function addActivity(title, detail) {
  activities.unshift({ title, detail, time: "방금" });
  renderActivities();
}

function renderChoices(targetId, items, onSelect) {
  const target = document.querySelector(targetId);
  target.innerHTML = "";

  items.forEach((item) => {
    const label = typeof item === "string" ? item : item.label;
    const button = document.createElement("button");
    button.className = "choice-button";
    button.type = "button";
    button.textContent = label;
    button.addEventListener("click", () => onSelect(item));
    target.appendChild(button);
  });
}

function updatePrivateFlow() {
  directListScreen.classList.toggle("is-hidden", isPrivateChatOpen);
  directChatScreen.classList.toggle("is-hidden", !isPrivateChatOpen);
  activityBand.hidden = isPrivateChatOpen;
}

function showPrivateList() {
  isPrivateChatOpen = false;
  renderContactList();
  updatePrivateFlow();
}

function getActiveHelpChoice() {
  return helpChoices.find((choice) => choice.label === activeHelpChoiceLabel) ?? helpChoices[0];
}

function updateHelpFlow(isDetailOpen) {
  helpListScreen.classList.toggle("is-hidden", isDetailOpen);
  helpDetailScreen.classList.toggle("is-hidden", !isDetailOpen);
}

function showHelpList() {
  updateHelpFlow(false);
}

function openHelpDetail(choice) {
  activeHelpChoiceLabel = choice.label;
  helpDetailTitle.textContent = choice.title;
  renderChoices("#help-action-list", choice.actions, (actionLabel) => {
    addActivity("도움 요청을 선택했어요", actionLabel);
  });
  updateHelpFlow(true);
}

function openPrivateChat(contactId) {
  activeContactId = contactId;
  isPrivateChatOpen = true;
  renderContactList();
  renderPrivateChat();
  updatePrivateFlow();
}

function renderContactList() {
  contactList.innerHTML = "";

  contacts.forEach((contact) => {
    const button = document.createElement("button");
    button.className = `contact-card${isPrivateChatOpen && contact.id === activeContactId ? " is-active" : ""}`;
    button.type = "button";
    button.innerHTML = `
      <span class="avatar" aria-hidden="true">${contact.avatar}</span>
      <span>
        <span class="contact-id">${contact.id}</span>
      </span>
      <span class="id-badge">${contact.status}</span>
    `;
    button.addEventListener("click", () => openPrivateChat(contact.id));
    contactList.appendChild(button);
  });
}

function renderNetworkList() {
  networkList.innerHTML = "";

  contacts.forEach((contact) => {
    const card = document.createElement("article");
    card.className = "network-card";
    card.innerHTML = `
      <div class="avatar" aria-hidden="true">${contact.avatar}</div>
      <div>
        <span class="contact-id">${contact.id}</span>
        <div class="contact-meta">관심사: ${contact.shared}</div>
        <p>${contact.privacy}</p>
      </div>
      <button class="network-action" type="button">1대1 대화</button>
    `;
    card.querySelector(".network-action").addEventListener("click", () => {
      setView("direct");
      openPrivateChat(contact.id);
    });
    networkList.appendChild(card);
  });
}

function renderPrivateChat() {
  const contact = getActiveContact();
  privateChatTitle.textContent = contact.id;
  privateChatMeta.textContent = "1대1 안부 대화";
  privateChatStatus.textContent = contact.status;
  privatePrivacyNote.textContent = contact.privacy;
  privateChatWindow.innerHTML = "";

  contact.messages.forEach((message) => {
    const item = document.createElement("div");
    item.className = `chat-message${message.mine ? " mine" : ""}`;
    item.innerHTML = `
      <span class="chat-author">${message.author}</span>
      <p class="chat-text">${message.text}</p>
    `;
    privateChatWindow.appendChild(item);
  });

  privateChatWindow.scrollTop = privateChatWindow.scrollHeight;
  renderAiReplySuggestions(contact);
}

function renderAiReplySuggestions(contact) {
  const lastIncomingMessage = getLastIncomingMessage(contact);
  aiReplyList.innerHTML = "";

  if (!lastIncomingMessage) {
    return;
  }

  const recommendation = getReplyRecommendation(lastIncomingMessage.text);

  recommendation.replies.forEach((reply) => {
    const button = document.createElement("button");
    button.className = "ai-reply-button";
    button.type = "button";
    button.textContent = reply;
    button.addEventListener("click", () => {
      privateChatInput.value = reply;
      privateChatInput.focus();
    });
    aiReplyList.appendChild(button);
  });
}

function sendPrivateMessage(text) {
  const cleanText = text.trim();
  if (cleanText.length === 0) {
    return;
  }

  const contact = getActiveContact();
  contact.messages.push({ author: "나", text: cleanText, mine: true });
  contact.status = "방금 대화";
  addActivity(`${contact.id}님과 1대1 대화`, cleanText);
  renderContactList();
  renderNetworkList();
  renderPrivateChat();
  privateChatInput.value = "";
}

function renderPrivateQuickActions() {
  privateQuickActions.innerHTML = "";

  privateQuickMessages.forEach((message) => {
    const button = document.createElement("button");
    button.className = "choice-button";
    button.type = "button";
    button.textContent = message;
    button.addEventListener("click", () => sendPrivateMessage(message));
    privateQuickActions.appendChild(button);
  });
}

function renderGroupChat() {
  groupChatWindow.innerHTML = "";

  groupMessages.forEach((message) => {
    const item = document.createElement("div");
    item.className = `chat-message${message.mine ? " mine" : ""}`;
    item.innerHTML = `
      <span class="chat-author">${message.author}</span>
      <p class="chat-text">${message.text}</p>
    `;
    groupChatWindow.appendChild(item);
  });

  groupChatWindow.scrollTop = groupChatWindow.scrollHeight;
  renderGroupReplySuggestions();
}

function renderGroupReplySuggestions() {
  const lastIncomingMessage = getLastIncomingGroupMessage();
  groupReplyList.innerHTML = "";

  if (!lastIncomingMessage) {
    return;
  }

  getGroupReplyRecommendation(lastIncomingMessage.text).forEach((reply) => {
    const button = document.createElement("button");
    button.className = "ai-reply-button";
    button.type = "button";
    button.textContent = reply;
    button.addEventListener("click", () => {
      groupChatInput.value = reply;
      groupChatInput.focus();
    });
    groupReplyList.appendChild(button);
  });
}

function sendGroupMessage(text) {
  const cleanText = text.trim();
  if (cleanText.length === 0) {
    return;
  }

  groupMessages.push({ author: "나", text: cleanText, mine: true });
  addActivity("단체방에 글을 남겼어요", cleanText);
  renderGroupChat();
  groupChatInput.value = "";
}

function renderGroupQuickActions() {
  groupQuickActions.innerHTML = "";

  groupQuickMessages.forEach((message) => {
    const button = document.createElement("button");
    button.className = "choice-button";
    button.type = "button";
    button.textContent = message;
    button.addEventListener("click", () => sendGroupMessage(message));
    groupQuickActions.appendChild(button);
  });
}

function getVoiceTarget(target = activeVoiceTarget) {
  if (target === "group") {
    return {
      button: groupVoiceButton,
      input: groupChatInput,
      status: groupVoiceStatus,
      successMessage: "들은 내용을 단체방 입력칸에 넣었어요. 확인 후 보내기를 눌러주세요.",
    };
  }

  return {
    button: voiceButton,
    input: privateChatInput,
    status: voiceStatus,
    successMessage: "들은 내용을 1대1 대화 입력칸에 넣었어요. 확인 후 보내기를 눌러주세요.",
  };
}

function setVoiceStatus(message, target = activeVoiceTarget) {
  getVoiceTarget(target).status.textContent = message;
}

function setVoiceListening(nextListening) {
  isListening = nextListening;

  [voiceButton, groupVoiceButton].forEach((button) => {
    const isActiveButton = nextListening && button === getVoiceTarget().button;
    button.classList.toggle("is-listening", isActiveButton);
    button.setAttribute("aria-pressed", String(isActiveButton));
    button.textContent = isActiveButton ? "듣는 중" : "음성 입력";
  });
}

function setupVoiceInput() {
  if (!SpeechRecognition) {
    [voiceButton, groupVoiceButton].forEach((button) => {
      button.disabled = true;
    });
    voiceStatus.textContent = "이 브라우저에서는 음성 입력을 지원하지 않아요. 빠른 말 버튼을 이용해 주세요.";
    groupVoiceStatus.textContent = "이 브라우저에서는 음성 입력을 지원하지 않아요. 빠른 말 버튼을 이용해 주세요.";
    return;
  }

  speechRecognition = new SpeechRecognition();
  speechRecognition.lang = "ko-KR";
  speechRecognition.interimResults = false;
  speechRecognition.maxAlternatives = 1;

  speechRecognition.addEventListener("start", () => {
    setVoiceListening(true);
    setVoiceStatus("말씀해 주세요. 듣고 있어요.");
  });

  speechRecognition.addEventListener("result", (event) => {
    const transcript = event.results?.[0]?.[0]?.transcript?.trim() ?? "";
    if (transcript.length === 0) {
      setVoiceStatus("말소리를 잘 듣지 못했어요. 다시 한 번 눌러주세요.");
      return;
    }

    const target = getVoiceTarget();
    target.input.value = transcript.slice(0, 40);
    target.status.textContent = target.successMessage;
    target.input.focus();
  });

  speechRecognition.addEventListener("error", (event) => {
    const messages = {
      "not-allowed": "마이크 권한이 필요해요. 허용하기 어렵다면 빠른 말 버튼을 이용해 주세요.",
      "no-speech": "말소리를 듣지 못했어요. 조용한 곳에서 다시 눌러주세요.",
      network: "음성 인식 연결이 불안정해요. 빠른 말 버튼을 이용해 주세요.",
    };
    setVoiceStatus(messages[event.error] ?? "음성 입력이 잠시 어려워요. 빠른 말 버튼을 이용해 주세요.");
  });

  speechRecognition.addEventListener("end", () => {
    setVoiceListening(false);
  });
}

function startVoiceInput(target) {
  if (!speechRecognition) {
    setVoiceStatus("이 브라우저에서는 음성 입력을 지원하지 않아요. 빠른 말 버튼을 이용해 주세요.", target);
    return;
  }

  if (isListening) {
    speechRecognition.stop();
    return;
  }

  activeVoiceTarget = target;

  try {
    speechRecognition.start();
  } catch {
    setVoiceStatus("이미 음성 입력을 준비하고 있어요. 잠시 뒤 다시 눌러주세요.", target);
  }
}

function setMicStatus(message) {
  micDeviceStatus.textContent = message;
}

async function populateMicrophoneList() {
  if (!navigator.mediaDevices?.enumerateDevices) {
    micSelect.disabled = true;
    setMicStatus("이 브라우저에서는 마이크 기기 목록을 확인할 수 없어요.");
    return;
  }

  const devices = await navigator.mediaDevices.enumerateDevices();
  const microphones = devices.filter((device) => device.kind === "audioinput");
  micSelect.innerHTML = "";

  if (microphones.length === 0) {
    micSelect.disabled = true;
    micSelect.innerHTML = '<option value="">연결된 마이크를 찾지 못했어요</option>';
    setMicStatus("기기에 연결된 마이크가 보이지 않아요. 기기 설정을 확인해 주세요.");
    return;
  }

  microphones.forEach((device, index) => {
    const option = document.createElement("option");
    option.value = device.deviceId;
    option.textContent = device.label || `마이크 ${index + 1}`;
    micSelect.appendChild(option);
  });

  if (selectedMicId && [...micSelect.options].some((option) => option.value === selectedMicId)) {
    micSelect.value = selectedMicId;
  } else {
    selectedMicId = micSelect.value;
  }

  micSelect.disabled = false;
}

async function checkMicrophoneConnection() {
  if (!navigator.mediaDevices?.getUserMedia) {
    micSelect.disabled = true;
    setMicStatus("이 브라우저에서는 마이크 권한 확인을 지원하지 않아요.");
    return;
  }

  micCheck.disabled = true;
  micCheck.textContent = "확인 중";
  setMicStatus("마이크 권한을 확인하고 있어요. 브라우저가 묻는 권한을 허용해 주세요.");

  const deviceId = micSelect.value || selectedMicId;
  const audioConstraint = deviceId ? { deviceId: { exact: deviceId } } : true;

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: audioConstraint });
    stream.getTracks().forEach((track) => track.stop());
    await populateMicrophoneList();
    const selectedName = micSelect.options[micSelect.selectedIndex]?.textContent || "선택된 마이크";
    setMicStatus(`${selectedName} 연결을 확인했어요. 음성 입력은 브라우저/기기 기본 마이크 설정을 따를 수 있어요.`);
  } catch (error) {
    const messages = {
      NotAllowedError: "마이크 권한이 거부됐어요. 브라우저 주소창이나 기기 설정에서 마이크 허용을 켜 주세요.",
      NotFoundError: "연결된 마이크를 찾지 못했어요. 마이크나 이어폰 연결을 확인해 주세요.",
      NotReadableError: "다른 앱이 마이크를 사용 중일 수 있어요. 잠시 뒤 다시 확인해 주세요.",
      OverconstrainedError: "선택한 마이크를 사용할 수 없어요. 다른 마이크를 선택해 주세요.",
    };
    setMicStatus(messages[error.name] ?? "마이크 연결 확인이 어려워요. 기기와 브라우저 권한을 확인해 주세요.");
  } finally {
    micCheck.disabled = false;
    micCheck.textContent = "마이크 연결 확인";
  }
}

function renderActivities() {
  const list = document.querySelector("#activity-list");
  list.innerHTML = "";

  activities.slice(0, 5).forEach((activity) => {
    const item = document.createElement("li");
    item.className = "activity-item";
    item.innerHTML = `
      <div>
        <strong>${activity.title}</strong>
        <span>${activity.detail}</span>
      </div>
      <div class="activity-time">${activity.time}</div>
    `;
    list.appendChild(item);
  });
}

actionButtons.forEach((button) => {
  button.addEventListener("click", () => setView(button.dataset.view));
});

privateChatBack.addEventListener("click", () => {
  showPrivateList();
});

privateChatSend.addEventListener("click", () => sendPrivateMessage(privateChatInput.value));

privateChatInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    sendPrivateMessage(privateChatInput.value);
  }
});

groupChatSend.addEventListener("click", () => sendGroupMessage(groupChatInput.value));

groupChatInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    sendGroupMessage(groupChatInput.value);
  }
});

voiceButton.addEventListener("click", () => startVoiceInput("private"));

groupVoiceButton.addEventListener("click", () => startVoiceInput("group"));

helpDetailBack.addEventListener("click", () => {
  showHelpList();
});

micCheck.addEventListener("click", () => {
  checkMicrophoneConnection();
});

micSelect.addEventListener("change", () => {
  selectedMicId = micSelect.value;
  const selectedName = micSelect.options[micSelect.selectedIndex]?.textContent || "선택한 마이크";
  setMicStatus(`${selectedName}을 선택했어요. 실제 연결 상태는 마이크 연결 확인으로 다시 확인할 수 있어요.`);
});

if (navigator.mediaDevices?.addEventListener) {
  navigator.mediaDevices.addEventListener("devicechange", () => {
    populateMicrophoneList().catch(() => {
      setMicStatus("마이크 목록을 새로 확인하지 못했어요.");
    });
  });
}

renderChoices("#help-list", helpChoices, (choice) => {
  openHelpDetail(choice);
});

renderContactList();
renderNetworkList();
renderPrivateQuickActions();
renderPrivateChat();
renderGroupQuickActions();
renderGroupChat();
setupVoiceInput();
renderActivities();
showPrivateList();
showHelpList();
