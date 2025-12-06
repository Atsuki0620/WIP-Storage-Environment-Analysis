#!/usr/bin/env python3
"""
データ品質検証スクリプト

検証内容:
1. センサーマスタのセンサーシリアルに、各計測ログCSVのserialが含まれること
2. ファイル名形式 `計測ログ_<SERIAL>(*_30d).csv` とCSV内serialが一致すること
3. 計測ログ_X0073B9LA2F.csv は serial が 100% X0073B9LA2F であること
"""
import sys
from pathlib import Path
import re
import pandas as pd


def validate_data():
    """データ品質検証を実行"""
    errors = []
    warnings = []

    # プロジェクトルートディレクトリを取得
    root_dir = Path(__file__).parent.parent
    data_dir = root_dir / 'data'

    # センサーマスタを読み込み
    sensor_master_path = data_dir / 'センサーマスタ.csv'
    if not sensor_master_path.exists():
        errors.append(f"センサーマスタ.csv が見つかりません: {sensor_master_path}")
        print_results(errors, warnings)
        return False

    sensor_master = pd.read_csv(sensor_master_path, encoding='utf-8-sig')
    valid_serials = set(sensor_master['センサーシリアル'].astype(str))

    print(f"センサーマスタに登録されているシリアル: {valid_serials}")
    print()

    # 計測ログファイルを検証
    log_files = sorted(data_dir.glob('計測ログ_*.csv'))

    if not log_files:
        errors.append("計測ログファイルが見つかりません")
        print_results(errors, warnings)
        return False

    print(f"検証対象ファイル数: {len(log_files)}")
    print()

    for log_file in log_files:
        print(f"検証中: {log_file.name}")

        # ファイル名からシリアルを抽出
        match = re.match(r'計測ログ_([A-Z0-9]+)(?:_30d)?\.csv$', log_file.name)
        if not match:
            warnings.append(f"  ファイル名の形式が不正: {log_file.name}")
            continue

        expected_serial = match.group(1)
        print(f"  期待されるserial: {expected_serial}")

        # CSVを読み込み
        try:
            df = pd.read_csv(log_file, encoding='utf-8-sig')
        except Exception as e:
            errors.append(f"  CSV読み込みエラー ({log_file.name}): {e}")
            continue

        if 'serial' not in df.columns:
            errors.append(f"  'serial' 列が見つかりません: {log_file.name}")
            continue

        # CSV内のserial値を確認
        actual_serials = set(df['serial'].astype(str).unique())
        print(f"  実際のserial値: {actual_serials}")

        # 検証1: センサーマスタにserialが含まれること
        for serial in actual_serials:
            if serial not in valid_serials:
                errors.append(
                    f"  センサーマスタに未登録のserial: {serial} "
                    f"(ファイル: {log_file.name})"
                )

        # 検証2: ファイル名とCSV内serialの一致
        if len(actual_serials) == 1:
            actual_serial = list(actual_serials)[0]
            if actual_serial != expected_serial:
                errors.append(
                    f"  ファイル名とserial不一致: "
                    f"ファイル名={expected_serial}, CSV内={actual_serial} "
                    f"(ファイル: {log_file.name})"
                )
        else:
            warnings.append(
                f"  複数のserial値が混在: {actual_serials} "
                f"(ファイル: {log_file.name})"
            )

        # 検証3: X0073B9LA2F.csv は 100% X0073B9LA2F であること
        if log_file.name in ['計測ログ_X0073B9LA2F.csv', '計測ログ_X0073B9LA2F_30d.csv']:
            if actual_serials != {'X0073B9LA2F'}:
                errors.append(
                    f"  {log_file.name} のserialが100% X0073B9LA2F ではありません: "
                    f"{actual_serials}"
                )
            else:
                print(f"  ✓ serialが100% X0073B9LA2F です")

        print()

    print_results(errors, warnings)

    return len(errors) == 0


def print_results(errors, warnings):
    """検証結果を出力"""
    print("=" * 60)
    print("検証結果")
    print("=" * 60)

    if warnings:
        print("\n【警告】")
        for warning in warnings:
            print(f"  - {warning}")

    if errors:
        print("\n【エラー】")
        for error in errors:
            print(f"  - {error}")
        print(f"\n検証失敗: {len(errors)} 件のエラーがあります")
    else:
        print("\n✓ すべての検証に成功しました")

    print("=" * 60)


if __name__ == '__main__':
    success = validate_data()
    sys.exit(0 if success else 1)
