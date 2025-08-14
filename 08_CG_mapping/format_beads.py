# Simple interactive helper to build <beads> and <weights> lists for VOTCA mapping
# - No third-party libs
# - Elements supported: C, H, O, S, F
# - Duplicate indices are detected and skipped (with warnings)
# - Final summary reports counts per element and total
#
# Example inputs (finish by pressing Enter on the "element symbol" prompt):
#   Molecule name: MOL
#   Element symbol: C
#   Indices for C (space-separated): 163 165 167
#   Element symbol: O
#   Indices for O (space-separated): 164 171
#   Element symbol: H
#   Indices for H (space-separated): 166 168 169
#   Element symbol: <Enter to finish>

def format_beads_weights_with_checks():
    # Atomic mass table (approximate integer masses)
    mass_dict = {"C": 12, "H": 1, "O": 16, "S": 32, "F": 19}

    mol_name = input("请输入分子名（如 MOL）: ").strip()

    beads_entries = []          # ordered list of "1:MOL:C163" ...
    weights_entries = []        # ordered list of "12" ...
    seen = set()                # set of tuples like ("C", "163")
    per_element_counts = {}     # element -> count

    def add_atom(symbol: str, idx: str):
        """Try adding one atom; check duplicates; update data structures."""
        key = (symbol, idx)
        if key in seen:
            print(f"⚠ 重复：{symbol}{idx} 已存在，已跳过。")
            return False
        seen.add(key)
        beads_entries.append(f"1:{mol_name}:{symbol}{idx}")
        weights_entries.append(str(mass_dict[symbol]))
        per_element_counts[symbol] = per_element_counts.get(symbol, 0) + 1
        return True

    while True:
        symbol = input("请输入元素符号（C/H/O/S/F，回车结束）: ").strip()
        if symbol == "":
            break
        if symbol not in mass_dict:
            print(f"⚠ 不支持的元素：{symbol}，已跳过。支持的元素：C H O S F")
            continue

        raw = input(f"请输入 {symbol} 的原子序号（用空格分隔）: ").strip()
        if not raw:
            print("⚠ 未输入任何序号，已跳过该元素。")
            continue

        tokens = raw.split()
        # Check duplicates within the current batch
        batch_seen = set()
        for t in tokens:
            if not t.isdigit():
                print(f"⚠ 非数字序号：{t}，已跳过。")
                continue
            if t in batch_seen:
                print(f"⚠ 本次输入内重复：{symbol}{t}，已跳过。")
                continue
            batch_seen.add(t)
            add_atom(symbol, t)

        # After each element batch, show a brief count update
        print(f"当前累计：{', '.join([f'{k}={v}' for k,v in sorted(per_element_counts.items())])} "
              f"| 总计={sum(per_element_counts.values())}")

    # Final outputs
    print("\n===== <beads> 列表 =====")
    print(" ".join(beads_entries))

    print("\n===== <weights> 列表 =====")
    print(" ".join(weights_entries))

    # Summary
    print("\n===== 原子数量汇总 =====")
    if per_element_counts:
        for k in sorted(per_element_counts.keys()):
            print(f"{k}: {per_element_counts[k]}")
    print(f"总计: {sum(per_element_counts.values())}")

if __name__ == "__main__":
    format_beads_weights_with_checks()
