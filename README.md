# samplelab
csv 파일을 업로드하고 결측치 제거 및 데이터확인을 거쳐 간단한 회귀/분류 모델을 통해 학습시키는 과정을 담은 Django 기반 openML 프로젝트

- Back : Django(Python)
- Front : HTML, CSS, Javascript(Bootstrap 활용)
- 학습 모델 : LightGBM Regressor, LightGBM Classifier
- 전처리 모델 : Scikit-Learn MinMaxScaler, Scikit-Learn StandardScaler
- 시각화 라이브러리 : Plotly(Boxplot, Heatmap), ChartJS(Histogram, Barchart)
- 기타 활용 라이브러리 : Pandas, Numpy

1) 파일 업로드
![samplelab1](https://user-images.githubusercontent.com/73330542/121798390-f6888180-cc60-11eb-8b43-f86baa187dfd.jpg)

2) 데이터 확인 및 결측치 제거 방법 선택
![samplelab2](https://user-images.githubusercontent.com/73330542/121798388-f5efeb00-cc60-11eb-85a9-69d5fe4915a4.jpg)

3) 데이터 분포 정보 확인
![samplelab3](https://user-images.githubusercontent.com/73330542/121798386-f5efeb00-cc60-11eb-9ac0-a4ac1372daeb.jpg)

4) 데이터 컬럼 간 상관관계 및 Range 확인
![samplelab4](https://user-images.githubusercontent.com/73330542/121798385-f5575480-cc60-11eb-9d8d-8d7776bf8a95.jpg)

5) 학습에 활용할 X데이터와 y데이터 컬럼 및 학습데이터셋의 크기 선택
![samplelab5](https://user-images.githubusercontent.com/73330542/121798384-f4262780-cc60-11eb-8244-c9e165b6b26e.jpg)

6) 모델과 스케일러 종류 선택
![samplelab6](https://user-images.githubusercontent.com/73330542/121798392-f7211800-cc60-11eb-8223-8b4d9ec4d208.jpg)

7) 학습결과 확인(모델 정확도 및 피쳐중요도)
![samplelab7](https://user-images.githubusercontent.com/73330542/121798391-f6888180-cc60-11eb-93be-df6f7eef06f1.jpg)





