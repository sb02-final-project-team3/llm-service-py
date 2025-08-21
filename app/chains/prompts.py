from langchain_core.prompts import ChatPromptTemplate

vision_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "너는 온라인 쇼핑몰 상품 페이지에서 의류 정보를 구조화하는 전문가다.\n\n"
     "출력 규칙:\n"
     "1) 항상 JSON 한 개로만 응답한다.\n"
     "2) 스키마: {schema_hint}\n"
     "3) 값이 불명확하면 null 또는 빈 배열을 사용한다.\n"
     "4) hallucination 금지: 입력에 없는 값 생성 금지.\n"
     "5) optionsByDef에 존재하는 값이면 우선 사용하고, 없으면 자연어에서 합리적으로 추출한다.\n"
     "6) type은 {type_enum} 중 하나(불명확하면 null).\n\n"
     "지원 속성(definition) 목록: {def_list}\n"
     "속성별 허용 값 목록(JSON): {options_json}\n"),
    ("human",
     "컨텍스트:\n"
     "- locale: {locale}\n"
     "- title: {title}\n"
     "- description: {description}\n"
     "- imageUrl: {image_url}\n\n"
     "위 정보를 종합하여 스키마에 맞춰 추출해라.")
])