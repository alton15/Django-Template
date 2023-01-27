---

# Django Server Templete

Python Django 프레임워크를 활용한 Django 서버 템플릿입니다.

---

## 개요

- 개발 및 uWSGI 활용 프로덕션 서버 실행을 위한 자동화 Shell-script
- 주요 파라미터는 `environments.yaml` 을 참조 하도록 구성 (at `settings.py`)
- rest_framework, corsheaders(CORS) 를 포함한 django settings.py
- server_timezone 및 static & media url, logger
- 기본적인 JSON, Form-Data(File) 포멧의 Request parameter 입력에 대응하는 ExampleAPI 구성
- Response 포맷 통일

  `{'code': status_code, 'message': message, 'payload': payload}`

---

## Get Started

### 1. Set Ignored Files/Directories

- Git Ignored
  ```text
  - /system/keys.yaml  # django-secret-key, DB key 및 기타 중요 key 값이 기록된 파일
  ```

- 추가 수정 필요
  ```text
  - /system/environments.yaml  # 서버 구동 및 시스템 설정에 필요한 값들이 기록된 파일
  ```

### 2. Setup Execution Environments

- with Virtual Envs (Dev)

  패키지 설치
  
  → 프로젝트 경로 최상단의 `requirements.txt` 파일을 참고하여 Python 가상환경 세팅이 필요합니다.

  **! 주의사항 !**

  `pip install -f requirements.txt` 명령어로 라이브러리 단순 설치 시 문제가 발생할 수 있습니다.

  - conda 환경에서 uwsgi 를 설치할 땐, `conda install -c conda-forge uwsgi` 명령어를 사용해 설치

- with Docker

  Docker Image 빌드는

  `/system/environments.yaml` 의 내부 파라미터를 참조하여 Dockerfile 을 통해 빌드하도록 구성 되어있습니다

  ```bash
  # Docker Image 빌드
  ./bin/build_container.sh
  ```

### 3. Run

- with Virtual Envs (Dev)

  ```bash
  # Python 직접 실행
  python manage.py runserver 0.0.0.0:5050  # environments.yaml 의 host 와 port 참조
  
  # 스크립트로 실행 (가상환경 활성화 포함)
  ./bin/run_dev_server.sh
  
  # 백그라운드로 실행
  nohup ./bin/run_dev_server.sh &
  ```

- with uWSGI

  ```bash
  # 콘솔에서 바로 실행
  ./bin/run_uwsgi_server.sh
  
  # 백그라운드로 실행
  nohup ./bin/run_uwsgi_server.sh &
  ```

- with Docker Container

  ```bash
  # Container 실행
  ./bin/docker_run_container.sh
  
  # Container 중지
  ./bin/docker_stop_container.sh
  ```

### 4. Test

- 개발 환경 세팅

  ```bash
  # 개발 환경 세팅이 잘 되어있는지 확인할 수 있는 테스트 실행 명령어
  ./bin/test_scripts.sh
  ```

---
