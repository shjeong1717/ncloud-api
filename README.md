### /init.sh 파일 우선 실행

---
<br>

/config.py 의 _ACCESS_KEY, _SECRET_KEY 에 네이버 클라우드의 키 정보 입력

---
<br>

/api : 파이썬으로 실행할 파일 폴더
- execEventRuleGroup.py: Configuration > Event Rule
- execMonitorGroup.py: Configuration > Template > Target group
- execMetricsGroup.py: Configuration > Template > Rule template
- execPlugin.py: Configuration > Plugin (process, port, file 플러그인 설정)

---
<br>

/yaml : 설정을 입력할 yaml파일 폴더 (파이썬 파일과 1:1매칭)
- event.yaml
- monitor.yaml
- metric.yaml
- plugin.yaml

---
<br>


> <a href="https://guide.ncloud-docs.com/docs/management-rmgr-1-1-2#NRNNcloudResourceNames" target="_blank">리소스 유형 참고 페이지 이동</a><br>
