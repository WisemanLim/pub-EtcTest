# EtcTest

다양한 테스트 및 유틸리티 스크립트 모음입니다.

## 개요

qPCR 데이터 분석, PPT 병합, Ollama LLM 테스트 등 다양한 기능을 제공하는 유틸리티 스크립트 모음입니다.

## 주요 기능

### 1. QpcrSigmoidCt.py
- qPCR 데이터의 시그모이드 곡선 분석
- Ct 값 계산
- 효율성 추정
- 시각화

### 2. LocalOllama.py
- Ollama LLM 로컬 테스트
- 간단한 챗봇 인터페이스
- REST API 테스트

### 3. PPTMerge.py
- PowerPoint 파일 병합 유틸리티

## 사용 방법

### qPCR 분석

```bash
python QpcrSigmoidCt.py
```

`qpcr_input.csv` 파일이 필요합니다.

### Ollama 테스트

```bash
python LocalOllama.py
```

Ollama가 실행 중이어야 합니다.

## 요구사항

- Python 3.12
- numpy
- matplotlib
- ollama (LocalOllama.py 사용 시)

## 설치

### uv 설치

#### Windows
```powershell
# PowerShell에서 실행
irm https://astral.sh/uv/install.ps1 | iex
```

#### macOS / Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

설치 후 터미널을 재시작하거나 다음 명령어로 PATH에 추가:
```bash
export PATH="$HOME/.cargo/bin:$PATH"
```

### 가상환경 설정

```bash
# Python 3.12 가상환경 생성
uv venv --python 3.12

# 가상환경 활성화
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

### 패키지 설치

```bash
# uv를 사용한 패키지 설치
uv pip install -r requirements.txt
```

## 파일 구조

- `QpcrSigmoidCt.py`: qPCR 시그모이드 곡선 분석
- `QpcrSigmoidCt2.py`: qPCR 분석 변형 버전
- `QpcrSigmoidCtST.py`: qPCR 분석 ST 버전
- `LocalOllama.py`: Ollama LLM 테스트
- `PPTMerge.py`: PowerPoint 파일 병합

## 데이터 형식

### qPCR 입력 파일 형식
CSV 파일 형식으로, 첫 번째 열은 cycle 번호이고, 이후 열은 각 샘플의 형광값입니다.

---

해당 프로젝트는 Examples-Python의 Private Repository에서 공개 가능한 수준의 소스를 Public Repository로 변환한 것입니다.

