import os
import sys

import pandas as pd
from spark_dataframe_tools import get_color_b

pd.options.mode.copy_on_write = True


def get_dataframe_catalog_nivel():
    df_catalogo_nivel = [
        {"CODE": "01", "DESC": "DAAS PERU SPARK", "SHOR_NAME": "SPARK", "DEFAULT": "YES"},
        {"CODE": "02", "DESC": "DAAS PERU MONITORING USER", "SHOR_NAME": "MONITORING USER", "DEFAULT": "YES"},
        {"CODE": "04", "DESC": "DAAS PERU EGRESSION DECRYPTION", "SHOR_NAME": "EGRESSION DECRYPTION", "DEFAULT": "YES"},
        {"CODE": "15", "DESC": "DAAS PERU DATAPROC USER READ", "SHOR_NAME": "DATAPROC USER READ", "DEFAULT": "YES"},
        {"CODE": "21", "DESC": "DAAS PERU DATAPROC USER", "SHOR_NAME": "DATAPROC USER", "DEFAULT": "YES"},
        {"CODE": "26", "DESC": "DAAS PERU DEVELOPER", "SHOR_NAME": "DEVELOPER", "DEFAULT": "NO"},
        {"CODE": "27", "DESC": "DAAS PERU DATA ARCHITECT", "SHOR_NAME": "DATA ARCHITECT", "DEFAULT": "NO"},
        {"CODE": "28", "DESC": "DAAS PERU GDRIVE", "SHOR_NAME": "GDRIVE", "DEFAULT": "NO"},
        {"CODE": "29", "DESC": "DAAS PERU XDATA", "SHOR_NAME": "XDATA", "DEFAULT": "NO"},
        {"CODE": "30", "DESC": "DAAS PERU DATA SCIENTIST", "SHOR_NAME": "DATA SCIENTIST", "DEFAULT": "NO"},
        {"CODE": "31", "DESC": "DAAS PERU PROCESS MANAGER", "SHOR_NAME": "PROCESS MANAGER", "DEFAULT": "NO"},
        {"CODE": "32", "DESC": "DAAS PERU MICROSTRATEGY", "SHOR_NAME": "MICROSTRATEGY", "DEFAULT": "NO"},
        {"CODE": "33", "DESC": "DAAS PERU DISCOVERY", "SHOR_NAME": "DISCOVERY", "DEFAULT": "NO"},
        {"CODE": "34", "DESC": "DAAS PERU VBOX", "SHOR_NAME": "VBOX", "DEFAULT": "NO"},
        {"CODE": "35", "DESC": "DAAS PERU SANDBOX", "SHOR_NAME": "SANDBOX ADMIN", "DEFAULT": "NO"},
        {"CODE": "36", "DESC": "DAAS PERU HISTORY SERVER", "SHOR_NAME": "HISTORYSERVER", "DEFAULT": "NO"},
        {"CODE": "37", "DESC": "DAAS PERU HISTORY SERVER3", "SHOR_NAME": "HISTORYSERVER3", "DEFAULT": "NO"},
        {"CODE": "38", "DESC": "DAAS PERU FILE EXPLORER", "SHOR_NAME": "FILE EXPLORER", "DEFAULT": "NO"},
        {"CODE": "39", "DESC": "DAAS PERU VISUALIZER", "SHOR_NAME": "VISUALIZADOR", "DEFAULT": "NO"},
        {"CODE": "40", "DESC": "DAAS PERU INTELLIGENCE INSTANCE", "SHOR_NAME": "INTELLIGENCE INSTANCE", "DEFAULT": "NO"},
        {"CODE": "41", "DESC": "DAAS PERU INTELLIGENCE SERVICE USER", "SHOR_NAME": "INTELLIGENCE USER", "DEFAULT": "NO"},
        {"CODE": "42", "DESC": "DAAS PERU MIGRATION", "SHOR_NAME": "MIGRATION", "DEFAULT": "NO"}
    ]
    df = pd.DataFrame(df_catalogo_nivel)
    return df


def get_catalog_nivel(description):
    description = str(description).upper().strip()

    df = get_dataframe_catalog_nivel()
    result = df[df['SHOR_NAME'] == description]

    rs = dict(CODE="", DESC="")
    try:
        rs['CODE'] = result['CODE'].iloc[0]
        rs['DESC'] = result['DESC'].iloc[0]
    except BaseException:
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


def get_acl(path, uuaa_desc):
    path = str(path).lower().strip()
    uuaa_desc = str(uuaa_desc).upper().strip()
    path_split = path.split("/")
    path_target = str(path_split[4])

    rs = dict(ID_RECURSO="", TARGET_RECURSO="")
    if path_target == "app" and uuaa_desc == "PROJECT":
        uuaa_name = str(path_split[5])
        if len(uuaa_name) == 4:
            uuaa_name = uuaa_name
        else:
            uuaa_name = "NOT_UUAA"

        path_unique = "-".join(path_split[7:])
        if path_unique == f"dataproc-streaming":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}STRE"
        elif path_unique == f"dataproc-batch":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}BATC"
        elif path_unique == f"dataproc-resources":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}RESO"
        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()

    elif path_target == "data" and uuaa_desc == "PROJECT":
        path_unique = "-".join(path_split[5:])
        uuaa_name = str(path_split[6])

        if len(uuaa_name) == 4:
            uuaa_name = uuaa_name
        else:
            uuaa_name = "NOT_UUAA"

        if path_unique == f"raw-{uuaa_name}-refusals":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}RRFL"
        elif path_unique == f"raw-{uuaa_name}-data":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}RDAT"

        elif path_unique == f"raw-{uuaa_name}-datatmp":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}RDTM"

        elif path_unique == f"raw-external-datatmp":
            struct_acl = f"DAS_PE_DATM_REDTM"

        elif path_unique == f"master-external-datatmp":
            struct_acl = f"DAS_PE_DATM_MEDTM"

        elif path_unique == f"master-dq":
            struct_acl = f"DAS_PE_DATM_MDQ"
        elif path_unique == f"master-{uuaa_name}-data":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}MDAT"

        elif path_unique == f"master-{uuaa_name}-schemas":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}MSHM"

        elif path_unique == f"master-{uuaa_name}-data-l1t":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}ML1T"
        elif path_unique == f"share-{uuaa_name}-datatmp":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}SDTM"
        elif path_unique == f"master-{uuaa_name}-datatmp":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}MDTM"
        elif path_unique == f"master-{uuaa_name}-refusals":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}MRFL"
        elif path_unique == f"master-p{uuaa_name}-refusals-dq":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}MRFLDQ"
        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()

    elif path_target == "in" and uuaa_desc == "PROJECT":
        path_unique = "-".join(path_split[5:])

        if len(path_split[5:]) == 3:
            uuaa_name = str(path_split[7])
        elif len(path_split[5:]) == 4:
            uuaa_name = str(path_split[8])
        else:
            uuaa_name = ""
        if len(uuaa_name) == 4:
            uuaa_name = uuaa_name
        else:
            uuaa_name = "NOT_UUAA"

        if path_unique == f"staging-datax-{uuaa_name}":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}INST"

        elif path_unique == f"staging-ratransmit-external-{uuaa_name}":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}INRA"

        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()

    elif path_target == "logs" and uuaa_desc == "PROJECT":
        path_unique = "-".join(path_split[5:])
        if path_unique == f"historyserver":
            struct_acl = f"DAS_PE_DATM_LOHR"
        elif path_unique == f"historyserver3":
            struct_acl = f"DAS_PE_DATM_LOH3"
        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()

    elif path_target == "out" and uuaa_desc == "PROJECT":
        path_unique = "-".join(path_split[5:])
        uuaa_name = str(path_split[7])
        if len(uuaa_name) == 4:
            uuaa_name = uuaa_name
        else:
            uuaa_name = "NOT_UUAA"

        if path_unique == f"staging-ratransmit-{uuaa_name}":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}OUST"
        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()

    elif path_target == "argos-front" and uuaa_desc == "PROJECT":
        path_unique = "-".join(path_split[4:])
        if path_unique == f"argos-front-dcos-userland":
            struct_acl = f"DAS_PE_ARGF_DCOSUSER"
        elif path_unique == f"argos-front-jobs-report":
            struct_acl = f"DAS_PE_ARGF_JOBSREPO"
        elif path_unique == f"argos-front-jobs-status":
            struct_acl = f"DAS_PE_ARGF_JOBSSTAT"
        elif path_unique == f"argos-front-juanitor":
            struct_acl = f"DAS_PE_ARGF_JUANITOR"
        elif path_unique == f"argos-front-logs":
            struct_acl = f"DAS_PE_ARGF_LOGS"
        elif path_unique == f"argos-front-mesos-tasks":
            struct_acl = f"DAS_PE_ARGF_MESOSTAS"
        elif path_unique == f"argos-front-task-logs":
            struct_acl = f"DAS_PE_ARGF_TASKLOGS"
        elif path_unique == f"argos-front-tpt-logs":
            struct_acl = f"DAS_PE_ARGF_TPTLOGS"
        elif path_unique == f"argos-front-alerts":
            struct_acl = f"DAS_PE_ARGF_ALERTS"
        elif path_unique == f"argos-front-alerts-store":
            struct_acl = f"DAS_PE_ARGF_ALERTSST"
        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()
    elif path_target == "dataproc-ui" and uuaa_desc == "PROJECT":
        path_unique = "-".join(path_split[4:])
        if path_unique == f"dataproc-ui":
            struct_acl = f"DAS_PE_DATM_DATAPRUI"
        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()

    elif path_target == "discovery" and uuaa_desc == "PROJECT":
        path_unique = "-".join(path_split[4:])
        if path_unique == f"discovery":
            struct_acl = f"DAS_PE_DATM_DISCOVER"
        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()

    elif path_target == "microstrategy" and uuaa_desc == "PROJECT":
        path_unique = "-".join(path_split[4:])
        if path_unique == f"microstrategy":
            struct_acl = f"DAS_PE_DATM_MICRPSTR"
        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()

    elif path_target == "sandbox" and uuaa_desc == "PROJECT":
        path_unique = "-".join(path_split[4:])
        if path_unique == f"sandbox":
            struct_acl = f"DAS_PE_DATM_SANDBOX"
        else:
            struct_acl = ""
        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()

    elif path_target == "data" and uuaa_desc == "SANDBOX":
        path_unique = "-".join(path_split[5:])

        uuaa_name = "NOT_UUAA"
        table_name = "NOT_TABLE"

        if len(path_split[5:]) == 3:
            uuaa_name = str(path_split[6])
        elif len(path_split[5:]) == 4:
            uuaa_name = str(path_split[6])
        elif len(path_split[5:]) == 5:
            uuaa_name = str(path_split[6])
            table_name = str(path_split[8])
        else:
            uuaa_name = "NOT_UUAA"
            table_name = "NOT_TABLE"

        if len(uuaa_name) == 4:
            uuaa_name = uuaa_name

        if path_unique == f"sandboxes-{uuaa_name}-data":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}SDAT"
        elif path_unique == f"sandboxes-{uuaa_name}-models":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}SMDS"
        elif path_unique == f"sandboxes-{uuaa_name}-archived":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}SAHV"
        elif path_unique == f"sandboxes-{uuaa_name}-xdata":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}SXDT"
        elif path_unique == f"sandboxes-{uuaa_name}-historyserver":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}SOHR"
        elif path_unique == f"sandboxes-{uuaa_name}-upload":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}SUPL"

        elif path_unique == f"master-{uuaa_name}-data":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}MDAT"
        elif path_unique == f"master-{uuaa_name}-data-l1t":
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}ML1T"
        elif path_unique == f"master-{uuaa_name}-data-{table_name}-l3":
            table_name_tag = "".join(table_name.split("_")[2:])
            struct_acl = f"DAS_PE_DATM_{uuaa_name.upper()}_{table_name_tag}ML3"
        else:
            struct_acl = ""

        rs["ID_RECURSO"] = struct_acl
        rs["TARGET_RECURSO"] = path_target.upper()
    else:
        rs["ID_RECURSO"] = ""
        rs["TARGET_RECURSO"] = ""
    return rs


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


def classification_id_resource(path_name, uuaa_desc):
    path_name = str(path_name).lower().strip()
    if path_name not in ("", None):
        acl_name = get_acl(path_name, uuaa_desc)
        return acl_name["ID_RECURSO"]
    else:
        return ""


def classification_target_resource(path_name, uuaa_desc):
    path_name = str(path_name).lower().strip()
    if path_name not in ("", None):
        acl_name = get_acl(path_name, uuaa_desc)
        return acl_name["TARGET_RECURSO"]
    else:
        return ""


def generate_profiling(file_excel=None, wo=None):
    data = pd.read_excel(file_excel, sheet_name="ACL", engine='openpyxl')
    df1 = data.iloc[:, 0:7]
    df1.columns = map(lambda x: str(x).strip().upper(), df1.columns)

    df1['UUAA_NAME'] = df1.apply(lambda x: classification_uuaa_name(project=x["PROJECT"]), axis=1)
    df1['UUAA_DESC'] = df1.apply(lambda x: classification_uuaa_desc(project=x["PROJECT"]), axis=1)
    df1['TARGET_RECURSO'] = df1.apply(lambda x: classification_target_resource(path_name=x["PATH"], uuaa_desc=x["UUAA_DESC"]), axis=1)
    df1['ID_RECURSO'] = df1.apply(lambda x: classification_id_resource(path_name=x["PATH"], uuaa_desc=x["UUAA_DESC"]), axis=1)
    df1['TIPO_RECURSO'] = df1['PERMISSIONS'].apply(classification_type_resource)
    df1['LONGITUD_RECURSO'] = df1['ID_RECURSO'].apply(lambda x: len(str(x)))
    df1['ID_COLECTIVO'] = df1.apply(lambda x: classification_id_collective(description=x["DESCRIPTION"], group=x["GROUP"]), axis=1)
    df1['NOMBRE_COLECTIVO'] = df1.apply(lambda x: classification_name_collective(group=x["GROUP"]), axis=1)
    df1['ID_CONTENIDO'] = df1.apply(lambda x: classification_id_content(uuaa_name=x["UUAA_NAME"], uuaa_desc=x["UUAA_DESC"]), axis=1)
    df1['NOMBRE_CONTENIDO'] = df1.apply(lambda x: classification_name_content(uuaa_name=x["UUAA_NAME"]), axis=1)
    df1['ID_NIVEL'] = df1.apply(lambda x: classification_id_nivel(uuaa_name=x["UUAA_NAME"], description=x["DESCRIPTION"]), axis=1)
    df1['NOMBRE_NIVEL'] = df1.apply(lambda x: classification_name_nivel(uuaa_name=x["UUAA_NAME"], description=x["DESCRIPTION"]), axis=1)

    df_catalog_nivel = get_dataframe_catalog_nivel()
    df_catalog_nivel.loc[:, 'NOMBRE'] = df_catalog_nivel["DESC"]
    df_catalog_nivel.loc[:, 'DESCRIPCION'] = df_catalog_nivel["DESC"]
    df_catalog_nivel.loc[:, 'NRO MAX USUARIO'] = "0"
    df_catalog_nivel.loc[:, 'TOLERANCIA'] = "ACTIVA"

    df_contenido_nivel_colectivo = df1[['ID_CONTENIDO', 'ID_NIVEL', 'NOMBRE_NIVEL', 'ID_COLECTIVO', 'NOMBRE_COLECTIVO']]
    df_contenido_nivel_colectivo.loc[:, 'UUAA'] = "9993"
    df_contenido_nivel_colectivo = df_contenido_nivel_colectivo[["ID_CONTENIDO", "ID_NIVEL", "NOMBRE_NIVEL", "UUAA", "ID_COLECTIVO", "NOMBRE_COLECTIVO"]]
    df_contenido_nivel_colectivo = df_contenido_nivel_colectivo.drop_duplicates().reset_index(drop=True)
    df_contenido_nivel_colectivo = df_contenido_nivel_colectivo.sort_values(['ID_CONTENIDO', 'ID_NIVEL', 'ID_COLECTIVO'], ascending=[True, True, True])

    df_recurso = df1[['ID_RECURSO', 'TIPO_RECURSO', 'PATH']]
    df_recurso.loc[:, 'NOMBRE RECURSO'] = df_recurso["PATH"]
    df_recurso.loc[:, 'UUAA'] = "9993"
    df_recurso.loc[:, 'AMBIENTE'] = "DATA AS SERVICE PERU"
    df_recurso = df_recurso[["ID_RECURSO", "NOMBRE RECURSO", "UUAA", "AMBIENTE", "TIPO_RECURSO"]]
    df_recurso = df_recurso.drop_duplicates().reset_index(drop=True)
    df_recurso = df_recurso.sort_values(['ID_RECURSO', 'TIPO_RECURSO'], ascending=[True, False])

    df_colectivo = df1[['ID_COLECTIVO', 'NOMBRE_COLECTIVO']]
    df_colectivo.loc[:, 'GESTOR RESPONSABLE'] = "PAIS - PERU"
    df_colectivo.loc[:, 'DESCRIPCION'] = df_colectivo["NOMBRE_COLECTIVO"]
    df_colectivo = df_colectivo.drop_duplicates().reset_index(drop=True)
    df_colectivo = df_colectivo.sort_values(['ID_COLECTIVO'], ascending=[True])

    df_colectivo_grupo = df1[['GROUP', 'ID_COLECTIVO', 'NOMBRE_COLECTIVO']]
    df_colectivo_grupo.loc[:, 'ENTORNO'] = "E.PREVIOUS / PRODUCTION"
    df_colectivo_grupo.loc[:, 'AMBIENTE'] = "DATA AS SERVICE PERU"
    df_colectivo_grupo.loc[:, 'TIPO CONNECTOR'] = "FIJO"
    df_colectivo_grupo = df_colectivo_grupo.drop_duplicates().reset_index(drop=True)
    df_colectivo_grupo = df_colectivo_grupo.sort_values(['GROUP', 'ID_COLECTIVO'], ascending=[True, True])

    df_contenido = df1[['ID_CONTENIDO', 'NOMBRE_CONTENIDO']]
    df_contenido.loc[:, 'GESTOR RESPONSABLE'] = "PAIS - PERU"
    df_contenido.loc[:, 'CLASE'] = "TECNICA"
    df_contenido.loc[:, 'SEGURIDAD INTERNA'] = "NO"
    df_contenido.loc[:, 'CONFIDENCIALIDAD'] = "NO"
    df_contenido.loc[:, 'CONTENIDO SENSIBLE'] = "NO"
    df_contenido.loc[:, 'DESCRIPCION'] = df_contenido["NOMBRE_CONTENIDO"]
    df_contenido.loc[:, 'UUAA'] = "9993"
    df_contenido.loc[:, 'ALIAS APLICACION'] = df_contenido["NOMBRE_CONTENIDO"]
    df_contenido.loc[:, 'LINK DOC. OFICIALES'] = "-"
    df_contenido.loc[:, 'INFO TECNICA'] = "-"
    df_contenido.loc[:, 'AREA SOLICITANTE'] = "-"
    df_contenido.loc[:, 'OTROS INTERVINIENTES'] = "-"
    df_contenido.loc[:, 'DOC. CONTENIDO/USUARIO'] = "-"
    df_contenido = df_contenido.drop_duplicates().reset_index(drop=True)
    df_contenido = df_contenido.sort_values(['ID_CONTENIDO'], ascending=[True])

    df_recurso_contenido_nivel = df1[['ID_RECURSO', 'PATH', 'TIPO_RECURSO', 'ID_CONTENIDO', 'ID_NIVEL', 'NOMBRE_NIVEL']]
    df_recurso_contenido_nivel = df_recurso_contenido_nivel.drop_duplicates().reset_index(drop=True)
    df_recurso_contenido_nivel = df_recurso_contenido_nivel.sort_values(['ID_RECURSO', "ID_CONTENIDO", "ID_NIVEL"], ascending=[True, True, True])

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
    df1.to_excel(writer, sheet_name="original_processing", index=False)
    df_catalog_nivel.to_excel(writer, sheet_name="catalog_nivel", index=False)
    df_contenido_nivel_colectivo.to_excel(writer, sheet_name="contenido_nivel_colectivo", index=False)
    df_recurso.to_excel(writer, sheet_name="recurso", index=False)
    df_recurso_contenido_nivel.to_excel(writer, sheet_name="recurso_preasignacion", index=False)
    df_colectivo.to_excel(writer, sheet_name="colectivo", index=False)
    df_colectivo_grupo.to_excel(writer, sheet_name="colectivo_grupo", index=False)
    df_contenido.to_excel(writer, sheet_name="contenido", index=False)

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
