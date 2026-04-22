# FileDownTransfer

**역할**: 화면에 표시되지 않는 비시각적 다운로드 컴포넌트. `download(url, saveName)` 호출로 서버 파일을 클라이언트에 저장한다. `FileDownload`와 API가 유사하지만 UI를 갖지 않아 코드에서만 제어한다.
**출처**: `sample_filedownloadtransfer_01.xfdl` (컴포넌트명: `FileDownloadTransfer`)

## 최소 구성

비시각 컴포넌트이므로 XFDL `<Objects>` 영역에 선언:

```xml
<FileDownloadTransfer id="FileDownloadTransfer00"
                      onsuccess="FileDownloadTransfer00_onsuccess"
                      onerror="FileDownloadTransfer00_onerror"/>
```

다운로드 트리거는 버튼 등 다른 컴포넌트에서 스크립트로 호출:

```xml
<Button id="btnDown" taborder="0" text="다운로드"
        left="20" top="20" width="120" height="50"
        onclick="btnDown_onclick"/>
```

## 주요 속성

FileDownTransfer 자체 속성은 없다. 이벤트 핸들러 연결이 핵심이다.

## 이벤트

| 이벤트 | 시그니처 | 설명 |
|---|---|---|
| `onsuccess` | `(obj:nexacro.FileDownloadTransfer, e)` | 다운로드 완료 시 발생 |
| `onerror` | `(obj:nexacro.FileDownloadTransfer, e)` | 다운로드 실패 시 발생 |
| `onprogress` | `(obj:nexacro.FileDownloadTransfer, e)` | 다운로드 진행 중 발생 (진행률 표시 가능) |

## 사용 API (스크립트)

```javascript
// 다운로드 실행 — URL과 저장 파일명 전달
this.btnDown_onclick = function(obj, e) {
    var fileUrl  = this.Dataset00.getColumn(e.row, "fileurl");
    var saveName = "master.zip";
    this.FileDownloadTransfer00.download(fileUrl, saveName);
};

// 성공 핸들러
this.FileDownloadTransfer00_onsuccess = function(obj, e) {
    this.alert("파일 다운로드가 완료되었습니다.");
};

// 실패 핸들러
this.FileDownloadTransfer00_onerror = function(obj, e) {
    this.alert("다운로드 실패: " + e.errormsg);
};
```

## 주의점 / 팁

- `download(url, saveName)` 의 두 번째 인자로 저장 파일명을 지정한다. 생략하면 서버의 Content-Disposition 헤더를 따른다.
- 비시각적 컴포넌트이므로 진행 상태를 사용자에게 알리려면 별도의 Static·ProgressBar 컴포넌트와 `onprogress` 이벤트를 조합한다.
- 동일 URL을 여러 번 다운로드하려면 `download()` 완료(`onsuccess`) 후 다시 호출해야 한다.
- 서버 측 응답 헤더에 `Content-Disposition: attachment; filename="파일명"` 설정이 없으면 브라우저 정책에 따라 동작이 다를 수 있다.
