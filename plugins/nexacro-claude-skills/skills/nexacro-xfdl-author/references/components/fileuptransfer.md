# FileUpTransfer

**역할**: 화면에 표시되지 않는 비시각적 업로드 컴포넌트. `FileDialog` + `VirtualFile`로 파일을 가져온 뒤 `addFile()`로 큐에 추가하고 `upload(url)`로 서버에 전송한다. `onsuccess`/`onerror`/`onprogress` 이벤트로 전송 상태를 추적한다.
**출처**: `sample_fileuptransfer_01.xfdl`

## 최소 구성

비시각 컴포넌트이므로 `<Objects>` 영역에 선언:

```xml
<FileUpTransfer id="FileUpTransfer00"
                onprogress="FileUpTransfer00_onprogress"
                onsuccess="FileUpTransfer00_onsuccess"
                onerror="FileUpTransfer00_onerror"/>
```

파일 선택을 위한 FileDialog와 함께 사용:

```xml
<FileDialog id="FileDialog00" onclose="FileDialog00_onclose"/>
<Button id="btnUpload" taborder="0" text="업로드"
        left="150" top="20" width="120" height="50"
        onclick="btnUpload_onclick"/>
```

## 주요 속성

FileUpTransfer 자체 속성은 없다. 동작은 메서드 호출과 이벤트 핸들러로 제어한다.

## 이벤트

| 이벤트 | 시그니처 | 설명 |
|---|---|---|
| `onprogress` | `(obj:nexacro.FileUploadTransfer, e:nexacro.FileUploadTransferProgressEventInfo)` | 업로드 진행 중 발생 |
| `onsuccess` | `(obj:nexacro.FileUploadTransfer, e:nexacro.FileUploadTransferEventinfo)` | 업로드 완료 시 발생 |
| `onerror` | `(obj:nexacro.FileUploadTransfer, e:nexacro.FileUploadTransferErrorEventInfo)` | 업로드 실패 시 발생 |

## 사용 API (스크립트)

```javascript
// 1단계: FileDialog로 파일 선택
this.btnOpen_onclick = function(obj, e) {
    this.FileDialog00.open("파일 선택", FileDialog.MULTILOAD);
};

// 2단계: FileDialog onclose에서 VirtualFile 열기
this.FileDialog00_onclose = function(obj, e) {
    for (var i = 0, len = e.virtualfiles.length, vFile; i < len; i++) {
        vFile = e.virtualfiles[i];
        vFile.addEventHandler("onsuccess", this.FileList_onsuccess, this);
        vFile.addEventHandler("onerror",   this.FileList_onerror,   this);
        vFile.open(null, VirtualFile.openRead);
    }
};

// 3단계: VirtualFile 열기 성공 시 업로드 큐에 추가
this.FileList_onsuccess = function(obj, e) {
    this.FileUpTransfer00.addFile(obj.filename, obj);
};

this.FileList_onerror = function(obj, e) {
    this.alert("파일 열기 실패: " + obj.filename);
};

// 4단계: 업로드 실행
this.btnUpload_onclick = function(obj, e) {
    this.FileUpTransfer00.upload("http://example.com/fileupload");
};

// 이벤트 핸들러
this.FileUpTransfer00_onprogress = function(obj, e) {
    // e.loadedsize, e.totalsize 로 진행률 계산 가능
};

this.FileUpTransfer00_onsuccess = function(obj, e) {
    this.alert("업로드가 완료되었습니다.");
};

this.FileUpTransfer00_onerror = function(obj, e) {
    this.alert("업로드 실패");
};
```

## 주의점 / 팁

- 파일 선택 -> VirtualFile open -> addFile -> upload 의 4단계 파이프라인을 순서대로 완료해야 한다.
- `addFile(filename, virtualFile)`은 업로드 전 여러 번 호출하여 복수 파일을 큐에 쌓을 수 있다.
- `upload(url)` 한 번으로 큐에 있는 모든 파일이 서버로 전송된다.
- 전송 완료 후 다시 업로드하려면 `addFile()`부터 다시 시작해야 한다 (큐 초기화 필요).
- 서버는 `multipart/form-data` 방식으로 파일을 수신해야 한다.
