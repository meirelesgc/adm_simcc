@app.route("/departamento", methods=["POST"])
def create_or_update_departamento():
    data_list = request.form.to_dict(flat=False)
    files = request.files

    insert_sql = """
        INSERT INTO departamento (
            dep_id, org_cod, dep_nom, dep_des, dep_email, dep_site, dep_sigla, dep_tel, img_data
        ) VALUES (
            %(dep_id)s, 
            %(org_cod)s, 
            %(dep_nom)s,
            %(dep_des)s, 
            %(dep_email)s, 
            %(dep_site)s, 
            %(dep_sigla)s, 
            %(dep_tel)s, 
            %(img_data)s
        )
    """

    update_sql = """
        UPDATE departamento SET 
            org_cod=%(org_cod)s, dep_nom=%(dep_nom)s, dep_des=%(dep_des)s, 
            dep_email=%(dep_email)s, dep_site=%(dep_site)s, dep_sigla=%(dep_sigla)s, dep_tel=%(dep_tel)s, 
            img_data=%(img_data)s
        WHERE dep_id=%(dep_id)s
    """

    try:
        for i in range(len(data_list["dep_id"])):
            params = {
                "dep_id": data_list["dep_id"][i],
                "org_cod": data_list.get("org_cod", [None])[i],
                "dep_nom": data_list.get("dep_nom", [None])[i],
                "dep_des": data_list.get("dep_des", [None])[i],
                "dep_email": data_list.get("dep_email", [None])[i],
                "dep_site": data_list.get("dep_site", [None])[i],
                "dep_sigla": data_list.get("dep_sigla", [None])[i],
                "dep_tel": data_list.get("dep_tel", [None])[i],
                "img_data": (
                    psycopg2.Binary(files[f"img_data_{i}"].read())
                    if f"img_data_{i}" in files
                    else None
                ),
            }

            try:
                connection.exec(insert_sql, params)
            except psycopg2.errors.UniqueViolation:
                connection.exec(update_sql, params)

        return jsonify({"message": "Departamentos processed successfully"}), 201
    except Exception as e:
        return (
            jsonify({"message": "Error processing departamentos", "error": str(e)}),
            500,
        )


# getDepartamentos
@app.route("/getDepartamentos", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def get_departamentos():
    try:
        scriptSql = "SELECT dep_id, org_cod, dep_nom, dep_des, dep_email, dep_site, dep_sigla, dep_tel, img_data FROM departamento"
        result = connection.select(scriptSql)
        departamentos = []
        for row in result:
            departamento = {
                "dep_id": row[0],
                "org_cod": row[1],
                "dep_nom": row[2],
                "dep_des": row[3],
                "dep_email": row[4],
                "dep_site": row[5],
                "dep_sigla": row[6],
                "dep_tel": row[7],
                # 'img_data': row[8],  # Se necessário, você pode enviar img_data como uma string ou outro formato
            }
            departamentos.append(departamento)

        return jsonify(departamentos), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


# VER EMPENHOS
@app.route("/AllEmpenhos", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def get_empenhos():
    scriptSql = """
    SELECT 
        id, coluna, emp_nom, status_tomb, tipo_emp, pdf_empenho, data_fornecedor, 
        prazo_entrega, status_recebimento, loc_entrega, loc_entrega_confirmado, cnpj, 
        loc_nom, des_nom, status_tombamento, data_tombamento, data_aviso, prazo_teste, 
        atestado, loc_tom, status_nf, observacoes, data_agendamento, n_termo_processo, 
        origem, valor_termo, n_projeto, data_tomb_sei, pdf_nf, pdf_resumo, created_at
    FROM 
        empenho
    """

    resultado = connection.select(scriptSql)

    columns = [
        "id",
        "coluna",
        "emp_nom",
        "status_tomb",
        "tipo_emp",
        "pdf_empenho",
        "data_fornecedor",
        "prazo_entrega",
        "status_recebimento",
        "loc_entrega",
        "loc_entrega_confirmado",
        "cnpj",
        "loc_nom",
        "des_nom",
        "status_tombamento",
        "data_tombamento",
        "data_aviso",
        "prazo_teste",
        "atestado",
        "loc_tom",
        "status_nf",
        "observacoes",
        "data_agendamento",
        "n_termo_processo",
        "origem",
        "valor_termo",
        "n_projeto",
        "data_tomb_sei",
        "pdf_nf",
        "pdf_resumo",
        "created_at",
    ]

    # Convert the binary data to base64
    result_with_base64 = []
    for row in resultado:
        row_dict = dict(zip(columns, row))
        row_dict["pdf_empenho"] = (
            base64.b64encode(row_dict["pdf_empenho"]).decode("utf-8")
            if row_dict["pdf_empenho"]
            else None
        )
        row_dict["pdf_nf"] = (
            base64.b64encode(row_dict["pdf_nf"]).decode("utf-8")
            if row_dict["pdf_nf"]
            else None
        )
        row_dict["pdf_resumo"] = (
            base64.b64encode(row_dict["pdf_resumo"]).decode("utf-8")
            if row_dict["pdf_resumo"]
            else None
        )
        result_with_base64.append(row_dict)

    return jsonify(result_with_base64), 200
