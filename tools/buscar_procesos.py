import requests
from datetime import date

def buscar_procesos(fecha=None):
    if fecha is None:
        fecha = date.today().isoformat()

    url = "https://contratacionesabiertas.oece.gob.pe/api/v1/releases"
    params = {
        "startDate": fecha,
        "endDate": fecha,
        "mainProcurementCategory": "services",
        "sourceId": "seace_v3",
        "order": "desc"
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"❌ Error al consultar la API: {e}")
        return []

    releases = data.get("releases", [])
    if not releases:
        print(f"⚠️  No se encontraron procesos para la fecha {fecha}")
        return []

    procesos = []
    ocids_vistos = set()
    
    for r in releases:
        tender = r.get("tender", {})
        buyer = r.get("buyer", {})
        value = tender.get("value", {})

        ocid = r.get("ocid", "")
        if ocid in ocids_vistos:
            continue
        ocids_vistos.add(ocid)

        proceso = {
            "ocid": ocid,
            "titulo": tender.get("title", "Sin título"),
            "descripcion": tender.get("description", ""),
            "entidad": buyer.get("name", ""),
            "monto": value.get("amount_PEN", 0),
            "fecha_limite": tender.get("tenderPeriod", {}).get("endDate", ""),
            "fuente": "seace_v3"
        }
        procesos.append(proceso)

    print(f"✅ {len(procesos)} procesos encontrados para {fecha}")
    return procesos