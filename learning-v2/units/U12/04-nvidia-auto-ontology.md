# NVIDIA Auto Ontology가 데이터베이스에서 만드는 의미 계층

“10월 온라인 매출이 얼마였나요?”라는 질문을 받으면 ‘온라인’이 주문 채널인지, 결제 방식인지부터 확인해야 합니다. ‘매출’도 주문을 접수한 금액, 출고한 금액, 환불을 제외한 금액으로 해석할 수 있습니다. SQL로 계산하려면 어떤 표와 열을 조인하고, 어느 정의에 맞춰 합계를 내는지 알아야 합니다. NVIDIA의 `auto-ontology` 프로젝트는 데이터베이스와 질문 사이에 이 지식을 담는 **의미 계층(semantic layer)**을 만듭니다. 이 수업은 2026-11-19에 공개 저장소의 HEAD를 조회하고 내려받아 확인한 커밋 `778ccdef75536bee5653306f8ded655924e4ada8`을 기준으로 읽습니다. 프로젝트 서버와 모델은 실행하지 않았습니다. [공식 저장소의 해당 커밋](https://github.com/NVIDIA/auto-ontology/tree/778ccdef75536bee5653306f8ded655924e4ada8), [README 작동 방식](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/README.md#how-it-works)

## 입력은 데이터베이스 구조와 구조에 관한 기록입니다

첫 입력은 연결된 데이터베이스의 **카탈로그**입니다. 여기에는 테이블과 열, 뷰, 기본 키, 선언된 외래 키가 들어갑니다. 기본 키가 주문을 유일하게 식별하고, 주문 항목의 주문 번호가 주문 표의 키를 참조하면 두 표를 어떤 열로 연결할지 있는 그대로 얻을 수 있습니다. 커넥터가 제공하면 기존 질의 이력도 읽습니다. 같은 가격 계산식이 분석 SQL에 여러 번 나타나면 그 식을 이름 붙인 계산으로 제안할 단서가 됩니다. `run_ingest`는 카탈로그를 기록하고 검색용 임베딩을 pgvector에 적재합니다. 임베딩은 대상의 이름이나 설명을 검색하기 위해 사용하는 숫자 벡터입니다. pgvector는 PostgreSQL에서 벡터를 저장하고 검색할 수 있게 하는 확장입니다. 카탈로그는 어떤 표가 실제로 있는지 보여 줍니다. 어느 가격 정의가 회사의 공인 매출인지는 별도 확인이 필요합니다. [ingest.py의 `run_ingest`](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/auto_ontology/ingestion_service/ingest.py#L82), [아키텍처의 입력과 카탈로그](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/docs/architecture.md#generate-an-ontology)

설정에서 **의미 컴파일(semantic compilation)**을 켜면 테이블별 처리와 테이블 간 처리가 이어집니다. 테이블별로 SQL로 표본을 조사하고, 열을 설명하며, 그 열을 어떤 `Term`에 묶을지 제안합니다. `Term`은 질문에서 쓰이는 업무 개념의 이름과 설명을 담는 프로젝트 내부 객체입니다. `extract_term`은 실제 테이블 이름·설명과 후보 열 목록을 프롬프트에 넣고 구조화된 응답을 요청합니다. 결과를 정리하고, 없으면 대체 결과를 만들어 반환합니다. ‘주문 항목’이라는 Term의 ‘연장 가격’ 속성이 `invoice_lines.extended_price`에 대응하면 ‘연장 가격’을 물은 에이전트가 실제 열 이름을 찾을 수 있습니다. 이 대응이 프로젝트에서 **컬럼 속성(column attribute)**을 쓰는 이유입니다. [term_extractor.py의 `extract_term`](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/auto_ontology/semantic/term_extractor.py#L237), [visit_enter.py의 `process_table`](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/auto_ontology/semantic/visit_enter.py#L870)

테이블 간 처리에서는 관련 개념을 묶고, **의미 외래 키(semantic foreign key)**로 관련 테이블의 열을 연결하며, 질의 이력 등에서 **SQL 속성(SQL attribute)**을 제안합니다. SQL 속성은 이름과 설명이 붙은 SQL 표현입니다. 예를 들어 이미 검토된 마진 계산식을 이름으로 찾을 수 있게 해 주는 항목입니다. OWL에서 속성이 개체 사이의 관계와 논리 의미를 가질 수 있다는 점을 배웠습니다. 여기서 SQL 속성이라는 이름은 에이전트가 재사용할 계산 정의를 뜻합니다. 소스에는 한 데이터베이스 안의 테이블별 처리 뒤 테이블 그룹, 외래 키, SQL 속성, 열 속성 설명을 순서대로 호출하는 코드가 있습니다. [compile.py의 `_run_semantic_compilation`](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/auto_ontology/semantic/compile.py#L49), [용어와 SQL 속성의 내부 구조](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/auto_ontology/server/model_interchange/schemas.py#L100)

## 후보 조인이 통과한다는 말의 뜻

제품이 추정하는 연결을 살펴보기 위해 합성 매출표를 예로 듭니다. 주문 O-8의 항목 두 줄 A와 B가 80과 20이고, ‘채널 취합’ 표에는 O-8에 해당하는 매칭 행이 둘 있습니다. 배송 이벤트와 수금 이벤트를 한 표로 모은 결과라서 주문당 행이 둘입니다. 두 표에 주문 코드를 붙여 조인할 수 있지만, 조인 후 각 항목이 두 번 나타나 합계가 100에서 200이 됩니다. 질문에서 한 주문 항목을 한 번만 세려고 했다면 조인 전에 매칭되는 채널 행을 한 건으로 좁히거나, 계산 단위를 유지하는 경로를 선택해야 합니다.

고정한 코드에서 의미 연결을 아직 만들지 않은 열을 처리할 때는 선언된 외래 키를 우선 사용합니다. 추정 경로는 주어진 데이터베이스 범위에서 벡터 검색과 모델 후보를 사용하고, 연결이 있고 DB 조회가 허용되면 열 값과 실제 조인을 확인합니다. `_join_returns_rows`는 조인해 적어도 한 행이 나오는지 봅니다. 일반 조인이 오류를 내면 양쪽을 텍스트로 바꿔 다시 시도할 수 있습니다. 값을 조사하면 아무 값도 만나지 않는 후보를 거를 수 있습니다. 적어도 한 행이 나왔다는 조건만으로 업무 용어의 정의가 일치했는지, 정합된 행이 몇 퍼센트인지, 집계가 중복되는지는 알 수 없습니다. `PREVENT_SEMANTIC_FK_DB_QUERIES` 설정을 켜면 이 추정 경로에서 값과 조인 확인을 수행하지 않습니다. [semantic_fk.py의 선언·추정 경로](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/auto_ontology/semantic/semantic_fk.py#L152), [조인 검사 구현](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/auto_ontology/semantic/semantic_fk.py#L753)

## 저장한 의미 계층으로 질문에 답하기

에이전트가 질문을 받으면 `retrieve`로 용어, 실제 열, 이름을 붙인 계산식과 조인 경로를 찾습니다. `run_sql`은 값을 확인하거나 초안 SQL을 시험할 때 사용합니다. 소스의 `check_query`는 질의를 파싱하고 카탈로그에서 이름을 확인한 뒤, 해당 질의의 테이블이 검색으로 제시된 범위에 드는지 검사합니다. 에이전트는 `submit`으로 최종 질의와 설명을 보낼 수 있습니다. “연장 가격이 무엇인가요?” 같은 정보 질문은 검색 근거 이후 SQL 계산 없이 제출하는 경로가 있습니다. README의 Wide World Importers 예시는 한 제품의 특정 지역·기간 매출에 합계와 항목 수, 사용한 SQL을 같이 보여 줍니다. 외부 예시의 입력과 출력 구조를 확인한 것이며, 그 결과를 이 교재에서 별도로 재실행하지 않았습니다. [README Quickstart](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/README.md#quickstart), [카탈로그와 검색 범위 검사](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/auto_ontology/retrieval/text_to_sql/react/run_sql.py#L355), [`submit` 구현](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/auto_ontology/retrieval/text_to_sql/react/loop.py#L81)

MCP로 제공되는 `check_answerable`은 질문에 나온 대상에 대해 의미 계층이 제공하는 후보를 점검하는 단계입니다. 예를 들어 ‘광고비 대비 매출’을 물을 때 광고비를 표현할 후보가 없다면 에이전트는 원천을 더 찾아야 할지 사용자에게 확인할 수 있습니다. 문서상 이 검사는 후보 검색의 포괄 정도를 산출하며 SQL을 작성하지 않습니다. 모든 질문 용어에 후보가 있어도 정확한 집계 단위를 보장하지 않습니다. 매출이 100이어야 하는 시험 입력에서 200이 나오면 실제 질의와 완료된 업무 정의를 함께 검토합니다. 사람이 승인한 이름과 설명에는 검토 표시를 붙일 수 있습니다. 해당 표시와 유효한 열 이름이 함께 나타나도 특정 질문의 답이 검토되었다는 의미와는 다릅니다. [답변 가능성 검사 문서](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/docs/architecture.md#check-answerability), [용어 승인 필드와 업데이트 코드](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/auto_ontology/server/terms/router.py#L204)

## 출력 형식에서 정확히 무엇을 교환할 수 있을까요

제품은 용어, 열 속성, SQL 속성, 의미 외래 키를 PostgreSQL에 저장하고 임베딩을 pgvector로 관리합니다. 고정한 코드의 내보내기 API는 자체 YAML과 Apache Ossie 형식을 받습니다. 자체 형식의 스키마는 `data_layer`의 카탈로그·키·조인과 `semantic_layer`의 용어·열 연결·SQL 정의 등을 기술합니다. Ossie 옵션에 `include_ontology`를 더하면 시맨틱 모델과 Ossie ontology, 둘의 매핑 문서를 ZIP으로 내보내는 경로가 있습니다. 이 경로가 사용하는 데이터 구조와 교환 형식은 ‘온톨로지’라는 이름 뒤의 구체적인 의미를 보여 줍니다. [교환 형식 스키마](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/auto_ontology/server/model_interchange/schemas.py#L15), [YAML·ZIP 구현](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/auto_ontology/server/model_interchange/service.py#L198)

앞 수업의 OWL 사례는 `EtchEquipment`와 `ProcessEquipment`에 클래스 포함 공리를 적용해 E-17의 유형을 얻었습니다. 이 제품 사례의 용어 그래프는 용어가 가리키는 표와 열, 필요한 조인, 계산 정의를 질문 시점에 제공해 SQL을 구성하는 데 쓰입니다. OWL 추론이 필요한 업무라면 교환 형식이 어떤 공리를 전달할 수 있고 어느 추론기가 의미를 해석하는지 별도로 확인해야 합니다. 원천 문장에서 개념과 공리를 찾는 ontology learning을 요청받았을 때는 문서 입력과 공리 후보 산출을 살피고, 데이터베이스 용어와 집계식을 제공하려는 경우에는 이 제품에서 본 카탈로그·매핑·질의 결과를 확인하면 됩니다. 두 접근을 함께 쓸 때는 식별자와 의미를 잇는 매핑을 따로 설계합니다. [OWL 2 Direct Semantics §2–3](https://www.w3.org/TR/owl2-direct-semantics/), [NVIDIA 모델 교환 스키마](https://github.com/NVIDIA/auto-ontology/blob/778ccdef75536bee5653306f8ded655924e4ada8/auto_ontology/server/model_interchange/schemas.py#L94)

## 설명 연습

**1.** 표와 열이 모두 존재하고 조인 미리보기에서 행도 나왔습니다. 그런데 월별 고객 수가 두 배가 됐습니다. 무엇을 추가로 확인할까요?

질문이 고객 한 명을 센다는 뜻인지 가입 기록을 센다는 뜻인지 합의합니다. 고객 ID가 지역이나 월에 따라 반복되는지 확인하고, 조인 전후의 고객 ID 개수와 각 ID당 행 수를 비교합니다. 활성 고객의 승인된 정의를 적용했는지도 확인합니다. 이름 검증과 조인 검사는 SQL 실행에 필요한 일부 조건을 확인했고, 이 과정은 실제 수의 의미를 확인합니다.

**2.** 프로젝트 용어를 표와 열에 연결한 YAML을 받았습니다. 처음 보는 독자에게 OWL 포함 공리와 무엇이 다른지 어떻게 설명할까요?

용어 YAML에서 ‘주문 항목’은 어떤 표와 열이 개념을 표현하는지 알려 줍니다. OWL에서 ‘식각 장비는 공정 장비의 하위 클래스’라는 공리는 식각 장비인 모든 개체를 공정 장비로도 해석하도록 정합니다. 각각 파일을 읽는 프로그램이 대상에 어떤 연산을 할 수 있는지 예를 들면 차이를 설명할 수 있습니다.
