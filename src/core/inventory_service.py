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

    def _normalize(self, text):
        t = text.lower().strip()
        clean_text = t.replace('(', ' ').replace(')', ' ').replace('-', ' ').replace('_', ' ')
        words = clean_text.split()
        normalized_words = []
        for w in words:
            if len(w) > 3 and w.endswith('s'):
                normalized_words.append(w[:-1])
            else:
                normalized_words.append(w)
        return set(normalized_words), t

    def _check_match(self, target_norm, target_words, key):
        key_words, key_norm = self._normalize(key)
        
        # 1. Direct contains
        if target_norm in key_norm or key_norm in target_norm:
            return True
            
        # 2. Word overlap
        common = target_words.intersection(key_words)
        if len(common) >= 1 and any(len(w) > 3 for w in common):
            return True
        elif len(common) >= 2:
            return True
            
        # 3. Heuristic for critical equipment
        critical_terms = {"oxygen", "n95", "respirator", "medical", "aid", "rope", "water", "gloves"}
        if any(w in critical_terms for w in target_words) and any(w in critical_terms for w in key_words):
            if target_words.intersection(key_words).intersection(critical_terms):
                return True
        return False

    def _apply_deduction(self, val, key, qty, log):
        if isinstance(val, dict) and "qty" in val:
            val["qty"] = max(0, val["qty"] - qty)
            val["deployed"] = val.get("deployed", 0) + qty
            log.append(f"{qty}x {key}")
            print(f"✅ LOGISTICS: Deducted {qty}x {key}. New Total Deployed: {val['deployed']}")
        return True

    def deduct_items(self, items_to_deduct):
        """
        Deducts items from stock and adds to 'deployed' count.
        items_to_deduct: List of strings OR list of dicts with {'name', 'qty'}
        """
        data = self._load_data()
        categories = data.get('categories', {})
        deducted_log = []

        for item in items_to_deduct:
            name = item['name'] if isinstance(item, dict) else item
            qty_to_sub = item['qty'] if isinstance(item, dict) else 1
            
            target_words, target_norm = self._normalize(name)
            
            found = False
            # Deep-search all categories and subcategories
            for cat, items in categories.items():
                if found: break
                
                for key, val in items.items():
                    # Check if val is a nested category itself
                    if isinstance(val, dict) and not any(k in val for k in ["qty", "stock", "stock_count"]):
                        # It's a subcategory, search inside it
                        for sub_key, sub_val in val.items():
                            if self._check_match(target_norm, target_words, sub_key):
                                self._apply_deduction(sub_val, sub_key, qty_to_sub, deducted_log)
                                found = True
                                break
                    else:
                        # It's a direct item
                        if self._check_match(target_norm, target_words, key):
                            self._apply_deduction(val, key, qty_to_sub, deducted_log)
                            found = True
                            break
            
            if not found:
                print(f"⚠️ LOGISTICS WARNING: Could not find match for '{name}' in any category.")
        
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
