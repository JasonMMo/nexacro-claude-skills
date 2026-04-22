# ProgressBar

**역할**: 작업 진행 상태를 시각적으로 표시하는 막대 컴포넌트. `pos` 값을 직접 설정하거나 `stepIt()`으로 단계적으로 증가시킨다.
**출처**: `sample_progressbar_01.xfdl`

## 최소 구성

`<Layout>` 안에 배치:

```xml
<ProgressBar id="ProgressBar00" taborder="0"
             left="32" top="40" width="480" height="32"
             min="0" max="100" smooth="true"/>
```

## 주요 속성

| 속성 | 타입 | 설명 |
|---|---|---|
| `min` | number | 최솟값 (기본값: 0) |
| `max` | number | 최댓값 (기본값: 100) |
| `pos` | number | 현재 진행 위치. `min` ~ `max` 범위 |
| `step` | number | `stepIt()` 호출 시 증가량 (기본값: 1) |
| `direction` | string | `forward`(왼→오른쪽, 기본값) / `backward`(오른→왼쪽) |
| `smooth` | boolean | `true` 설정 시 부드러운 애니메이션 표시 |
| `text` | string | 진행 바 위에 표시할 텍스트 |

## 이벤트

ProgressBar 자체에 사용자 인터랙션 이벤트는 없다. 진행 상태 변화는 외부에서 타이머(Timer) 등을 통해 `pos`를 갱신한다.

## 사용 API (스크립트)

```javascript
// pos 직접 설정
this.ProgressBar00.pos = 50;
this.ProgressBar00.text = "50 %";

// stepIt()으로 단계 증가 (step 속성 값만큼 pos 증가)
this.ProgressBar00.stepIt();

// 현재 진행률(%) 계산
var pct = parseInt((this.ProgressBar00.pos / this.ProgressBar00.max) * 100);
this.ProgressBar00.text = pct + " %";

// 초기화
this.ProgressBar00.pos  = 0;
this.ProgressBar00.text = "대기 중";
```

## 주의점 / 팁

- `pos`가 `max`에 도달해도 자동으로 멈추지 않는다. 스크립트에서 `pos == max` 조건을 확인하여 타이머를 중지해야 한다.
- `direction="backward"` 설정 시 오른쪽에서 왼쪽 방향으로 진행 표시된다.
- 두 개 이상의 ProgressBar를 동시에 사용할 때는 각각 독립적인 `pos`를 관리해야 한다.
- 텍스트를 `"N %"` 형식으로 실시간 업데이트하면 사용자에게 진행 상황을 명확히 전달할 수 있다.
