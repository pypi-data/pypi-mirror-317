import os
import sys

import pandas as pd
from spark_dataframe_tools import get_color_b

pd.options.mode.copy_on_write = True


def get_catalog_nivel(description):
    description = str(description).lower().strip()
    rs = dict(CODE="", DESC="")
    if description == "spark":
        rs["CODE"] = "01"
        rs["DESC"] = "DAAS PERU SPARK"
    elif description == "monitoring user":
        rs["CODE"] = "02"
        rs["DESC"] = "DAAS PERU MONITORING USER"
    elif description == "data architect":
        rs["CODE"] = "03"
        rs["DESC"] = "DAAS PERU DATA ARCHITECT"
    elif description == "egression decryption":
        rs["CODE"] = "04"
        rs["DESC"] = "DAAS PERU EGRESSION DECRYPTION"
    elif description == "microstategy":
        rs["CODE"] = "05"
        rs["DESC"] = "DAAS PERU MICROSTRATEGY"
    elif description == "process manager":
        rs["CODE"] = "06"
        rs["DESC"] = "DAAS PERU PM PRODUCTIVO"
    elif description == "vbox":
        rs["CODE"] = "07"
        rs["DESC"] = "DAAS PERU VBOX"
    elif description == "history server":
        rs["CODE"] = "09"
        rs["DESC"] = "DAAS PERU HISTORY SERVER"
    elif description == "xdata":
        rs["CODE"] = "10"
        rs["DESC"] = "DAAS PERU XDATA"
    elif description == "visualizador":
        rs["CODE"] = "11"
        rs["DESC"] = "DAAS PERU VISUALIZADOR"
    elif description == "dataproc user read":
        rs["CODE"] = "15"
        rs["DESC"] = "DAAS PERU DATAPROC USER READ"
    elif description == "data scientist":
        rs["CODE"] = "16"
        rs["DESC"] = "DAAS PERU DATA SCIENTIST"
    elif description == "dataproc user":
        rs["CODE"] = "21"
        rs["DESC"] = "DAAS PERU DATAPROC USER"
    elif description == "developer":
        rs["CODE"] = "26"
        rs["DESC"] = "DAAS PERU DEVELOPER"
    else:
        rs["CODE"] = ""
        rs["DESC"] = ""
    return rs


def get_uuaa(project):
    project = str(project).lower().strip()
    rs = dict(UUAA_NAME="", UUAA_DESC="")

    if project.startswith(("project", "sandbox")):
        if project.startswith("project"):
            rs["UUAA_NAME"] = str(project.split(":")[1]).upper().strip()
            rs["UUAA_DESC"] = "PROJECT"
        else:
            rs["UUAA_NAME"] = str(project.split(" ")[1]).upper().strip()
            rs["UUAA_DESC"] = "SANDBOX"
        return rs
    else:
        return rs


def get_acl(path, uuaa_name, uuaa_desc):
    path = str(path).lower().strip()
    uuaa_name = str(uuaa_name).upper().strip()
    uuaa_desc = str(uuaa_desc).upper().strip()
    path_split = path.split("/")
    path_target = str(path_split[4])

    rs = dict(ID_RECURSO="", TARGET_RECURSO="")
    if path_target == "app" and uuaa_desc == "PROJECT":
        path_target1 = str(str(path_split[7])[0:3]).upper()
        path_target2 = str(str(path_split[7])[4:5]).upper()
        path_target3 = str(str(path_split[8])[0:4]).upper()
        rs["ID_RECURSO"] = f"DAS_PE_{uuaa_name}_{path_target1}{path_target2}{path_target3}"
        rs["TARGET_RECURSO"] = path_target.upper()
    elif path_target == "data" and uuaa_desc == "PROJECT":
        storage = str(path_split[5]).upper()
        if storage == "RAW":
            uuaa_name = uuaa_name
        path_target1 = str(str(path_split[5])[0:3]).upper()
        path_target2 = str(str(path_split[7])[0:4]).upper()
        rs["ID_RECURSO"] = f"DAS_PE_{uuaa_name}_{path_target1}{path_target2}"
        rs["TARGET_RECURSO"] = path_target.upper()
    elif path_target == "in" and uuaa_desc == "PROJECT":
        path_target1 = str(str(path_split[4])[0:2]).upper()
        path_target2 = str(str(path_split[5])[0:2]).upper()
        path_target3 = str(str(path_split[6])[0:3]).upper()
        path_target4 = str(str(path_split[6])[4:5]).upper()
        rs["ID_RECURSO"] = f"DAS_PE_{uuaa_name}_{path_target1}{path_target2}{path_target3}{path_target4}"
        rs["TARGET_RECURSO"] = path_target.upper()
    elif path_target == "logs" and uuaa_desc == "PROJECT":
        path_target1 = str(str(path_split[4])[0:3]).upper()
        path_target2 = str(str(path_split[5])[0:5]).upper()
        rs["ID_RECURSO"] = f"DAS_PE_{uuaa_name}_{path_target1}{path_target2}"
        rs["TARGET_RECURSO"] = path_target.upper()
    elif path_target == "out" and uuaa_desc == "PROJECT":
        path_target1 = str(str(path_split[4])[0:2]).upper()
        path_target2 = str(str(path_split[5])[0:2]).upper()
        path_target3 = str(str(path_split[6])[0:4]).upper()
        rs["ID_RECURSO"] = f"DAS_PE_{uuaa_name}_{path_target1}{path_target2}{path_target3}"
        rs["TARGET_RECURSO"] = path_target.upper()
    elif path_target == "argos-front" and uuaa_desc == "PROJECT":
        path_argos_text = str(path_split[5]).replace("-", "").strip()
        path_target1 = str(str(path_split[4])[0:3]).upper()
        path_target2 = str(str(path_split[4])[6:7]).upper()
        uuaa_name = f"{path_target1}{path_target2}"
        path_target3 = str(str(path_argos_text)[0:3]).upper()
        path_target4 = str(str(path_argos_text)[4:9]).upper()
        rs["ID_RECURSO"] = f"DAS_PE_{uuaa_name}_{path_target3}{path_target4}"
        rs["TARGET_RECURSO"] = path_target.upper()
    elif path_target == "dataproc-ui" and uuaa_desc == "PROJECT":
        path_target1 = str(str(path_split[4])[0:3]).upper()
        path_target2 = str(str(path_split[4])[4:5]).upper()
        uuaa_name = f"{path_target1}{path_target2}"
        path_target3 = str(str(path_split[4])[0:3]).upper()
        path_target4 = str(str(path_split[4])[9:11]).upper()
        rs["ID_RECURSO"] = f"DAS_PE_{uuaa_name}_{path_target3}{path_target4}"
        rs["TARGET_RECURSO"] = path_target.upper()
    elif path_target == "data" and uuaa_desc == "SANDBOX":
        path_target1 = str(str(path_split[5])[0:3]).upper()
        path_target2 = str(str(path_split[-1])[0:5]).upper()
        rs["ID_RECURSO"] = f"DAS_PE_{uuaa_name}_{path_target1}{path_target2}"
        rs["TARGET_RECURSO"] = path_target.upper()
    else:
        rs["ID_RECURSO"] = ""
        rs["TARGET_RECURSO"] = ""
    return rs["ID_RECURSO"]


def classification_uuaa_name(project):
    project = str(project).lower().strip()
    if project not in ("", None):
        id_uuaa = get_uuaa(project)
        return id_uuaa["UUAA_NAME"]
    else:
        return ""


def classification_uuaa_desc(project):
    project = str(project).lower().strip()
    if project not in ("", None):
        id_uuaa = get_uuaa(project)
        return id_uuaa["UUAA_DESC"]
    else:
        return ""


def classification_type_resource(permission):
    if permission == "R":
        return "DAAS RESOURCE READ ONLY"
    else:
        return "DAAS RESOURCE READ AND WRITE"


def classification_id_collective(description, group):
    description = str(description).lower()
    group = str(group).upper()
    if description.strip() in ('spark', 'egression decryption', 'monitoring user', 'dataproc user', 'vbox',
                               "developer", 'dataproc user read', 'data scientist', 'process manager', 'xdata'):

        id_colectivo = f"D_{group[6:8]}{group[9:15]}"
        return id_colectivo
    else:
        return ""


def classification_name_collective(group):
    if group not in ("", None):
        nombre_colectivo = f"DAAS PERU {group.upper()}"
        return nombre_colectivo
    else:
        return ""


def classification_id_content(uuaa_name, uuaa_desc):
    if uuaa_name not in ("", None):
        if uuaa_name == "VBOX" or uuaa_desc == "SANDBOX":
            id_contenido = f"SAND{uuaa_name.upper()}"
        else:
            id_contenido = f"P{uuaa_name.upper()}"
        return id_contenido
    else:
        return ""


def classification_name_content(uuaa_name):
    if uuaa_name not in ("", None):
        nombre_contenido = f"DAAS PERU {uuaa_name.upper()}"
        return nombre_contenido
    else:
        return ""


def classification_id_nivel(uuaa_name, description):
    description = str(description).lower().strip()
    if uuaa_name not in ("", None):
        catalog_nivel = get_catalog_nivel(description)
        return catalog_nivel["CODE"]
    else:
        return ""


def classification_name_nivel(uuaa_name, description):
    description = str(description).lower().strip()
    if uuaa_name not in ("", None):
        catalog_nivel = get_catalog_nivel(description)
        return catalog_nivel["DESC"]
    else:
        return ""


def classification_id_resource(path_name, uuaa_name, uuaa_desc):
    path_name = str(path_name).lower().strip()
    if path_name not in ("", None):
        acl_name = get_acl(path_name, uuaa_name, uuaa_desc)
        return acl_name
    else:
        return ""


def generate_profiling(file_excel=None, wo=None):
    data = pd.read_excel(file_excel, sheet_name="ACL", engine='openpyxl')
    df1 = data.iloc[:, 0:7]
    df1.columns = map(lambda x: str(x).strip().upper(), df1.columns)

    df1['UUAA_NAME'] = df1.apply(lambda x: classification_uuaa_name(project=x["PROJECT"]), axis=1)
    df1['UUAA_DESC'] = df1.apply(lambda x: classification_uuaa_desc(project=x["PROJECT"]), axis=1)
    df1['ID_RECURSO'] = df1.apply(lambda x: classification_id_resource(path_name=x["PATH"], uuaa_name=x["UUAA_NAME"], uuaa_desc=x["UUAA_DESC"]), axis=1)
    df1['TIPO_RECURSO'] = df1['PERMISSIONS'].apply(classification_type_resource)
    df1['ID_COLECTIVO'] = df1.apply(lambda x: classification_id_collective(description=x["DESCRIPTION"], group=x["GROUP"]), axis=1)
    df1['NOMBRE_COLECTIVO'] = df1.apply(lambda x: classification_name_collective(group=x["GROUP"]), axis=1)
    df1['ID_CONTENIDO'] = df1.apply(lambda x: classification_id_content(uuaa_name=x["UUAA_NAME"], uuaa_desc=x["UUAA_DESC"]), axis=1)
    df1['NOMBRE_CONTENIDO'] = df1.apply(lambda x: classification_name_content(uuaa_name=x["UUAA_NAME"]), axis=1)
    df1['ID_NIVEL'] = df1.apply(lambda x: classification_id_nivel(uuaa_name=x["UUAA_NAME"], description=x["DESCRIPTION"]), axis=1)
    df1['NOMBRE_NIVEL'] = df1.apply(lambda x: classification_name_nivel(uuaa_name=x["UUAA_NAME"], description=x["DESCRIPTION"]), axis=1)
    df1['NOMBRE_COLECTIVO'] = df1.apply(lambda x: classification_name_collective(group=x["GROUP"]), axis=1)

    df_recurso = df1[['ID_RECURSO', 'TIPO_RECURSO']]
    df_recurso = df_recurso.drop_duplicates().reset_index(drop=True)

    df_colectivo = df1[['ID_COLECTIVO', 'NOMBRE_COLECTIVO']]
    df_colectivo = df_colectivo.drop_duplicates().reset_index(drop=True)

    df_grupo_colectivo = df1[['GROUP', 'ID_COLECTIVO', 'NOMBRE_COLECTIVO']]
    df_grupo_colectivo = df_grupo_colectivo.drop_duplicates().reset_index(drop=True)

    df_contenido_nivel_colectivo = df1[['ID_CONTENIDO', 'ID_NIVEL', 'ID_COLECTIVO', 'NOMBRE_COLECTIVO']]
    df_contenido_nivel_colectivo = df_contenido_nivel_colectivo.drop_duplicates().reset_index(drop=True)

    is_windows = sys.platform.startswith('win')
    path_directory = os.path.join("DIRECTORY_PROFILING")
    path_profiling = os.path.join(path_directory, "profiling_acl.xlsx")
    path_template_resource = os.path.join(path_directory, f"{wo}_PLANTILLA_RECURSO.xlsx")
    path_template_pre_assignment = os.path.join(path_directory, f"{wo}_PLANTILLA_PREASIGNACION.xlsx")
    path_template_previous = os.path.join(path_directory, f"{wo}_PLANTILLA_EPREVIOUS.xlsx")
    path_template_production = os.path.join(path_directory, f"{wo}_PLANTILLA_EPRODUCCION.xlsx")

    if is_windows:
        path_profiling = path_profiling.replace("\\", "/")
        path_template_resource = path_template_resource.replace("\\", "/")
        path_template_pre_assignment = path_template_pre_assignment.replace("\\", "/")
        path_template_previous = path_template_previous.replace("\\", "/")
        path_template_production = path_template_production.replace("\\", "/")
    if not os.path.exists(path_directory):
        os.makedirs(path_directory)

    writer = pd.ExcelWriter(f"{path_profiling}", engine="xlsxwriter")
    data.to_excel(writer, sheet_name="original", index=False)
    df_recurso.to_excel(writer, sheet_name="recurso", index=False)
    df_colectivo.to_excel(writer, sheet_name="colectivo", index=False)
    df_grupo_colectivo.to_excel(writer, sheet_name="grupo_colectivo", index=False)
    df_contenido_nivel_colectivo.to_excel(writer, sheet_name="contenido_nivel_colectivo", index=False)
    writer.close()
    print(get_color_b(f'Create file: {path_profiling}'))

    df_plantilla_resource = df1[['ID_RECURSO', 'TIPO_RECURSO', "PATH"]]
    df_plantilla_resource.loc[:, 'NOMBRE AMBIENTE'] = "DATA AS SERVICE PERU"
    df_plantilla_resource.loc[:, 'NOMBRE RECURSO'] = df_plantilla_resource["PATH"]
    df_plantilla_resource.loc[:, 'NOMBRE RECURSO EXTENDIDO'] = df_plantilla_resource["PATH"]
    df_plantilla_resource.loc[:, 'UUAA'] = "9993"
    del df_plantilla_resource["PATH"]
    df_plantilla_resource.columns = ["COD RECURSO", "NOMBRE TIPO RECURSO", "NOMBRE AMBIENTE", "NOMBRE RECURSO", "NOMBRE RECURSO EXTENDIDO", "UUAA"]
    df_plantilla_resource.to_excel(f"{path_template_resource}", index=False, sheet_name='PLANTILLA_RECURSO')
    print(get_color_b(f'Create file: {path_template_resource}'))

    df_plantilla_pre_assigment = df1[['ID_CONTENIDO', 'ID_NIVEL', 'ID_RECURSO', 'TIPO_RECURSO']]
    df_plantilla_pre_assigment.loc[:, 'AMBIENTE'] = "DATA AS SERVICE PERU"
    df_plantilla_pre_assigment.loc[:, 'COD CONEXION'] = "MONO"
    df_plantilla_pre_assigment.columns = ["COD CONTENIDO", "COD NIVEL", "COD RECURSO", "TIPO RECURSO", "AMBIENTE", "COD CONEXION"]
    df_plantilla_pre_assigment.to_excel(f"{path_template_pre_assignment}", index=False, sheet_name='PLANTILLA_PREASIGNACION')
    print(get_color_b(f'Create file: {path_template_pre_assignment}'))

    df_plantilla_previous = df1[['ID_CONTENIDO', 'ID_NIVEL', 'ID_RECURSO', 'TIPO_RECURSO']]
    df_plantilla_previous.loc[:, 'AMBIENTE'] = "DATA AS SERVICE PERU"
    df_plantilla_previous.loc[:, 'COD CONEXION'] = "MONO"
    df_plantilla_previous.loc[:, 'ENTORNO DESTINO'] = "E.PREVIOS"
    df_plantilla_previous.columns = ["COD CONTENIDO", "COD NIVEL", "COD RECURSO", "TIPO RECURSO", "AMBIENTE", "COD CONEXION", "ENTORNO DESTINO"]
    df_plantilla_previous.to_excel(f"{path_template_previous}", index=False, sheet_name='PLANTILLA_EPREVIOUS')
    print(get_color_b(f'Create file: {path_template_previous}'))

    df_plantilla_production = df1[['ID_CONTENIDO', 'ID_NIVEL', 'ID_RECURSO', 'TIPO_RECURSO']]
    df_plantilla_production.loc[:, 'AMBIENTE'] = "DATA AS SERVICE PERU"
    df_plantilla_production.loc[:, 'COD CONEXION'] = "MONO"
    df_plantilla_production.loc[:, 'ENTORNO DESTINO'] = "PRODUCCIÓN"
    df_plantilla_production.columns = ["COD CONTENIDO", "COD NIVEL", "COD RECURSO", "TIPO RECURSO", "AMBIENTE", "COD CONEXION", "ENTORNO DESTINO"]
    df_plantilla_production.to_excel(f"{path_template_production}", index=False, sheet_name='PLANTILLA_EPRODUCCION')
    print(get_color_b(f'Create file: {path_template_production}'))
