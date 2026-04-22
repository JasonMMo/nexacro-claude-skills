# Form 구조 레퍼런스

xfdl 파일의 **최상위 골격** 과 섹션별 역할.

## 전체 골격

```xml
<?xml version="1.0" encoding="utf-8"?>
<FDL version="2.1">
  <Form id="main" width="1280" height="720" titletext="메인">
    <Layouts>
      <Layout width="1280" height="720"> ... </Layout>
    </Layouts>
    <Objects> ... </Objects>
    <Script type="xscript5.1"><![CDATA[ ... ]]></Script>
  </Form>
</FDL>
```

## 섹션 역할

| 섹션 | 역할 | 필수 |
|---|---|---|
| `<FDL version="2.1">` | 파일 포맷 버전 | ✓ |
| `<Form>` | Form 속성 정의 (id / 크기 / titletext / cssclass) | ✓ |
| `<Layouts>` | **가시** 컴포넌트 배치 컨테이너. 다중 해상도 지원을 위해 배열 | ✓ |
| `<Layout>` | 단일 해상도의 실제 컴포넌트 배치 | ✓ (최소 1개) |
| `<Objects>` | **비가시** 객체 선언 (Dataset, Transaction 등) | 선택 |
| `<Script>` | JavaScript 이벤트 핸들러 / 로직 | 선택 |

## `<Form>` 주요 속성

| 속성 | 기본값 | 설명 |
|---|---|---|
| `id` | — | Form 식별자. ChildFrame 의 `formurl` 로 참조되는 이름과 연결 |
| `width` / `height` | — | 디자인 기준 크기 |
| `titletext` | `""` | ChildFrame 제목바에 표시 |
| `cssclass` | — | xcss 클래스 지정 (테마) |
| `scrollbars` | `autoboth` | 스크롤 정책 |

## 다중 해상도 `<Layouts>`

```xml
<Layouts>
  <Layout name="desktop" width="1280" height="720" screenid="Screen_D"> ... </Layout>
  <Layout name="mobile"  width="360"  height="640" screenid="Screen_M"> ... </Layout>
</Layouts>
```

- `screenid` 가 environment.xml 의 `<Screen>` 과 매칭될 때 해당 `<Layout>` 이 선택됨.
- 기본은 단일 `<Layout>` 만 두고 `screenid` 생략 (모든 스크린 공통).

## `<Objects>` 안에 들어가는 것

- `<Dataset>` — 데이터 바인딩 소스 (가장 흔함)
- `<Transaction>` (구버전) — 서버 호출 정의
- 그 외 비가시 컴포넌트

→ Dataset 상세: `components/dataset.md`
→ 바인딩 패턴: `binding-patterns.md`

## `<Layout>` 내부 컴포넌트 배치 좌표계

| 속성 | 의미 |
|---|---|
| `left` | 좌측 픽셀 |
| `top` | 상단 픽셀 |
| `width` / `height` | 컴포넌트 크기 |
| `right` / `bottom` | (앵커 지정 시) 반대쪽 기준 |
| `taborder` | 탭 순서 (0부터) |

**앵커 패턴**: `left="10" right="10"` 를 동시에 주면 부모 리사이즈 시 좌우 고정 + 중앙 신축.

## `<Script>` 컨벤션

```xml
<Script type="xscript5.1"><![CDATA[
// Form 생명주기
this.Form_onload = function(obj, e) { ... };

// 컴포넌트 이벤트: this.<컴포넌트id>_<이벤트명>
this.btnSave_onclick    = function(obj, e) { ... };
this.dsList_onrowposchanged = function(obj, e, oldrow, newrow) { ... };

// 사용자 정의 함수
this.fn_loadData = function()
{
    // ...
};
]]></Script>
```

- `type="xscript5.1"` 고정 (ES5.1 서브셋 + nexacro 확장).
- `<![CDATA[ ... ]]>` 로 감싸 `<`, `>`, `&` 이스케이프 회피.
- `this` 는 Form 컨텍스트.

## 한 파일 최대 사이즈 관례

- Nexacro Studio 는 수백 KB 의 xfdl 도 다루지만 **Grid + Dataset + 복잡한 Script** 가 섞이면 편집 성능 저하.
- 업무 단위로 폼을 분할 + 공통 로직은 `Base::common.xfdl` 같은 헬퍼 폼으로 분리 권장.
