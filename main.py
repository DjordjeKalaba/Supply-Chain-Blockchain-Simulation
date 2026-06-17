import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
from datetime import datetime
import json
import os

# ---------------- BLOCKCHAIN ---------------- #

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        content = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(content.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

    @staticmethod
    def from_dict(block_dict):
        block = Block(
            block_dict["index"],
            block_dict["timestamp"],
            block_dict["data"],
            block_dict["previous_hash"]
        )
        block.hash = block_dict["hash"]
        return block

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(
            0,
            datetime.now().isoformat(),
            {
                "proizvod": "GENESIS",
                "faza": "Početak",
                "entitet": "Sistem",
                "uspješno": True,
                "vrijeme": datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            },
            "0"
        )

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        new_block = Block(
            len(self.chain),
            datetime.now().isoformat(),
            data,
            self.get_latest_block().hash
        )
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def to_list(self):
        return [block.to_dict() for block in self.chain]

    @staticmethod
    def from_list(chain_list):
        bc = Blockchain()
        bc.chain = [Block.from_dict(b) for b in chain_list]
        return bc

# ---------------- JSON HANDLING ---------------- #

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    BASE_DIR = os.getcwd()

JSON_FILE = os.path.join(BASE_DIR, "blockchain_data.json")



def load_products():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            data = json.load(f)
        products = {}
        for pid, chain_list in data.items():
            products[pid] = Blockchain.from_list(chain_list)
        return products
    return {}

def save_products():
    data = {pid: bc.to_list() for pid, bc in products.items()}
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- GUI ---------------- #

products = load_products()
stages_list = ["manufacturer","distributor","retailer","customer"]

root = tk.Tk()
root.title("Supply Chain Simulation")
root.geometry("1150x650")
root.configure(bg="#f0f0f0")

# --- Lijeva kolona --- #
left_frame = tk.Frame(root, bg="#f0f0f0", width=300)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Kreiranje proizvoda
prod_card = tk.LabelFrame(left_frame, text="Create Product", padx=10, pady=10, bg="#f0f0f0")
prod_card.pack(fill=tk.X, pady=5)

tk.Label(prod_card, text="Product Name:", bg="#f0f0f0").pack(anchor='w')
product_name_entry = tk.Entry(prod_card)
product_name_entry.pack(fill=tk.X, pady=2)

tk.Label(prod_card, text="Manufacturer:", bg="#f0f0f0").pack(anchor='w')
manufacturer_entry = tk.Entry(prod_card)
manufacturer_entry.pack(fill=tk.X, pady=2)

tk.Label(prod_card, text="Product Type:", bg="#f0f0f0").pack(anchor='w')
product_type_combo = ttk.Combobox(prod_card, values=["Food","Drink","Electronics","Clothes","Shoes"])
product_type_combo.current(0)
product_type_combo.pack(fill=tk.X, pady=2)

# Obrada proizvoda
proc_card = tk.LabelFrame(left_frame, text="Process Product", padx=10, pady=10, bg="#f0f0f0")
proc_card.pack(fill=tk.X, pady=5)

tk.Label(proc_card, text="Select Product:", bg="#f0f0f0").pack(anchor='w')
product_select_combo = ttk.Combobox(proc_card)
product_select_combo.pack(fill=tk.X, pady=2)

tk.Label(proc_card, text="Current Stage:", bg="#f0f0f0").pack(anchor='w')
current_stage_combo = ttk.Combobox(proc_card, values=stages_list[1:])
current_stage_combo.pack(fill=tk.X, pady=2)

tk.Label(proc_card, text="Entity Name:", bg="#f0f0f0").pack(anchor='w')
entity_entry = tk.Entry(proc_card)
entity_entry.pack(fill=tk.X, pady=2)

tk.Label(proc_card, text="Status:", bg="#f0f0f0").pack(anchor='w')
status_combo = ttk.Combobox(proc_card, values=["Successful","Unsuccessful"])
status_combo.current(0)
status_combo.pack(fill=tk.X, pady=2)

# --- Desna kolona sa scrollbarom --- #
right_frame = tk.Frame(root, bg="#f0f0f0")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

canvas = tk.Canvas(right_frame, bg="#f0f0f0", highlightthickness=0)
scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

product_cards = {}

# Blockchain info
blockchain_frame = tk.LabelFrame(scrollable_frame, text="Blockchain Info", padx=15, pady=10, bg="#f0f0f0", font=("Arial",12,"bold"))
blockchain_frame.pack(side=tk.TOP, fill="x", padx=10, pady=10)

tk.Label(blockchain_frame, text="Total Blocks:", bg="#f0f0f0").pack(anchor='w')
block_count_label = tk.Label(blockchain_frame, text="0", bg="#f0f0f0")
block_count_label.pack(anchor='w')

tk.Label(blockchain_frame, text="Last Block Time:", bg="#f0f0f0").pack(anchor='w')
last_block_label = tk.Label(blockchain_frame, text="No Data", bg="#f0f0f0")
last_block_label.pack(anchor='w')

status_label = tk.Label(blockchain_frame, text="Checking...", bg="#f0f0f0")
status_label.pack(anchor='w')

tk.Button(blockchain_frame, text="Verify Blockchain", command=lambda: verify_blockchain()).pack(pady=3)
tk.Button(blockchain_frame, text="Blockchain Details", command=lambda: show_blockchain_details()).pack(pady=3)

# ----------------- FUNKCIJE ----------------- #

def reset_fields():
    product_name_entry.delete(0, tk.END)
    manufacturer_entry.delete(0, tk.END)
    product_type_combo.current(0)
    product_select_combo.set("")
    current_stage_combo.set("")
    entity_entry.delete(0, tk.END)
    status_combo.current(0)

def update_product_select():
    product_select_combo['values'] = list(products.keys())

def create_product():
    pid = product_name_entry.get().strip()
    manufacturer = manufacturer_entry.get().strip()
    ptype = product_type_combo.get().strip()

    if not pid:
        messagebox.showerror("Error", "Please enter a product name.")
        return
    if pid in products:
        messagebox.showerror("Error", "Product already exists.")
        return

    bc = Blockchain()
    bc.add_block({
        "proizvod": pid,
        "faza": "manufacturer",
        "entitet": manufacturer,
        "tip": ptype,
        "uspješno": True,
        "vrijeme": datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    })
    products[pid] = bc
    save_products()
    refresh_gui_after_change(pid)
    reset_fields()
    messagebox.showinfo("Success", f"Product {pid} created successfully.")

def process_product():
    pid = product_select_combo.get().strip()
    bc = products[pid]
    if not bc.is_chain_valid():
        messagebox.showerror("Error", f"Cannot process {pid} because its blockchain is CORRUPTED! Fix the chain first.")
        return
    stage = current_stage_combo.get().strip()
    entity = entity_entry.get().strip()
    status = status_combo.get().strip()

    if not pid or pid not in products:
        messagebox.showerror("Error", "Please select a valid product.")
        return

    
    current_index = stages_list.index(bc.chain[-1].data.get("faza"))
    next_index = stages_list.index(stage)
    if next_index != current_index + 1:
        messagebox.showerror("Error", f"You must follow the order of stages! Next stage should be: {stages_list[current_index+1]}")
        return

    data = {
        "proizvod": pid,
        "faza": stage,
        "entitet": entity,
        "uspješno": status=="Successful",
        "vrijeme": datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    }

    bc.add_block(data)
    save_products()
    refresh_gui_after_change(pid)
    reset_fields()
    messagebox.showinfo("Success", f"Product {pid} processed successfully.")

def update_blockchain_info(pid):
    if pid not in products:
        block_count_label.config(text="0")
        last_block_label.config(text="No Data")
        status_label.config(text="No Data")
        return

    bc = products[pid]
    block_count_label.config(text=str(len(bc.chain)))
    last_block_label.config(text=bc.chain[-1].timestamp)
    if bc.is_chain_valid():
        status_label.config(text="Blockchain VALID ✅", fg="green")
    else:
        status_label.config(text="Blockchain CORRUPTED ❌", fg="red")

def verify_blockchain():
    pid = product_select_combo.get().strip()
    update_blockchain_info(pid)
    messagebox.showinfo("Verification", f"Blockchain for {pid} is {'VALID' if products[pid].is_chain_valid() else 'CORRUPTED'}.")

def show_blockchain_details():
    pid = product_select_combo.get().strip()
    if pid not in products:
        messagebox.showerror("Error", "Select a valid product.")
        return

    bc = products[pid]
    details = ""
    for block in bc.chain:
        details += f"Block #{block.index}\nTime: {block.timestamp}\nData: {block.data}\nHash: {block.hash}\nPrevious Hash: {block.previous_hash}\n{'-'*40}\n"

    top = tk.Toplevel(root)
    top.title(f"Blockchain Details - {pid}")
    text = tk.Text(top, wrap="word", width=100, height=30)
    text.pack(fill="both", expand=True)
    text.insert("1.0", details)
    text.config(state="disabled")

def view_history(pid):
    if pid not in products:
        return
    bc = products[pid]
    top = tk.Toplevel(root)
    top.title(f"History - {pid}")
    text = tk.Text(top, wrap="word", width=80, height=20)
    text.pack(fill="both", expand=True)
    for block in bc.chain[1:]:
        ts = block.data.get("vrijeme", block.timestamp)
        stage = block.data.get("faza", "")
        entity = block.data.get("entitet","")
        status = "Successful" if block.data.get("uspješno") else "Unsuccessful"
        text.insert("end", f"{ts} | Stage: {stage.capitalize()} | Entity: {entity} | Status: {status}\n")
    text.config(state="disabled")

# ----------------- VIZUALNE KARTICE ----------------- #

def update_visual_products():
    for widget in scrollable_frame.winfo_children():
        if widget != blockchain_frame:
            widget.destroy()
    product_cards.clear()

    for pid, bc in products.items():
        card = tk.Frame(scrollable_frame, bg="#ffffff", bd=2, relief="groove")
        card.pack(fill="x", pady=8, padx=40)  

        tk.Label(card, text=f"{pid}", bg="#ffffff", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(5,5))

        stages_frame = tk.Frame(card, bg="#ffffff")
        stages_frame.pack(fill="x", padx=10, pady=5)

        current_stage = bc.chain[-1].data.get("faza","")
        for stage in stages_list:
            color = "#4caf50" if stage == current_stage else "#f0f0f0"
            lbl = tk.Label(stages_frame, text=stage.capitalize(), bg=color, fg="black",
                           font=("Arial", 11, "bold"), width=20, relief="ridge", bd=1, padx=5, pady=5)
            lbl.pack(side="left", padx=2)

        tk.Button(card, text="View History", command=lambda p=pid: view_history(p),
                  bg="#1976d2", fg="white", font=("Arial", 10, "bold"), bd=0, relief="raised").pack(pady=5, padx=10, fill="x")

        product_cards[pid] = card

def refresh_gui_after_change(pid=None):
    update_product_select()
    if pid:
        update_blockchain_info(pid)
    update_visual_products()

# Dugmad
tk.Button(prod_card, text="Create", command=create_product, bg="#1976d2", fg="white", font=("Arial",10,"bold")).pack(pady=5, fill="x")
tk.Button(proc_card, text="Process", command=process_product, bg="#1976d2", fg="white", font=("Arial",10,"bold")).pack(pady=5, fill="x")

# Initial GUI update
refresh_gui_after_change()

root.mainloop()
