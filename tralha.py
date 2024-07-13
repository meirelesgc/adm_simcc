@app.route('/departamento', methods=['POST'])
def create_or_update_departamento():
    data_list = request.form.to_dict(flat=False)
    files = request.files

    insert_sql = '''
        INSERT INTO departamento (
            dep_id, org_cod, dep_nom, dep_des, dep_email, dep_site, dep_sigla, dep_tel, img_data
        ) VALUES (
            %(dep_id)s, %(org_cod)s, %(dep_nom)s, %(dep_des)s, %(dep_email)s, %(dep_site)s, %(dep_sigla)s, %(dep_tel)s, %(img_data)s
        )
    '''

    update_sql = '''
        UPDATE departamento SET 
            org_cod=%(org_cod)s, dep_nom=%(dep_nom)s, dep_des=%(dep_des)s, 
            dep_email=%(dep_email)s, dep_site=%(dep_site)s, dep_sigla=%(dep_sigla)s, dep_tel=%(dep_tel)s, 
            img_data=%(img_data)s
        WHERE dep_id=%(dep_id)s
    '''

    try:
        for i in range(len(data_list['dep_id'])):
            params = {
                'dep_id': data_list['dep_id'][i],
                'org_cod': data_list.get('org_cod', [None])[i],
                'dep_nom': data_list.get('dep_nom', [None])[i],
                'dep_des': data_list.get('dep_des', [None])[i],
                'dep_email': data_list.get('dep_email', [None])[i],
                'dep_site': data_list.get('dep_site', [None])[i],
                'dep_sigla': data_list.get('dep_sigla', [None])[i],
                'dep_tel': data_list.get('dep_tel', [None])[i],
                'img_data': psycopg2.Binary(files[f'img_data_{i}'].read()) if f'img_data_{i}' in files else None,
            }

            try:
                connection.exec(insert_sql, params)
            except psycopg2.errors.UniqueViolation:
                connection.exec(update_sql, params)

        return jsonify({'message': 'Departamentos processed successfully'}), 201
    except Exception as e:
        return jsonify({'message': 'Error processing departamentos', 'error': str(e)}), 500

#getDepartamentos
@app.route("/getDepartamentos", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def get_departamentos():
    try:
        scriptSql = 'SELECT dep_id, org_cod, dep_nom, dep_des, dep_email, dep_site, dep_sigla, dep_tel, img_data FROM departamento'
        result = connection.select(scriptSql)
        departamentos = []
        for row in result:
            departamento = {
                'dep_id': row[0],
                'org_cod': row[1],
                'dep_nom': row[2],
                'dep_des': row[3],
                'dep_email': row[4],
                'dep_site': row[5],
                'dep_sigla': row[6],
                'dep_tel': row[7],
                # 'img_data': row[8],  # Se necessário, você pode enviar img_data como uma string ou outro formato
            }
            departamentos.append(departamento)
        
        return jsonify(departamentos), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    
#tecnicos
    
@app.route('/tecnicos', methods=['POST'])
def create_or_update_tecnicos():
    data_list = request.json

    script_sql = '''
        DELETE FROM tecnico 
        WHERE carga_id = (
            SELECT 
                id 
            FROM 
                carga_ano_semestre 
            WHERE 
                year_charge = %(year_charge)s 
                AND semester = %(semester)s);
    '''
    params = {'year_charge': data_list[0]['year_charge'], 'semester': data_list[0]['semester']}
    connection.exec(script_sql, params)
    
    select_sql = """
        SELECT 
            id 
        FROM 
            carga_ano_semestre 
        WHERE 
            year_charge = %(year_charge)s 
            AND semester = %(semester)s;
    """
    
    carga_id = connection.select(select_sql, params)

    insert_sql = '''
        INSERT INTO tecnico (
            matric, ins_ufmg, nome, genero, deno_sit, 
            rt, classe, cargo, nivel, ref, titulacao, 
            setor, detalhe_setor, dting_org, data_prog,
            carga_id
        ) VALUES 
        (%(matric)s, %(ins_ufmg)s, %(nome)s, %(genero)s, %(deno_sit)s, %(rt)s, %(classe)s, %(cargo)s, %(nivel)s, %(ref)s, %(titulacao)s, %(setor)s, %(detalhe_setor)s, %(dting_org)s, %(data_prog)s, %(carga_id)s)
    '''

    for record in data_list:
        params = {
            'matric': record.get('matric'),
            'ins_ufmg': record.get('ins_ufmg'),
            'nome': record.get('nome'),
            'genero': record.get('genero'),
            'deno_sit': record.get('deno_sit'),
            'rt': record.get('rt'),
            'classe': record.get('classe'),
            'cargo': record.get('cargo'),
            'nivel': record.get('nivel'),
            'ref': record.get('ref'),
            'titulacao': record.get('titulacao'),
            'setor': record.get('setor'),
            'detalhe_setor': record.get('detalhe_setor'),
            'dting_org': record.get('dting_org'),
            'data_prog': record.get('data_prog'),
            'carga_id': carga_id[0][0]
        }
        try:
            connection.exec(insert_sql, params)
        except:
            print(f'Matricula já cadastrada: {record.get('matric')}')
            
    return jsonify({'message': 'Técnicos processed successfully'}), 201
    
    #docentes

@app.route('/tecnicos', methods=['GET'])
def get_tecnicos():
    year = request.args.get('year')
    semester = request.args.get('semester')
    if year or semester:
        year_filter = """
        LEFT JOIN carga_ano_semestre cs ON t.carga_id = cs.carga_id
        WHERE 
            year_charge = %(year_charge)s
            AND semester = %(semester)s 
        """
    else:
        year_filter = """
        LEFT JOIN carga_ano_semestre cs ON t.carga_id = cs.id
        WHERE carga_id = (
        SELECT id 
        FROM carga_ano_semestre 
        ORDER BY 
            year_charge DESC, 
            semester DESC
        LIMIT 1)
        """
    
    script_sql = """
    SELECT 
        matric,
        ins_ufmg,
        nome,
        genero,
        deno_sit,
        rt,
        classe,
        cargo,
        nivel,
        ref,
        titulacao, 
        setor,
        detalhe_setor,
        dting_org,
        data_prog
    FROM
        tecnico t
    {year_filter}
    """
    reg = connection.select(script_sql, {'year_charge': year, 'semester': semester})
    df = pd.DataFrame(reg, columns=[
        
'matric',
'ins_ufmg',
'nome',
'genero',
'deno_sit',
'rt',
'classe',
'cargo',
'nivel',
'ref',
'titulacao',
'setor',
'detalhe_setor',
'dting_org',
'data_prog',
        
    ])
    
    return jsonify(df.to_dict(orient='records'))


@app.route('/docentes', methods=['GET'])
def get_docentes():
    year = request.args.get('year')
    semester = request.args.get('semester')
    if year or semester:
        year_filter = """
        LEFT JOIN carga_ano_semestre cs ON d.carga_id = cs.carga_id
        WHERE 
            cs.year_charge = %(year_charge)s
            AND cs.semester = %(semester)s 
        """
    else: 
        year_filter = """
        LEFT JOIN carga_ano_semestre cs ON d.carga_id = cs.id
        WHERE carga_id = (
        SELECT id 
        FROM carga_ano_semestre 
        ORDER BY 
            year_charge DESC, 
            semester DESC
        LIMIT 1)
        """
        
    script_sql = """
    SELECT 
        matric, 
        inscUFMG, 
        nome, 
        genero, 
        situacao, 
        rt, 
        clas, 
        cargo, 
        classe, 
        ref, 
        titulacao, 
        entradaNaUFMG, 
        progressao
    FROM docentes d
    {year_filter}
    """
    reg = connection.select(script_sql, {'year_charge': year, 'semester': semester})

    df = pd.DataFrame(reg, columns=[
        'matric',
        'inscUFMG',
        'nome',
        'genero',
        'situacao',
        'rt',
        'clas',
        'cargo',
        'classe',
        'ref',
        'titulacao',
        'entradaNaUFMG',
        'progressao',
    ])
    return jsonify(df.to_dict(orient='records'))


@app.route('/docentes', methods=['POST'])
def create_or_update_docentes():
    data_list = request.json
    
    select_sql = '''
        SELECT carga_id FROM carga_ano_semestre WHERE year_charge = %(year_charge)s AND semester = %(semester)s 
    '''
    
    delete_sql = '''
        DELETE FROM docentes 
        WHERE carga_id = (
            SELECT 
                id 
            FROM 
                carga_ano_semestre 
            WHERE 
                year_charge = %(year_charge)s 
                AND semester = %(semester)s);
    '''
    select_sql = """
        SELECT 
            id 
        FROM 
            carga_ano_semestre 
        WHERE 
            year_charge = %(year_charge)s 
            AND semester = %(semester)s;
    """
    delete_data = {'year_charge': data_list[0]['year_charge'], 'semester': data_list[0]['semester']}
    carga_id = connection.select(select_sql, delete_data)
    insert_sql = '''
        INSERT INTO docentes (
            matric, inscUFMG, nome, genero, situacao, rt, clas, cargo, classe, ref, titulacao, entradaNaUFMG, progressao, carga_id
        ) VALUES (
            %(matric)s, %(inscUFMG)s, %(nome)s, %(genero)s, %(situacao)s, %(rt)s, %(clas)s, %(cargo)s, %(classe)s, %(ref)s, %(titulacao)s, %(entradaNaUFMG)s, %(progressao)s, %(carga_id)s
        )
    '''
    connection.exec(delete_sql, delete_data)  # Reset the table
    for record in data_list:
        params = {
            'matric': record.get('matric'),
            'inscUFMG': record.get('inscUFMG'),
            'nome': record.get('nome'),
            'genero': record.get('genero'),
            'situacao': record.get('situacao'),
            'rt': record.get('rt'),
            'clas': record.get('clas'),
            'cargo': record.get('cargo'),
            'classe': record.get('classe'),
            'ref': record.get('ref'),
            'titulacao': record.get('titulacao'),
            'entradaNaUFMG': record.get('entradaNaUFMG'),
            'progressao': record.get('progressao'),
            'carga_id': carga_id[0][0]
        }
        try:
            connection.exec(insert_sql, params)
        except:
            print(f'Matricula já cadastrada: {record.get('matric')}')
    return jsonify({'message': 'Docentes processed successfully'}), 201
