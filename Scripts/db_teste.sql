INSERT INTO institution (institution_id, name, acronym, lattes_id)
VALUES (
        '68125729-c357-4830-ba4d-ec3ca757c323',
        'Universidade do Estado da Bahia',
        'UNEB',
        '584200000007'
    ),
    (
        '2a643ff4-5a18-4d87-8c3d-6c3f7091e001',
        'Universidade Estadual de Santa Cruz',
        'UESC',
        '363100000000'
    ),
    (
        '08aa6e17-f9ae-4979-a399-5b32a506a15e',
        'Universidade Estadual do Sudoeste da Bahia',
        'UESB',
        '749000000008'
    ),
    (
        '7d367bc2-5c74-4648-a637-7f5c3f4fac81',
        'Universidade Estadual de Feira de Santana',
        'UEFS',
        '204400000003'
    ),
    (
        '498cadc8-b8f6-4008-902e-76281109187d',
        'Universidade Federal do Sul da Bahia',
        'UFSB',
        'JIDJ00000007'
    ),
    (
        '498cadc8-b8f6-4008-902e-76281101237d',
        'Universidade Irregular no Curriculo Lattes',
        'UICL',
        '000000000000'
    );
SELECT *
FROM institution;
DELETE FROM institution
WHERE institution_id = '498cadc8-b8f6-4008-902e-76281109187d';
INSERT INTO researcher (name, lattes_id, institution_id)
VALUES ('John Doe', 'JD123', 1),
    ('Jane Smith', 'JS456', 2);
SELECT *
FROM researcher;
INSERT INTO graduate_program (
        code,
        name,
        area,
        modality,
        TYPE,
        rating,
        institution_id
    )
VALUES (
        'GP001',
        'Computer Science',
        'Computer Science',
        'Master',
        'MSc',
        'A',
        1
    ),
    (
        'GP002',
        'Electrical Engineering',
        'Engineering',
        'PhD',
        'PhD',
        'B',
        2
    );
SELECT *
FROM graduate_program;
INSERT INTO graduate_program_researcher (graduate_program_id, researcher_id, year, type_)
VALUES (1, 1, 2022, 'Supervisor'),
    (2, 2, 2021, 'Co-Supervisor');
SELECT *
FROM graduate_program_researcher;