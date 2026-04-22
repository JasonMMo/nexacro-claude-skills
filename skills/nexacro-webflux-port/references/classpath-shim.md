# Classpath 교체 전략 (maven-dependency-plugin unpack + excludes)

원본 Nexacro JAR (`nexacroN-xapi-jakarta`, `nexacroN-xeni-jakarta`) 의 **POJO/POI 클래스는 재사용**하고,
**Servlet 결합 클래스만 WebFlux 재구현으로 교체**하는 표준 패턴.

## 왜 필요한가

- 원본 JAR 안에는 Servlet 결합 클래스(10+개) 와 POJO/POI 클래스(수백 개) 가 **한 패키지 안에 섞여 있다**.
- Servlet 결합 클래스만 제거하고 WebFlux 재구현으로 바꿔야 한다.
- 패키지/시그니처를 그대로 유지해야 POJO/POI 클래스들이 내부 호출 시 **재구현된 클래스를 찾을 수 있다**.

## 표준 pom.xml 구조 (xeni-webflux 예)

```xml
<dependencies>
    <!--
         System-scope 원본 JAR — POJO/POI 클래스 제공.
         <optional>true</optional> 로 다운스트림 transitive 전파 차단.
         unpack 플러그인은 로컬 모듈 범위에서만 동작하므로 optional 로 가려도 무방.
    -->
    <dependency>
        <groupId>com.nexacro</groupId>
        <artifactId>nexacroN-xeni-jakarta</artifactId>
        <version>${nexacro.xeni.version}</version>
        <scope>system</scope>
        <systemPath>${project.basedir}/lib/nexacroN-xeni-jakarta-*.jar</systemPath>
        <optional>true</optional>
    </dependency>
    <!-- 그 외 spring-webflux, reactor-core, poi, commons-io, ... -->
</dependencies>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-dependency-plugin</artifactId>
            <executions>
                <execution>
                    <id>unpack-nexacro-xeni-pojo</id>
                    <phase>process-classes</phase>
                    <goals><goal>unpack</goal></goals>
                    <configuration>
                        <artifactItems>
                            <artifactItem>
                                <groupId>com.nexacro</groupId>
                                <artifactId>nexacroN-xeni-jakarta</artifactId>
                                <version>${nexacro.xeni.version}</version>
                                <type>jar</type>
                                <overWrite>false</overWrite>
                                <outputDirectory>${project.build.outputDirectory}</outputDirectory>
                                <!--
                                    Servlet 결합 .class 들을 exclude.
                                    각 excluded .class 는 src/main/java 의
                                    WebFlux 재구현이 classpath 에서 우선 적용됨.
                                -->
                                <excludes>
                                    com/nexacro/java/xeni/services/GridExportImportServlet.class,
                                    com/nexacro/java/xeni/services/GridExportImportAgent.class,
                                    com/nexacro/java/xeni/provider/ServletProvider.class,
                                    com/nexacro/java/xeni/extend/XeniMultipartProcBase.class,
                                    com/nexacro/java/xeni/extend/XeniMultipartProcDef.class,
                                    com/nexacro/java/xeni/extend/XeniExcelDataStorageBase.class,
                                    com/nexacro/java/xeni/extend/XeniExcelDataStorageDef.class,
                                    com/nexacro/java/xeni/export/impl/GridPartExportExcel.class,
                                    com/nexacro/java/xeni/export/impl/GridPartExportCsv.class,
                                    com/nexacro/java/xeni/export/api/GridExportExcel.class,
                                    com/nexacro/java/xeni/ximport/GridImportContext.class,
                                    com/nexacro/java/xeni/ximport/impl/GridImportExcelXSSFEvent.class,
                                    META-INF/**
                                </excludes>
                            </artifactItem>
                        </artifactItems>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

## 규칙

1. **`<scope>system</scope>` + `<optional>true</optional>`** — 시스템 JAR 은 빌드 참조용이고 실제 POJO 는 unpack 으로 `target/classes` 에 복제된다. optional 로 다운스트림 transitive 전파를 차단하지 않으면 소비자 classpath 에 원본 Servlet-coupled 클래스가 올라와 충돌.
2. **패키지/시그니처 유지** — shim 클래스는 `com.nexacro.java.xeni.*` 동일 경로/이름 사용. 패키지를 바꾸면 원본 JAR 내부 호출이 깨진다.
3. **`META-INF/**` 항상 exclude** — 원본 JAR 의 manifest/서명이 충돌할 수 있음.
4. **`jdeps` 검증이 유일한 진실** — shim 이 제대로 대체됐는지는 `jdeps target/xeni-webflux-*.jar | grep jakarta.servlet` = 0 건 으로만 판정.

## 함정 ① — POI / commons-io transitive 전파 실패

xeni-webflux 가 `nexacroN-xeni-jakarta` 를 system-scope 로 선언하면 Maven 이 xeni-webflux 의 POM 을
"invalid" 로 판정해 **transitive dependency 를 다운스트림에 전혀 전파하지 않는다**.

```
[WARNING] The POM for xeni-webflux is invalid, transitive dependencies (if any) will not be available
```

**해결**: Excel I/O 책임이 있는 하위 모듈(`uiadapter-webflux-excel`) 에서 **POI / commons-io 를 직접 선언**.
버전은 xeni-webflux 와 동일 유지.

```xml
<dependency>
    <groupId>org.apache.poi</groupId>
    <artifactId>poi</artifactId>
    <version>5.2.5</version>
</dependency>
<dependency>
    <groupId>org.apache.poi</groupId>
    <artifactId>poi-ooxml</artifactId>
    <version>5.2.5</version>
</dependency>
<dependency>
    <groupId>commons-io</groupId>
    <artifactId>commons-io</artifactId>
    <version>2.15.1</version>
</dependency>
```

## 함정 ② — Windows 파일 잠금

`mvn clean` 시 `target/classes` 의 unpacked 파일이 `javap` / `jdeps` 등 다른 프로세스에 잠겨 실패.

```
다른 프로세스가 파일을 사용 중이기 때문에 프로세스가 액세스 할 수 없습니다
```

**해결**: 먼저 `rm -rf <module>/target` 후 `mvn clean package`.

## 함정 ③ — excludes 에서 놓친 클래스

`jdeps` 에서 잔여 `jakarta.servlet` 참조가 남으면, exclude 목록에 빠진 클래스가 있다는 뜻.

```bash
# 어떤 클래스가 문제인지 식별
jdeps -v target/xeni-webflux-*.jar 2>&1 | grep -B1 jakarta.servlet
```

**처리 옵션**:
- **재구현이 필요한 경우** (다른 클래스가 호출) → shim 작성 후 excludes 에 추가.
- **orphan 인 경우** (reverse 참조 0건) → excludes 에만 추가하고 재구현 생략.
  - reverse 참조 확인: `javap -c target/classes/**/*.class 2>&1 | grep "<orphan-class-fqcn>"` → 결과 없음.
