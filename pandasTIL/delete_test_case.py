import sys
import data_keypart as keypart
from data_conn import db_connecting


def decimal_to_str(df):
    list_no = [str(no) for no in df.exp_no.tolist()]
    str_no = ",".join(list_no)
    return str_no

def get_exp_no(item_no,del_keyword):
    exp_no_sql =  "SELECT exp_no FROM exp WHERE exp_no LIKE '"+str(item_no)+"%' AND exp_display_no LIKE '%"+ del_keyword+"%'"
    exp_no_df = db_conn.query_excecute(exp_no_sql)
    exp_no_str = decimal_to_str(exp_no_df)
    return exp_no_str

def delete_exp_sql(exp_no_str_list):
    sql = f"DELETE exp WHERE exp_no IN ({exp_no_str_list})\r\n"
    out.write(sql)
    return sql 

def get_part_no(col_part,tbl_part,exp_no_str_list):
    exp_partno_sql = f"SELECT exp_{col_part}_no AS exp_no FROM exp_ti_{tbl_part} WHERE exp_no IN ({exp_no_str_list})"
    part_no_df = db_conn.query_excecute(exp_partno_sql)
    part_no_str = decimal_to_str(part_no_df)
    return part_no_str

def delete_exp_part_sql(tbl_part,exp_no_str_list):
    sql = f"DELETE exp_ti_{tbl_part} WHERE exp_no IN({exp_no_str_list}) \r\n"
    out.write(sql)
    return sql 

def delete_part_sql(col_part,tbl_part,tbl,part_no_str_list):
    sql = f"DELETE exp_ti_{tbl_part}_{tbl} WHERE exp_{col_part}_no IN ({part_no_str_list}) \r\n"
    out.write(sql)
    return sql

def delete_charged_cond(del_keyword):
    wh = f"ti_cell_chargede_cond_code LIKE '%{del_keyword}%'"
    sql = f"DELETE ti_cell_chargede_cond WHERE {wh} \r\n DELETE exp_ti_cell_property_cycle WHERE {wh}\r\n "
    out.write(sql)
    relate_sql =  f"exp_ti_cell_cycle_no in (SELECT exp_ti_cell_cycle_no FROM exp_ti_cell_property_cycle WHERE ti_cell_chargede_cond_code LIKE '%{del_keyword}%') "
    return relate_sql

def delete_cell(cycle_no , del_keyword):
    sql = f"DELETE  exp_ti_cell_property WHERE {cycle_no} \r\n DELETE exp_ti_cell_summary WHERE {cycle_no}"
    out.write(sql)
    relset_sql = f"DELETE exp_ti_relset WHERE cell_lot_no LIKE '%{del_keyword}%' "
    out.write(relset_sql)
    return sql, relset_sql

out = open('../data/datastdout.txt', 'w')
db_conn = db_connecting() 
key_dict = keypart.ti_dict
part_list = ["comp","process","property"]
item_id_list = list(key_dict.keys())

def delete_part_all(keyword):
    for item_id in item_id_list[:5]:
        COL = key_dict[item_id][0]
        TBL = key_dict[item_id][2]
        exp_no = get_exp_no(item_id,keyword)
        part_no = get_part_no(COL,TBL,exp_no)
        for part in part_list : 
            delete_part_sql(COL,TBL,part,part_no)
        delete_exp_part_sql(TBL,exp_no)
        delete_exp_sql(exp_no)
    exp_ti_cell_cycle_no = delete_charged_cond(keyword)
    delete_cell(exp_ti_cell_cycle_no,keyword)
    return out


delete_part_all('TEST-03')


