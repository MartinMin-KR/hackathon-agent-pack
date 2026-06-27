export const contacts = [
  {
    id: "다정-102",
    avatar: "102",
    safeArea: "같은 생활권",
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
    safeArea: "버스 2정거장 안팎",
    shared: "화분 관심",
    status: "새 안부 가능",
    privacy: "상대에게는 아이디와 넓은 생활권만 보여요.",
    messages: [
      { author: "마음-214", text: "식사는 하셨어요?", mine: false },
      { author: "나", text: "물어봐줘서 고마워요.", mine: true },
    ],
  },
  {
    id: "온기-330",
    avatar: "330",
    safeArea: "가까운 시장 근처 생활권",
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
    safeArea: "도보 15분 안팎",
    shared: "바둑 관심",
    status: "대화 대기",
    privacy: "서로 동의하기 전에는 개인 신상을 더 열지 않아요.",
    messages: [
      { author: "이웃-417", text: "잠은 잘 주무셨어요?", mine: false },
    ],
  },
];

export const helpChoices = [
  {
    label: "대화가 불편해요",
    result: "불편 신고가 준비됐어요. 신고에는 상대 아이디만 전달되고 자세한 신상은 공개되지 않습니다.",
    workerType: "불편 신고",
  },
  {
    label: "연결된 상대를 바꾸고 싶어요",
    result: "연결 변경 요청이 준비됐어요. 정확한 주소 없이 가까운 생활권 안에서 다시 배정됩니다.",
    workerType: "연결 변경 요청",
  },
  {
    label: "앱 사용이 어려워요",
    result: "앱 사용 도움 요청이 준비됐어요. 다음 버전에서는 가족/도우미에게 도움 링크를 보낼 수 있습니다.",
    workerType: "사용 지원 요청",
  },
  {
    label: "긴급 상황 안내",
    result: "지금 위험하거나 아프면 앱 안에서 기다리지 말고 112 또는 119에 바로 연락하세요.",
    workerType: "긴급 안내 노출",
  },
];

export const groupMessages = [
  { author: "마음-214", text: "오늘 시장에 다녀왔어요.", mine: false },
  { author: "온기-330", text: "저녁은 따뜻하게 챙겨 드세요.", mine: false },
  { author: "나", text: "물어봐줘서 고마워요.", mine: true },
];

export const seedActivities = [
  { title: "다정-102님과 1대1 대화", detail: "오늘 컨디션은 어떠세요?", time: "방금" },
  { title: "마음-214님에게 답했어요", detail: "물어봐줘서 고마워요", time: "10분 전" },
  { title: "단체방에 글을 남겼어요", detail: "저도 잠깐 들렀어요", time: "25분 전" },
];

export const replyRecommendationSets = [
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

export const privateQuickMessages = [
  "약은 챙기셨어요?",
  "오늘 컨디션은 어떠세요?",
  "식사는 하셨어요?",
  "잠은 잘 주무셨어요?",
  "아픈 곳은 없으세요?",
  "네, 챙겼어요",
  "괜찮아요",
  "조금 힘들어요",
  "물어봐줘서 고마워요",
];

export const groupQuickMessages = [
  "오늘 다들 어떠세요?",
  "식사 챙기셨어요?",
  "저도 잠깐 들렀어요",
  "응원합니다",
  "고마워요",
];

export const workerQueueSeed = [
  {
    id: "queue-1",
    memberId: "다정-102",
    type: "불편 신고",
    summary: "대화가 불편하다는 도움 항목을 열었어요.",
    state: "새로 도착",
  },
  {
    id: "queue-2",
    memberId: "마음-214",
    type: "연결 변경 요청",
    summary: "현재 연결 상대를 바꾸고 싶다는 요청이 남아 있어요.",
    state: "검토 필요",
  },
  {
    id: "queue-3",
    memberId: "이웃-417",
    type: "사용 지원 요청",
    summary: "앱 사용이 어렵다는 항목이 선택됐어요.",
    state: "안내 준비",
  },
];
