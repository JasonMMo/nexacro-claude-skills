# FileDownload

**역할**: 서버에서 파일을 다운로드하는 UI 컴포넌트. 다운로드 진행 상태를 시각적으로 표시하며, `download(url)` API로 실행한다. `FileDownTransfer`가 비UI 방식인 데 반해 FileDownload는 화면에 배치 가능한 컴포넌트다.
**출처**: `sample_filedownloadtransfer_01.xfdl` (FileDownload와 FileDownTransfer 비교 사용)

## 최소 구성

`<Layout>` 안에 배치:

```xml
<FileDownload id="FileDownload00" taborder="0"
              left="24" top="100" width="290" height="100"
              onsuccess="FileDownload00_onsuccess"
              onerror="FileDownload00_onerror"/>
```

## 주요 속성

| 속성 | 설명 |
|---|---|
| `left` / `top` / `width` / `height` | 화면 상 컴포넌트 위치·크기 |
| `text` | 컴포넌트 내부 표시 텍스트 |

## 이벤트

| 이벤트 | 시그니처 | 설명 |
|---|---|---|
| `onsuccess` | `(obj:nexacro.FileDownload, e)` | 다운로드 완료 시 발생 |
| `onerror` | `(obj:nexacro.FileDownload, e)` | 다운로드 실패 시 발생 |
| `onprogress` | `(obj:nexacro.FileDownload, e)` | 다운로드 진행 중 발생 (진행률 표시에 활용) |

## 사용 API (스크립트)

```javascript
// 다운로드 시작 — URL을 전달
this.FileDownload00.download("http://example.com/files/report.pdf");

// 성공 핸들러
this.FileDownload00_onsuccess = function(obj, e) {
    this.alert("다운로드가 완료되었습니다.");
};

// 실패 핸들러
this.FileDownload00_onerror = function(obj, e) {
    this.alert("다운로드 중 오류가 발생했습니다.");
};
```

## 주의점 / 팁

- `FileDownload`는 화면에 표시되는 컴포넌트이므로 `left`/`top`/`width`/`height`를 반드시 지정한다.
- 비시각적 다운로드가 필요할 때는 `FileDownTransfer`를 사용한다. 두 컴포넌트의 API(`.download()`)는 동일하지만 용도가 다르다.
- 다운로드 URL은 서버 측에서 Content-Disposition 헤더를 적절히 설정해야 올바른 파일명으로 저장된다.
- `onerror`를 반드시 구현하여 네트워크 오류나 403/404 응답을 사용자에게 안내한다.
