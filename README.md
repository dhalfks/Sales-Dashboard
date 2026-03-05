## Sales Dashboard (Streamlit)

식품 회사의 수입/수출 데이터를 임의로 생성하고, 월별 수출입 내역을 시각화하는 대시보드입니다.

### 1) 설치

```bash
pip install -r requirements.txt
```

### 2) 임시 데이터 생성

```bash
python generate_data.py
```

실행 후 `data/trade_data.csv` 파일이 생성됩니다.

### 3) 대시보드 실행

```bash
streamlit run app.py
```

브라우저에서 월별 수입/수출 금액 및 건수를 확인할 수 있습니다.
# Sales-Dashboard
