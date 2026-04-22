# MultiLineTextField

**역할**: 여러 줄 텍스트 입력 컴포넌트. TextArea의 현대적 대체재로 글자 수 카운트, 자동 줄바꿈 설정을 지원한다.
**Source**: `sample_multilinetextfield_01.xfdl`

## 최소 구성

`<Layout>` 내부에 배치:

```xml
<MultiLineTextField id="mltf_desc" taborder="0" left="100" top="50" width="300" height="130"
                    maxlength="100" wordWrap="english" usecharcount="true"
                    oninput="mltf_desc_oninput"/>
```

### Dataset 바인딩 형태

```xml
<MultiLineTextField id="mltf_desc" taborder="0" left="100" top="50" width="300" height="130"
                    maxlength="200" wordWrap="english"/>
```

### `<Bind>` 블록 (sibling of `<Layouts>`)

```xml
<Bind>
  <BindItem id="bind0" compid="mltf_desc" propid="value" datasetid="ds_main" columnid="col_desc"/>
</Bind>
```

## 주요 속성

| 속성 | 필수 | 설명 |
|---|---|---|
| id | ✓ | 컴포넌트 고유 식별자 |
| taborder | ✓ | 탭 포커스 순서 |
| left / top / width / height | ✓ | 위치 및 크기(픽셀) |
| maxlength | | 최대 입력 가능 문자 수 |
| wordWrap | | 줄바꿈 방식: `"english"` (영어 단어 단위), `"character"` (문자 단위) |
| usecharcount | | `"true"` 시 현재/최대 글자 수 카운터 표시 |

## 이벤트

| 이벤트 | 시그니처 | 용도 |
|---|---|---|
| oninput | `(obj:nexacro.MultiLineTextField, e:nexacro.InputEventInfo)` | 입력 중 실시간 발생; `obj.getLength()` 로 현재 글자 수 확인 |
| onchanged | `(obj:nexacro.MultiLineTextField, e:nexacro.ChangeEventInfo)` | 값 변경 후 포커스를 잃을 때 발생 |

## 바인딩

Dataset 컬럼과 1:1 바인딩할 때 `propid`에 `"value"` 를 지정한다.

```javascript
// 런타임에서 글자 수 체크
var len = this.mltf_desc.getLength();
var max = this.mltf_desc.maxlength;
```

## 주의점 / 팁

- `usecharcount` 는 런타임에서도 `this.mltf_desc.usecharcount = true;` 로 동적으로 켜고 끌 수 있다.
- `wordWrap` 속성 이름은 대소문자를 혼용(`wordWrap`)하므로 소문자(`wordwrap`)로 작성하지 않도록 주의한다.
- `maxlength` 를 설정하지 않으면 글자 수 카운터가 표시되더라도 최대값이 0으로 나타난다.
