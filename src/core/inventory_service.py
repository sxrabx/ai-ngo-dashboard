import os
import json

class InventoryService:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.inventory_path = os.path.join(base_dir, 'data', 'inventory.json')

    def _load_data(self):
        if not os.path.exists(self.inventory_path):
            return {}
        with open(self.inventory_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_all_items(self):
        data = self._load_data()
        return data.get('categories', {})

    def get_stats(self):
        data = self._load_data()
        categories = data.get('categories', {})
        stats = {
            "total_items": 0,
            "low_stock": 0,
            "categories": len(categories),
            "critical_items": 0,
            "total_deployed": 0
        }
        
        # Flatten and count (Simplified for display)
        for cat, content in categories.items():
            for item_key, item_val in content.items():
                if isinstance(item_val, list):
                    stats["total_items"] += len(item_val)
                elif isinstance(item_val, dict):
                    if "qty" in item_val:
                        stats["total_items"] += item_val["qty"]
                        stats["total_deployed"] += item_val.get("deployed", 0)
                        if item_val["qty"] < 5: stats["low_stock"] += 1
                    elif "stock_count" in item_val:
                        stats["total_items"] += item_val["stock_count"]
                    elif "stock" in item_val:
                        stats["total_items"] += item_val["stock"]
        
        return stats

    def deduct_items(self, items_to_deduct):
        """
        Deducts specific quantities from inventory.json.
        items_to_deduct: List of strings OR list of dicts with {'name', 'qty'}
        """
        data = self._load_data()
        categories = data.get('categories', {})
        deducted_log = []

        for item in items_to_deduct:
            # Handle both simple list and list of dicts
            name = item['name'] if isinstance(item, dict) else item
            qty_to_sub = item['qty'] if isinstance(item, dict) else 1
            
            # Normalize name for matching
            search_name = name.lower().strip()
            if search_name.endswith('s'): search_name = search_name[:-1]
            name_words = set(search_name.replace('(', '').replace(')', '').split())
            
            found = False
            for cat, items in categories.items():
                for key, val in items.items():
                    norm_key = key.lower()
                    key_words = set(norm_key.replace('(', '').replace(')', '').split())
                    
                    # Robust matching logic
                    is_match = (search_name in norm_key or norm_key in search_name)
                    if not is_match:
                        # Check keyword overlap (at least one word > 3 chars matches)
                        common = name_words.intersection(key_words)
                        if len(common) >= 1 and any(len(w) > 3 for w in common):
                            is_match = True

                    if is_match:
                        if isinstance(val, dict) and "qty" in val:
                            val["qty"] = max(0, val["qty"] - qty_to_sub)
                            val["deployed"] = val.get("deployed", 0) + qty_to_sub
                            deducted_log.append(f"{qty_to_sub}x {key}")
                            found = True
                            break
                        elif isinstance(val, int):
                            items[key] = {"qty": max(0, val - qty_to_sub), "deployed": qty_to_sub}
                            deducted_log.append(f"{qty_to_sub}x {key}")
                            found = True
                            break
                if found: break
        
        with open(self.inventory_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        
        return deducted_log

    def infer_recommendations(self, mission_description, people_count=1):
        description = mission_description.lower()
        recommendations = []
        
        # Mapping with base quantities
        mapping = [
            {"keys": ["flood", "water", "drown"], "items": ["Zodiac Boat", "Life Jackets", "Water Filters", "Rope"]},
            {"keys": ["medical", "injury", "sick", "doctor", "health"], "items": ["First Aid Kit", "Oxygen Tanks", "Medical Gloves", "N95 Respirators"]},
            {"keys": ["night", "dark", "subterranean", "shaft", "tunnel"], "items": ["Tactical Flashlights", "Batteries", "Power Banks"]},
            {"keys": ["fire", "toxic", "smoke", "chemical", "leak"], "items": ["Hazmat Suits", "Respirators", "Gas Sensors"]},
            {"keys": ["rescue", "trapped", "contractors", "builders", "sealed"], "items": ["Hydraulic Spreader", "Shoring Struts", "Rope", "Plasma Cutter"]},
            {"keys": ["food", "hungry", "distribution"], "items": ["MRE Rations", "Water Bottles"]},
            {"keys": ["comm", "signal", "radio", "phone"], "items": ["Satellite Uplink", "Digital Radios"]}
        ]
        
        for rule in mapping:
            if any(k in description for k in rule["keys"]):
                for item in rule["items"]:
                    if item not in recommendations:
                        recommendations.append(item)
        
        data = self._load_data()
        final_list = []
        for rec_name in recommendations:
            # Tactical quantity logic
            qty_req = 1
            if "Water" in rec_name or "Rations" in rec_name: qty_req = people_count
            if "Respirators" in rec_name or "Mask" in rec_name: qty_req = max(10, round(people_count * 0.5))
            if "Suit" in rec_name: qty_req = 8 # Enough for a breach team
            
            final_list.append({
                "name": rec_name,
                "status": "Ready",
                "qty": qty_req
            })
            
        return final_list

    def update_stock(self, name, qty, category="Logistics"):
        """Adds or updates an inventory item with immediate sync."""
        data = self._load_data()
        if category not in data.get("categories", {}):
            if "categories" not in data: data["categories"] = {}
            data["categories"][category] = {}
        
        # Search across all categories to see if it exists
        found = False
        for cat_name, items in data["categories"].items():
            for item_key in items:
                if item_key.lower() == name.lower():
                    if isinstance(items[item_key], dict):
                        items[item_key]["qty"] = items[item_key].get("qty", 0) + qty
                    else:
                        items[item_key] = items[item_key] + qty
                    found = True
                    break
            if found: break
        
        if not found:
            data["categories"][category][name] = {"qty": qty, "price": 0}

        with open(self.inventory_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return True
