# **xid-msi**

## **개요**
- wix3 기반의 MSI 설치 파일 생성 라이브러리.

# **설치**
1. wix3.14 설치 및 시스템 환경변수의 PATH에 등록.
2. xid-msi 설치
3. 다음과 같이 사용.
```python
import msi

project = msi.Create()
project.Build()

```
