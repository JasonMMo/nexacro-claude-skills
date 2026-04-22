# FileDialog

**역할**: OS 기본 파일 선택 다이얼로그를 여는 비시각적 컴포넌트. 사용자가 선택한 파일은 `onclose` 이벤트에서 `e.virtualfiles` 배열(VirtualFile 객체)로 전달된다.
**출처**: `sample_filedialog_01.xfdl`

## 최소 구성

`<Objects>` 또는 `<Layout>` 밖 비시각 영역에 선언:

```xml
<FileDialog id="FileDialog00" onclose="FileDialog00_onclose"/>
```

다이얼로그 호출은 버튼 `onclick` 등 스크립트에서 수행:

```xml
<Button id="btnOpen" taborder="0" text="파일 열기"
        left="20" top="20" width="120" height="50"
        onclick="btnOpen_onclick"/>
```

## 주요 속성

| 속성 | 설명 |
|---|---|
| `accept` | 허용할 파일 확장자 필터 문자열 (예: `".jpg,.png,.pdf"`) |

## 모드 상수

| 상수 | 설명 |
|---|---|
| `FileDialog.LOAD` | 단일 파일 선택 모드 |
| `FileDialog.MULTILOAD` | 복수 파일 선택 모드 |

## 이벤트

| 이벤트 | 시그니처 | 설명 |
|---|---|---|
| `onclose` | `(obj:nexacro.FileDialog, e:nexacro.FileDialogEventInfo)` | 다이얼로그 닫힐 때 발생. `e.virtualfiles`에 선택된 파일 배열 포함 |

## 사용 API (스크립트)

```javascript
// 단일 파일 선택 다이얼로그 열기
this.btnOpen_onclick = function(obj, e) {
    this.FileDialog00.accept = ".jpg,.png,.gif";  // 선택적 필터
    this.FileDialog00.open("타이틀", FileDialog.LOAD);
};

// 복수 파일 선택
this.btnMulti_onclick = function(obj, e) {
    this.FileDialog00.open("파일 선택", FileDialog.MULTILOAD);
};

// 선택된 파일 처리 (onclose 핸들러)
this.FileDialog00_onclose = function(obj, e) {
    var count = e.virtualfiles.length;
    for (var i = 0, vFile; i < count; i++) {
        vFile = e.virtualfiles[i];
        vFile.addEventHandler("onsuccess", this.vFile_onsuccess, this);
        vFile.open(null, VirtualFile.openRead);
    }
};

// VirtualFile 열기 성공 후 처리
this.vFile_onsuccess = function(obj, e) {
    // obj.filename 으로 파일명 접근
    this.FileUpTransfer00.addFile(obj.filename, obj);
};
```

## 주의점 / 팁

- `open()` 메서드는 블로킹이 아니라 OS 다이얼로그를 띄운 뒤 즉시 반환한다. 선택 결과는 반드시 `onclose`에서 처리한다.
- 사용자가 다이얼로그를 취소하면 `onclose`가 발생하지 않거나 `e.virtualfiles.length == 0`이다. 빈 배열 방어 코드를 작성한다.
- `accept` 필터는 OS 다이얼로그 기본 필터로 표시되지만, 실제 파일 타입 검증은 서버·스크립트에서 별도로 수행해야 한다.
- 선택한 파일은 `VirtualFile` 객체로 전달된다. 파일 경로 문자열이 아니므로 `FileUpTransfer.addFile()`과 함께 사용한다.
