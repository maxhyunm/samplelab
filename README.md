# samplelab
csv 파일을 업로드하고 결측치 제거 및 데이터확인을 거쳐 간단한 회귀/분류 모델을 통해 학습시키는 과정을 담은 Django 기반 openML 프로젝트

- Back : Django(Python)
- Front : HTML, CSS, Javascript(Bootstrap 활용)
- 학습 모델 : LightGBM Regressor, LightGBM Classifier
- 전처리 모델 : Scikit-Learn MinMaxScaler, Scikit-Learn StandardScaler
- 시각화 라이브러리 : Plotly(Boxplot, Heatmap), ChartJS(Histogram, Barchart)
- 기타 활용 라이브러리 : Pandas, Numpy

1) 파일 업로드
![samplelab1](https://user-images.githubusercontent.com/73330542/121796508-78be7900-cc54-11eb-916f-e76f2360890c.jpg)

2) 데이터 확인 및 결측치 제거 방법 선택
![samplelab2](https://user-images.githubusercontent.com/73330542/121796515-7bb96980-cc54-11eb-97d5-1a90ca038c3e.jpg)

3) 데이터 분포 정보 확인
![samplelab3](https://user-images.githubusercontent.com/73330542/121796514-7b20d300-cc54-11eb-8226-ba287d0d65d9.jpg)

4) 데이터 컬럼 간 상관관계 및 Range 확인
![samplelab4](https://user-images.githubusercontent.com/73330542/121796513-7b20d300-cc54-11eb-8e17-7341ef83cf5d.jpg)

5) 학습에 활용할 X데이터와 y데이터 컬럼 및 학습데이터셋의 크기 선택
![samplelab5](https://user-images.githubusercontent.com/73330542/121796512-7a883c80-cc54-11eb-81f7-f3889d330570.jpg)

6) 모델과 스케일러 종류 선택
![samplelab6](https://user-images.githubusercontent.com/73330542/121796510-7a883c80-cc54-11eb-92ae-b8a2d0030849.jpg)

7) 학습결과 확인(모델 정확도 및 피쳐중요도)
![samplelab7](https://user-images.githubusercontent.com/73330542/121796509-79efa600-cc54-11eb-89c5-8dd44e89ec87.jpg)




