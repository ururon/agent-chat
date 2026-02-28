#!/usr/bin/env python3
"""
生成 OpenAPI YAML 規格檔

將 FastAPI app 的 OpenAPI JSON 匯出為 YAML 格式
用於版本控制與文件生成
"""

import json
import sys
from pathlib import Path

import yaml

# 確保能夠導入 app 模組
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app


def generate_openapi_yaml(output_path: str = "openapi.yaml") -> None:
    """
    生成 OpenAPI YAML 規格檔

    Args:
        output_path: 輸出檔案路徑（相對於 backend/ 目錄）
    """
    # 取得 OpenAPI schema
    openapi_schema = app.openapi()

    # 確保輸出目錄存在
    output_file = Path(__file__).parent.parent / output_path
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # 轉換為 YAML 並寫入檔案
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(
            openapi_schema,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )

    print(f"✓ OpenAPI YAML 已生成: {output_file}")
    print(f"  檔案大小: {output_file.stat().st_size / 1024:.2f} KB")


if __name__ == "__main__":
    try:
        generate_openapi_yaml()
        print("\n✓ 完成！")
    except Exception as e:
        print(f"❌ 錯誤: {e}", file=sys.stderr)
        sys.exit(1)
