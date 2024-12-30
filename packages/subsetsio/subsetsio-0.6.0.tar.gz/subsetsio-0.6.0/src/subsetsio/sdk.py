from typing import Dict, List, Optional, Any, Union, Tuple
from pathlib import Path
import requests
import json
from dataclasses import dataclass
from .models.chart import parse_chart, parse_chart_metadata

@dataclass
class ChartDiff:
    chart_id: str
    create: List[List[Any]]
    update: List[List[Any]]
    delete: List[List[Any]]

class ChartDiffer:
    @staticmethod
    def _extract_key(datapoint: List[Any]) -> Any:
        return datapoint[0]
        
    def diff_data(self, old_data: List[List[Any]], new_data: List[List[Any]]) -> ChartDiff:
        old_lookup = {self._extract_key(item): item for item in old_data}
        new_lookup = {self._extract_key(item): item for item in new_data}
        
        common_keys = set(old_lookup.keys()) & set(new_lookup.keys())
        removed_keys = set(old_lookup.keys()) - common_keys
        added_keys = set(new_lookup.keys()) - common_keys
        
        update_keys = {
            key for key in common_keys 
            if old_lookup[key] != new_lookup[key]
        }
        
        return ChartDiff(
            chart_id="",
            create=[new_lookup[k] for k in added_keys],
            update=[new_lookup[k] for k in update_keys],
            delete=[old_lookup[k] for k in removed_keys]
        )

class SubsetsSDK:
    def __init__(self, api_key: str, api_url: str = "https://api.subsets.io", data_dir: str = "data"):
        self.api_key = api_key
        self.api_url = api_url.rstrip('/')
        self.headers = {"X-API-Key": api_key}
        self.differ = ChartDiffer()
        
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.charts_file = self.data_dir / "charts.jsonl"
        
        if not self.charts_file.exists():
            self.charts_file.touch()

    def _load_charts(self) -> Dict[str, Dict[str, Any]]:
        charts = {}
        if self.charts_file.stat().st_size > 0:
            with open(self.charts_file, 'r') as f:
                for line in f:
                    chart = json.loads(line)
                    charts[chart['sync_id']] = chart
        return charts 

    def _save_charts(self, charts: Dict[str, Dict[str, Any]]) -> None:
        sorted_charts = dict(sorted(charts.items()))
        with open(self.charts_file, 'w') as f:
            for chart in sorted_charts.values():
                f.write(json.dumps(chart) + '\n')

    def _has_metadata_changes(self, old_chart: Dict[str, Any], new_chart: Dict[str, Any]) -> bool:
        metadata_fields = {'title', 'subtitle', 'description', 'icon', 'source_id', 'config', 'type'}
        return any(
            old_chart.get(field) != new_chart.get(field)
            for field in metadata_fields
        )

    def list_charts(self, source_id: Optional[str] = None) -> List[Dict[str, Any]]:
        charts = self._load_charts()
        if source_id:
            return [chart for chart in charts.values() if chart.get('chart', {}).get('source_id') == source_id]
        return list(charts.values())

    def get_chart(self, sync_id: str) -> Dict[str, Any]:
        charts = self._load_charts()
        if sync_id not in charts:
            raise KeyError(f"Chart {sync_id} not found")
        return charts[sync_id]

    def create_chart(self, chart_data: Dict[str, Any], sync_id: str) -> str:
        parse_chart(chart_data)
        
        url = f"{self.api_url}/chart"
        response = requests.post(url, headers=self.headers, json=[chart_data])
        response.raise_for_status()
        chart_id = response.json()["chart_ids"][0]
        
        charts = self._load_charts()
        charts[sync_id] = {
            "sync_id": sync_id,
            "chart": chart_data,
            "chart_id": chart_id
        }
        self._save_charts(charts)
        
        return chart_id

    def create_charts(self, items: List[Dict[str, Any]]) -> List[str]:
        charts_to_create = [item["chart"] for item in items]
        for chart in charts_to_create:
            parse_chart(chart)
            
        url = f"{self.api_url}/chart"
        response = requests.post(url, headers=self.headers, json=charts_to_create)
        response.raise_for_status()
        chart_ids = response.json()["chart_ids"]
        
        charts = self._load_charts()
        for item, chart_id in zip(items, chart_ids):
            sync_id = item["sync_id"]
            charts[sync_id] = {
                "sync_id": sync_id,
                "chart": item["chart"],
                "chart_id": chart_id
            }
        self._save_charts(charts)
        
        return chart_ids

    def update_chart_metadata(self, sync_id: str, metadata: Dict[str, Any]) -> None:
        parse_chart_metadata(metadata)
        
        charts = self._load_charts()
        if sync_id not in charts:
            raise KeyError(f"Chart {sync_id} not found")

        chart_id = charts[sync_id]["chart_id"]
        url = f"{self.api_url}/chart/{chart_id}"
        response = requests.put(url, headers=self.headers, json=metadata)
        response.raise_for_status()
        
        charts[sync_id]["chart"].update(metadata)
        self._save_charts(charts)

    def update_charts_metadata(self, updates: Dict[str, Dict[str, Any]]) -> None:
        for metadata in updates.values():
            parse_chart_metadata(metadata)
            
        charts = self._load_charts()
        modified = False
        
        for sync_id, metadata in updates.items():
            if sync_id not in charts:
                continue
                
            chart_id = charts[sync_id]["chart_id"]
            url = f"{self.api_url}/chart/{chart_id}"
            response = requests.put(url, headers=self.headers, json=metadata)
            response.raise_for_status()
            
            charts[sync_id]["chart"].update(metadata)
            modified = True
        
        if modified:
            self._save_charts(charts)

    def delete_charts(self, sync_ids: List[str]) -> None:
        charts = self._load_charts()
        chart_ids = []
        for sync_id in sync_ids:
            if sync_id in charts:
                chart_ids.append(charts[sync_id]["chart_id"])
                del charts[sync_id]
        
        if chart_ids:
            url = f"{self.api_url}/chart"
            response = requests.delete(url, headers=self.headers, json={"chart_ids": chart_ids})
            response.raise_for_status()
            self._save_charts(charts)

    def update_chart_data(self, sync_id: str, current_data: List[List[Any]], new_data: List[List[Any]]) -> None:
        charts = self._load_charts()
        if sync_id not in charts:
            raise KeyError(f"Chart {sync_id} not found")

        chart_id = charts[sync_id]["chart_id"]
        diff = self.differ.diff_data(current_data, new_data)
        
        operations = {}
        if diff.create:
            operations["create"] = diff.create
        if diff.update:
            operations["update"] = diff.update
        if diff.delete:
            operations["delete"] = diff.delete
            
        if operations:
            url = f"{self.api_url}/chart/data"
            response = requests.put(url, headers=self.headers, json={chart_id: operations})
            response.raise_for_status()
            
            charts[sync_id]["chart"]["data"] = new_data
            self._save_charts(charts)

    def update_charts_data(self, updates: Dict[str, Tuple[List[List[Any]], List[List[Any]]]]) -> None:
        all_updates = {}
        charts = self._load_charts()
        modified = False
        
        for sync_id, (current_data, new_data) in updates.items():
            if sync_id not in charts:
                continue

            diff = self.differ.diff_data(current_data, new_data)
            chart_id = charts[sync_id]["chart_id"]
            
            operations = {}
            if diff.create:
                operations["create"] = diff.create
            if diff.update:
                operations["update"] = diff.update
            if diff.delete:
                operations["delete"] = diff.delete
                
            if operations:
                all_updates[chart_id] = operations
                charts[sync_id]["chart"]["data"] = new_data
                modified = True
                
        if all_updates:
            url = f"{self.api_url}/chart/data"
            response = requests.put(url, headers=self.headers, json=all_updates)
            response.raise_for_status()
            
            if modified:
                self._save_charts(charts)

    def sync(self, charts_to_sync: List[Dict[str, Any]], remove_missing: bool = False) -> None:
        existing_charts = self._load_charts()
        to_create = []
        data_updates = {}
        metadata_updates = {}

        current_sync_ids = {item["sync_id"] for item in charts_to_sync}
        
        for item in charts_to_sync:
            parse_chart(item["chart"])
        
        for item in charts_to_sync:
            sync_id = item["sync_id"]
            chart = item["chart"]
            
            if sync_id in existing_charts:
                existing_chart = existing_charts[sync_id]["chart"]
                
                if self._has_metadata_changes(existing_chart, chart):
                    metadata_updates[sync_id] = {
                        k: v for k, v in chart.items() 
                        if k in {'title', 'subtitle', 'description', 'icon', 'source_id', 'config', 'type'} 
                        and v != existing_chart.get(k)
                    }
                
                old_data = existing_chart.get("data", [])
                new_data = chart.get("data", [])
                if old_data != new_data:
                    data_updates[sync_id] = (old_data, new_data)
            else:
                to_create.append(item)

        if remove_missing:
            to_delete = [sync_id for sync_id in existing_charts if sync_id not in current_sync_ids]
            if to_delete:
                print(f"Deleting {len(to_delete)} charts...")
                self.delete_charts(to_delete)

        if not to_create and not data_updates and not metadata_updates and not (remove_missing and to_delete):
            print("No updates needed")
            return

        if to_create:
            print(f"Creating {len(to_create)} charts...")
            self.create_charts(to_create)

        if metadata_updates:
            print(f"Updating metadata for {len(metadata_updates)} charts...")
            self.update_charts_metadata(metadata_updates)

        if data_updates:
            print(f"Updating data for {len(data_updates)} charts...")
            self.update_charts_data(data_updates)