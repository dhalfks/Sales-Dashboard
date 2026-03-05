from __future__ import annotations

from pathlib import Path
import random

import pandas as pd


def build_items(n: int = 100) -> list[str]:
    prefixes = [
        "유기농",
        "신선",
        "프리미엄",
        "가공",
        "냉동",
        "저염",
        "고단백",
        "저당",
        "발효",
        "전통",
    ]
    food_names = [
        "쌀",
        "밀가루",
        "옥수수",
        "대두",
        "참치캔",
        "김치",
        "라면",
        "즉석밥",
        "고추장",
        "된장",
        "식용유",
        "올리브유",
        "사과주스",
        "오렌지주스",
        "커피원두",
        "녹차",
        "우유",
        "치즈",
        "버터",
        "요거트",
    ]
    items: list[str] = []
    idx = 1
    while len(items) < n:
        for p in prefixes:
            for f in food_names:
                if len(items) >= n:
                    break
                items.append(f"{p} {f} {idx:03d}")
                idx += 1
            if len(items) >= n:
                break
    return items


def generate_trade_data(seed: int = 42) -> pd.DataFrame:
    random.seed(seed)

    total_rows = 100
    import_rows = 60
    export_rows = 40
    year = 2025

    items = build_items(100)
    countries = ["미국", "중국", "일본", "베트남", "태국", "호주", "브라질", "독일", "프랑스", "캐나다"]
    trade_types = ["수입"] * import_rows + ["수출"] * export_rows
    random.shuffle(trade_types)

    rows = []
    for i in range(total_rows):
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        date = pd.Timestamp(year=year, month=month, day=day)
        quantity = random.randint(10, 500)
        unit_price = random.randint(2_000, 50_000)
        amount = quantity * unit_price

        rows.append(
            {
                "거래일자": date.strftime("%Y-%m-%d"),
                "연도": year,
                "월": month,
                "거래구분": trade_types[i],
                "품목": items[i],
                "국가": random.choice(countries),
                "수량": quantity,
                "단가": unit_price,
                "금액": amount,
            }
        )

    df = pd.DataFrame(rows).sort_values("거래일자").reset_index(drop=True)
    return df


def main() -> None:
    df = generate_trade_data()
    output_dir = Path("data")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "trade_data.csv"
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"생성 완료: {output_path} ({len(df)}건)")
    print(df["거래구분"].value_counts())


if __name__ == "__main__":
    main()
