# FileUpload

**역할**: 사용자가 파일을 선택하고 서버로 전송하는 UI 컴포넌트. OS 파일 선택 버튼 내장, 파일 목록(`filelist`) 관리, `upload(url)` 실행까지 포함한다. 비UI 방식은 `FileUpTransfer`를 사용한다.
**출처**: `sample_fileupload_01.xfdl`

## 최소 구성

`<Layout>` 안에 배치:

```xml
<FileUpload id="fileupload" taborder="0"
            left="27" top="20" width="253" height="220"
            itemcount="1"
            multiselect="true"
            itemheight="50"
            buttonsize="50"
            onitemchanged="fileupload_onitemchanged"
            onitemclick="fileupload_onitemclick"/>
```

## 주요 속성

| 속성 | 설명 |
|---|---|
| `itemcount` | 표시할 최대 파일 항목 수 |
| `multiselect` | `"true"` — 다중 파일 선택 허용 |
| `itemheight` | 파일 목록 각 항목의 높이(px) |
| `buttonsize` | 파일 선택 버튼 크기(px) |
| `filelist` | (읽기 전용) 선택된 파일 정보 배열. 각 항목은 `.filename` 속성 포함 |

## 이벤트

| 이벤트 | 시그니처 | 설명 |
|---|---|---|
| `onitemchanged` | `(obj:nexacro.FileUpload, e:nexacro.FileUploadItemChangeEventInfo)` | 파일 목록 변경 시 발생 (추가·삭제) |
| `onitemclick` | `(obj:nexacro.FileUpload, e:nexacro.FileUploadItemEventInfo)` | 목록 항목 클릭 시 발생. `e.index`로 항목 인덱스 확인 |

## 사용 API (스크립트)

```javascript
// 파일 선택 항목 추가 (파일 선택 다이얼로그 열기)
this.fileupload.appendItem();

// 선택된 파일 목록 조회
if (this.fileupload.filelist.length > 0) {
    for (var i = 0; i < this.fileupload.filelist.length; i++) {
        trace(this.fileupload.filelist[i].filename);
    }
}

// 업로드 실행
this.fileupload.upload("http://example.com/upload");

// 클릭한 항목 삭제 (onitemclick 핸들러)
this.fileupload_onitemclick = function(obj, e) {
    obj.deleteItem(e.index);
};

// 파일 변경 시 목록 표시 (onitemchanged 핸들러)
this.fileupload_onitemchanged = function(obj, e) {
    var names = "";
    for (var i = 0; i < obj.filelist.length; i++) {
        names += obj.filelist[i].filename + "\n";
    }
    this.TextArea00.value = names;
};
```

## 주의점 / 팁

- `upload(url)`은 주석 처리된 채로 샘플에 존재한다. 실제 서버 URL을 지정해야 동작한다.
- `onitemclick`에서 `deleteItem(e.index)`를 호출하면 클릭한 항목을 삭제할 수 있어 UX 개선에 유용하다.
- 파일 업로드 성공·실패 이벤트(`onsuccess`, `onerror`)가 필요하면 `FileUpTransfer`와 조합하거나 FileUpload 자체 이벤트를 사용한다.
- 서버는 `multipart/form-data` 방식으로 수신해야 한다.
