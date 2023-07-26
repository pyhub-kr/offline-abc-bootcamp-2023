# ABC 부트캠프 2023

## 보충

matplotlib/seaborn을 활용한 차트 그리기에서 마이너스 기호가 박스로 보여지는 상황이 있습니다. 이는 matplotlib에서 디폴트로 유니코드 마이너스 기호를 사용하기 때문이고, 폰트에 해당 기호가 없기 때문입니다.

아래 `plt.rc('axes', unicode_minus=False)` 설정을 하여, 유니코드 마이너스 기호가 아닌, 폰트의 기본 마이너스 기호를 활용토록 하여 이를 해결할 수 있습니다. 아래 코드를 시각화를 하는 jupyter notebook 시작 부분에 꼭 넣어주세요.

```python
import matplotlib.pyplot as plt
import platform

# Matplotlib에서 유니코드 마이너스 기호 대신 기본 마이너스 기호가 사용되도록 설정
plt.rc('axes', unicode_minus=False)

if platform.system() == "Darwin":
    plt.rc("font", family="AppleGothic")  # macOS 시스템 기본 폰트

elif platform.system() == "Windows":
    plt.rc("font", family="Malgun Gothic")  # Windows 시스템 기본 폰트
```

## 관련 과목

* 데이터 수집 및 크롤링
* 데이터 시각화

## 행정구역 SHP 파일 출처

* http://www.gisdeveloper.co.kr/?p=2332

## 강사

* 강사 : 이진석 (me@pyhub.kr)
* [인프런 파이썬/장고 분야 인기강사](https://www.inflearn.com/users/@askcompany)

