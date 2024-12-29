# WordExcelTools

An efficient toolkit for handling Excel files and generating Word documents, leveraging the power of python-docx and
openpyxl.
## Install

```sh
pip install wordexceltools
```

## Main Functions

```sh
1: excel_add_sheet(source_excel, sheet_name)
2: excel_copy_file(source_excel, target_excel)
3: excel_count_sheet_columns_with_prefix_suffix(sheet, column_prefix, column_suffix)
4: excel_delete_file(target_excel)
5: excel_delete_sheet_by_identifiers(source_excel, sheet_identifiers)
6: excel_delete_sheet_columns(sheet, target_column_index, number_of_columns)
7: excel_delete_sheet_columns_by_identifiers(sheet, column_identifiers)
8: excel_delete_sheet_rows(sheet, target_row_index, number_of_rows)
9: excel_fill_sheet_cells(sheet, ranges_to_fill, fill_value)
10: excel_get_sheet(workbook, sheet_identifiers)
11: excel_get_sheet_cell_date_value(sheet, row, column)
12: excel_get_sheet_cell_value(sheet, row, column)
13: excel_get_sheet_column_keyword_count(sheet, column_identifiers, keyword)
14: excel_get_sheet_column_len(sheet, column_identifiers)
15: excel_get_sheet_column_str_custom(sheet, column_identifiers, separator, end_mark)
16: excel_get_sheet_column_values(sheet, column_identifiers, include_header)
17: excel_get_sheet_row_col_count(sheet)
18: excel_get_sheet_row_or_col_max(sheet, identifiers, mode)
19: excel_get_sheet_row_values(sheet, row_identifiers, include_index)
20: excel_get_sheets_index_name(workbook)
21: excel_get_sheets_targets_counts(list_sheets, column_prefix, column_suffix)
22: excel_get_workbook(source_excel)
23: excel_insert_sheet_columns(sheet, target_column_index, number_of_columns)
24: excel_insert_sheet_rows(sheet, target_row_index, number_of_rows)
25: excel_merge_sheet_cells(sheet, ranges_to_merge)
26: excel_replace_sheet_content(sheet, target_text, replacement_text, rows, cols)
27: excel_save_workbook(workbook, output_file)
28: excel_set_sheet_alignment(sheet, ranges, horizontal, vertical)
29: excel_set_sheet_bold(sheet, ranges, bold)
30: excel_set_sheet_cell_value(sheet, row, column, value)
31: excel_set_sheet_fill_color(sheet, ranges, color_hex)
32: excel_set_sheet_font_color(sheet, ranges, color_hex)
33: excel_set_sheet_font_size(sheet, ranges, font_size)
34: excel_set_sheet_freeze_panes(sheet, cell_reference)
35: excel_unmerge_sheet_cells(sheet, ranges_to_unmerge)
36: word_add_custom_heading(document, level, text)
37: word_add_custom_paragraph(document, text, style)
38: word_add_custom_table(document, row_count, column_count, style, font_size, spacing_before)
39: word_add_figure_caption(document, caption_text)
40: word_add_indented_paragraph(document, text)
41: word_add_ordered_list(document, items, index_style, indentation)
42: word_add_table_caption(document, caption_text)
43: word_docxinitial(doc, text_font_type, text_font_size, text_font_line_spacing, text_header, text_footer)
44: word_get_section_number(paragraph_text)
45: word_get_table_cell_text(table, row_index, column_index)
46: word_merge_cells(table, start_row, start_column, end_row, end_column)
47: word_merge_cells_by_column(table, column_index)
48: word_set_number_to_roman(number)
49: word_set_table_alignment(table, start_row, start_column, end_row, end_column, horizontal_alignment, vertical_alignment)
50: word_set_table_cell_text(table, row_index, column_index, text)
51: word_set_table_cell_text(table, row_index, column_index, text)
52: word_set_table_style(table, font_size, spacing_before)
53: word_setsectionformat(doc)
```

## Example

```python
source_excel = "./test1.xlsx"
copy_excel = "./test2.xlsx"
# Test 1
excel_add_sheet(source_excel, "test1")

# Test 2
excel_copy_file(source_excel, copy_excel)

# Test 22
wb_copy = excel_get_workbook(copy_excel)

# Test 10
sheet_copy_1 = excel_get_sheet(wb_copy, 0)

# Test 3
print(excel_count_sheet_columns_with_prefix_suffix(sheet_copy_1, "平台", "结果"))

# Test 5
excel_delete_sheet_by_identifiers(copy_excel, 1)
workbook = excel_get_workbook(source_excel)

# Test 6
excel_delete_sheet_columns(sheet_copy_1, 2, 2)

# Test 7
excel_delete_sheet_columns_by_identifiers(sheet_copy_1, 1)

# Test 8
excel_delete_sheet_rows(sheet_copy_1, 2, 3)

# Test 9
excel_fill_sheet_cells(sheet_copy_1, (2, 4, 5, 4), 1)

# Test 11
print(excel_get_sheet_cell_date_value(sheet_copy_1, 10, 1))

# Test 12
print(excel_get_sheet_cell_value(sheet_copy_1, 10, 1))

# Test 13
print(excel_get_sheet_column_keyword_count(sheet_copy_1, 6, "XXXX"))

# Test 14
print(excel_get_sheet_column_len(sheet_copy_1, 6))

# Test 15
print(excel_get_sheet_column_str_custom(sheet_copy_1, 3))

# Test 16
print(excel_get_sheet_column_values(sheet_copy_1, 3))

# Test 17
print(excel_get_sheet_row_col_count(sheet_copy_1))

# Test 18
print(excel_get_sheet_row_or_col_max(sheet_copy_1, 1, mode='row'))

# Test 19
print(excel_get_sheet_row_values(sheet_copy_1, 2))

# Test 20
print(excel_get_sheets_index_name(wb_copy))

# Test 21
print(excel_get_sheets_targets_counts(sheet_copy_1, "平台", "结果"))

# Test 23
print(excel_insert_sheet_columns(sheet_copy_1, 4, 2))

# Test 24
print(excel_insert_sheet_rows(sheet_copy_1, 4, 2))

# Test 25
print(excel_merge_sheet_cells(sheet_copy_1, (2, 4, 5, 4)))

# Test 26
print(excel_replace_sheet_content(sheet_copy_1, "XXXX", "QWE", cols=6))

# Test 28
print(excel_set_sheet_alignment(sheet_copy_1, (2, 4, 5, 4), horizontal="left", vertical="center"))

# Test 29
print(excel_set_sheet_bold(sheet_copy_1, (2, 4, 5, 4)))

# Test 30
print(excel_set_sheet_cell_value(sheet_copy_1, 4, 1, "QQ"))

# Test 31
print(excel_set_sheet_fill_color(sheet_copy_1, (2, 4, 5, 4),  "FFFF00"))

# Test 32
print(excel_set_sheet_font_color(sheet_copy_1, (2, 4, 5, 4),  "FF0000"))

# Test 33
print(excel_set_sheet_font_size(sheet_copy_1, (2, 4, 5, 4),  16))

# Test 34
print(excel_set_sheet_freeze_panes(sheet_copy_1, "C2"))

# Test 34
print(excel_unmerge_sheet_cells(sheet_copy_1, (2, 4, 5, 4)))

# Test 27
print(excel_save_workbook(wb_copy))

# Test 4
excel_delete_file(copy_excel)
```