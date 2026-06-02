#!/usr/bin/env python3
"""
Steam Game Data Collection Script (Real Data)

Combines SteamSpy API (for ratings, playtime) and Steam Store API (for release dates, genres).
"""

import pandas as pd
import numpy as np
import steamspypi
import requests
import time
from datetime import datetime
import os

# Configuration
MAX_PAGES = 100  # Number of SteamSpy pages (1000 games per page) - Tăng từ 30 lên 100
REQUEST_DELAY = 1.0  # Delay between Store API calls (seconds) - Tăng để tránh rate limit
MIN_APPID = 1500000  # Giảm threshold để lấy thêm nhiều game hơn (từ 2M xuống 1.5M)
OUTPUT_PATH = 'data/raw/steam_games_raw.csv'


def fetch_steamspy_appids(pages=MAX_PAGES):
    """Fetch app IDs and metadata from SteamSpy."""
    all_data = []
    for page in range(0, pages):
        try:
            print(f"Fetching SteamSpy page {page}...")
            data = steamspypi.download({'request': 'all', 'page': page})
            if data and len(data) > 0:
                df = pd.DataFrame(data).T.reset_index()
                df = df.rename(columns={'index': 'appid'})
                # Remove duplicate appid column
                cols = df.columns.tolist()
                if cols.count('appid') > 1:
                    first_idx = cols.index('appid')
                    df = df.iloc[:, :first_idx+1].join(df.iloc[:, first_idx+2:])
                all_data.append(df)
                print(f"  Page {page}: {len(df)} games")
            else:
                print(f"  Page {page}: empty, stopping")
                break
            time.sleep(0.5)
        except Exception as e:
            print(f"  Error on page {page}: {e}")
            break

    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        combined = combined.drop_duplicates(subset='appid', keep='first')
        print(f"Total unique games from SteamSpy: {len(combined)}")
        return combined
    else:
        return pd.DataFrame()


def fetch_store_details(appid):
    """Fetch details from Steam Store API."""
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if str(appid) in data and data[str(appid)]['success']:
                return data[str(appid)]['data']
    except Exception:
        pass
    return None


def enrich_with_store_data(steamspy_df):
    """Add release_date, genres, developer, price from Steam Store."""
    appids = steamspy_df['appid'].unique().tolist()
    print(f"Enriching {len(appids)} games with Steam Store data...")

    store_records = []
    failed = []

    for i, appid in enumerate(appids, 1):
        if i % 100 == 0:
            print(f"  Processed {i}/{len(appids)}")

        details = fetch_store_details(appid)
        if details:
            store_records.append({
                'appid': appid,
                'store_name': details.get('name'),
                'release_date': details.get('release_date', {}).get('date'),
                'genres': [g['description'] for g in details.get('genres', [])],
                'developer': details.get('developers', [None])[0] if details.get('developers') else None,
                'publisher': details.get('publishers', [None])[0] if details.get('publishers') else None,
                'store_price': details.get('price_overview', {}).get('final') if details.get('price_overview') else None,
                'is_free': details.get('is_free', False)
            })
        else:
            failed.append(appid)

        time.sleep(REQUEST_DELAY)

    store_df = pd.DataFrame(store_records)
    print(f"  Successfully enriched: {len(store_df)} games")
    print(f"  Failed: {len(failed)} games")

    # Merge
    merged = pd.merge(steamspy_df, store_df, on='appid', how='inner')

    # Use store_price if available, else use SteamSpy price
    merged['price'] = merged['store_price'].combine_first(merged['price'])
    merged['price'] = pd.to_numeric(merged['price'], errors='coerce').fillna(0)

    return merged


def parse_release_date(date_str):
    """Parse Steam Store date strings like '21 Aug, 2012'."""
    if pd.isna(date_str) or not date_str:
        return None
    for fmt in ['%d %b, %Y', '%b %d, %Y', '%Y-%m-%d']:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def main():
    print("=" * 60)
    print("STEAM GAME DATA COLLECTION (2022-2026)")
    print("=" * 60)
    print(f"Configuration: MAX_PAGES={MAX_PAGES}, MIN_APPID={MIN_APPID:,}")
    print("=" * 60)

    os.makedirs('data/raw', exist_ok=True)
    
    # Bước 1: Lấy dữ liệu SteamSpy
    steamspy_df = fetch_steamspy_appids()
    if steamspy_df.empty:
        raise RuntimeError("Failed to fetch SteamSpy data")

    # BƯỚC TỐI ƯU: Ép kiểu appid về số nguyên và lọc thô trước khi gọi Store API
    steamspy_df['appid'] = pd.to_numeric(steamspy_df['appid'], errors='coerce')
    steamspy_df = steamspy_df[steamspy_df['appid'] >= MIN_APPID].copy()
    print(f"Lọc thô AppID >= {MIN_APPID:,}, còn lại {len(steamspy_df)} games tiềm năng.")

    # Bước 2: Chỉ lấy Store data cho những game tiềm năng này
    combined_df = enrich_with_store_data(steamspy_df)

    # Bước 3: Lấy ngày phát hành và lọc chính xác năm 2022-2026
    combined_df['release_date'] = combined_df['release_date'].apply(parse_release_date)
    combined_df['year'] = combined_df['release_date'].dt.year
    before_filter = len(combined_df)

    # Lọc theo năm 2022-2026
    combined_df = combined_df[combined_df['year'].between(2022, 2026)]
    print(f"\nFiltered to 2022-2026: {len(combined_df)} games (from {before_filter})")

    # Bước 4: Lưu file
    combined_df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nRaw data saved to: {OUTPUT_PATH}")
    print(f"Dataset shape: {combined_df.shape}")


if __name__ == "__main__":
    main()