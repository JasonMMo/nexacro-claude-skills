# VirtualFile

**역할**: 클라이언트 메모리상의 파일 핸들을 추상화한 비시각적 객체. `FileDialog`, `FileUpTransfer`와 함께 파일 읽기·쓰기 파이프라인을 구성한다. XFDL 선언이 아닌 스크립트로 인스턴스를 생성하거나 다른 컴포넌트의 콜백에서 전달받는다.
**출처**: `sample_filedialog_01.xfdl` (FileDialog 콜백 내 VirtualFile 활용 패턴)

## 최소 구성

VirtualFile은 XFDL `<Layout>` 에 직접 선언하지 않는다. `FileDialog`의 `onclose` 콜백에서 `e.virtualfiles` 배열로 전달받거나, `FileUpTransfer`에서 파일 목록을 추가할 때 사용한다.

```xml
<!-- VirtualFile 자체는 비시각적 — 선언 없음 -->
<!-- FileDialog와 함께 사용하는 선언 예시 -->
<FileDialog id="FileDialog00" onclose="FileDialog00_onclose"/>
```

## 주요 속성 / 상수

| 항목 | 설명 |
|---|---|
| `filename` | (읽기 전용) 파일 이름 문자열 |
| `VirtualFile.openRead` | `open()` 호출 시 읽기 모드 상수 |
| `VirtualFile.openWrite` | `open()` 호출 시 쓰기 모드 상수 |

## 이벤트

| 이벤트 | 시그니처 | 설명 |
|---|---|---|
| `onsuccess` | `(obj:nexacro.VirtualFile, e:nexacro.VirtualFileEventInfo)` | `open`, `read`, `write`, `getFileSize` 등의 비동기 작업 성공 시 발생. `e.reason`으로 완료된 작업 구분 |
| `onerror` | `(obj:nexacro.VirtualFile, e:nexacro.VirtualFileErrorEventInfo)` | 파일 작업 실패 시 발생 |

## 사용 API (스크립트)

```javascript
// FileDialog onclose에서 virtualfile 목록 처리
this.FileDialog00_onclose = function(obj, e) {
    for (var i = 0, len = e.virtualfiles.length, vFile; i < len; i++) {
        vFile = e.virtualfiles[i];
        vFile.addEventHandler("onsuccess", this.vFile_onsuccess, this);
        vFile.addEventHandler("onerror",   this.vFile_onerror,   this);
        vFile.open(null, VirtualFile.openRead);  // 비동기 — onsuccess에서 후속 처리
    }
};

// onsuccess에서 reason 분기 처리
this.vFile_onsuccess = function(obj, e) {
    switch (e.reason) {
        case 1: // open 완료
            obj.getFileSize();
            break;
        case 2: // getFileSize 완료
            // obj.filename, e.size 사용 가능
            break;
    }
};

// FileUpTransfer에 파일 추가
this.vFile_onsuccess_forUpload = function(obj, e) {
    this.FileUpTransfer00.addFile(obj.filename, obj);
};
```

## 주의점 / 팁

- VirtualFile의 모든 I/O는 **비동기**다. `open()` 직후 파일 내용에 접근하면 안 되고, 반드시 `onsuccess` 핸들러 안에서 후속 작업을 수행한다.
- `e.reason` 상수 값(1=open, 2=getFileSize 등)은 공식 문서에서 확인한다. 숫자를 하드코딩하기보다 주석으로 의미를 명시한다.
- `FileDialog`에서 다중 파일을 선택하면 `e.virtualfiles`가 배열로 전달된다. 반드시 반복 처리해야 한다.
- `FileUpTransfer.addFile(filename, virtualFile)` 호출로 VirtualFile을 업로드 큐에 추가할 수 있다.
