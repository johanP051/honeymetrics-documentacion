with open("/tmp/generate_exact_excel.py", "r") as f:
    content = f.read()

hyperlink_logic = """
        if c_idx in [1, 2, 6, 7]:
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            
        if c_idx == 2:
            try:
                pb_num_str = hu[1].split('-')[2].split('.')[0]
                pb_num = int(pb_num_str)
                fila_en_hoja1 = 6 + pb_num
                cell.hyperlink = f"#'PRODUCT BACKLOG'!A{fila_en_hoja1}"
                cell.font = link_font
            except Exception:
                pass
                
        if c_idx == 7:
            cell.value = "[Pendiente screenshot]"
"""

old_logic = """
        if c_idx in [1, 2, 6, 7]:
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            
        if c_idx == 7 and hu[6] != "N/A":
            cell.value = "LINK"
            cell.hyperlink = hu[6]
            cell.font = link_font
        elif c_idx == 7 and hu[6] == "N/A":
            cell.value = "FOTO"
"""

content = content.replace(old_logic.strip(), hyperlink_logic.strip())

with open("/tmp/generate_exact_excel.py", "w") as f:
    f.write(content)
