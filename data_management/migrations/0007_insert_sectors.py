from django.db import migrations

def create_sectors(apps, schema_editor):
    Sector = apps.get_model('data_management', 'Sector')
    sectors = [
        ("004.005", "4.5 Process. de Roupas"),
        ("004.004", "4.4 Process. de produtos"),
        ("004.003", "4.3 Limpeza e Desinf. de superf"),
        ("004.002", "4.2 Gestão de Infraestrutura"),
        ("004.001", "4.1 Gestão de equipamentos"),
        ("003.007", "3.7 Mét. endoscópicos e vid."),
        ("003.006", "3.6 Radiologia Interv."),
        ("003.005", "3.5 Medicina Nuclear"),
        ("003.004", "3.4 Diagósticos por imagem"),
        ("003.003", "3.3 Met. Diagósticos. e Terap."),
        ("003.002", "3.2 Anatomia Patológica e Citop"),
        ("003.001", "3.1 Análises clínicas"),
        ("002.020", "2.20 Atenção Domiciliar"),
        ("002.019", "2.19 Atenção Primária"),
        ("002.018", "2.18 Telemedicina"),
        ("002.017", "2.17 Odontologia"),
        ("002.016", "2.16 Atend. Pré Hospitalar"),
        ("002.015", "2.15 Atendimento Oftalmológico"),
        ("002.014", "2.14 Assistência Nutricional"),
        ("002.013", "2.13 Assistência Farmacêutica"),
        ("002.012", "2.12 Med. Hiperbárica"),
        ("002.011", "2.11 Radioterapia"),
        ("002.010", "2.10 Assistência Oncológica"),
        ("002.009", "2.9 Assistência Nefrológica"),
        ("002.008", "2.8 Assistência Hemoterápica"),
        ("002.007", "2.7 Cuidados Intensivos"),
        ("002.006", "2.6 Atendimento Neonatal"),
        ("002.005", "2.5 Atendimento Obstétrico"),
        ("002.004", "2.4 Atendimento Cirúrgico"),
        ("002.003", "2.3 Atendimento Emergencial"),
        ("002.002", "2.2 Atendimento Ambulatorial"),
        ("002.001", "2.1 Internação"),
        ("001.010", "1.10 Gestão Da Comunicação"),
        ("001.009", "1.9 Gestão Da Segurança"),
        ("001.008", "1.8 Gestão Do Acesso"),
        ("001.007", "1.7 Gestão Da Tec. Da Inf."),
        ("001.006", "1.6 Gestão De Suprimentos"),
        ("001.005", "1.5 Gestão De Pessoas"),
        ("001.004", "1.4 Gestão Adm Financeira"),
        ("001.003", "1.3 Prev. Controle De Infecção"),
        ("001.002", "1.2 Gestão Da Qualidade"),
        ("001.001", "1.1 Liderança Organizacional"),
    
    ]
    
    for id, description in sectors:
        # Store only the description as the Sector's name.
        Sector.objects.create(name=description, sector_id=id)

def remove_sectors(apps, schema_editor):
    Sector = apps.get_model('data_management', 'Sector')
    sector_names = [
        "Process. de Roupas",
        "Process. de produtos",
        "Limpeza e Desinf. de superf",
        "Gestão de Infraestrutura",
        "Gestão de equipamentos",
        "Mét. endoscópicos e vid.",
        "Radiologia Interv.",
        "Medicina Nuclear",
        "Diagósticos por imagem",
        "Met. Diagósticos. e Terap.",
        "Anatomia Patológica e Citop",
        "Análises clínicas",
        "Atenção Domiciliar",
        "Atenção Primária",
        "Telemedicina",
        "Odontologia",
        "Atend. Pré Hospitalar",
        "Atendimento Oftalmológico",
        "Assistência Nutricional",
        "Assistência Farmacêutica",
        "Med. Hiperbárica",
        "Radioterapia",
        "Assistência Oncológica",
        "Assistência Nefrológica",
        "Assistência Hemoterápica",
        "Cuidados Intensivos",
        "Atendimento Neonatal",
        "Atendimento Obstétrico",
        "Atendimento Cirúrgico",
        "Atendimento Emergencial",
        "Atendimento Ambulatorial",
        "Internação",
        "Gestão Da Comunicação",
        "Gestão Da Segurança",
        "Gestão Do Acesso",
        "Gestão Da Tec. Da Inf.",
        "Gestão De Suprimentos",
        "Gestão De Pessoas",
        "Gestão Adm Financeira",
        "Prev. Controle De Infecção",
        "Gestão Da Qualidade",
        "Liderança Organizacional",
        "Avaliador Externo",
    ]
    for name in sector_names:
        Sector.objects.filter(name=name).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('data_management', '0006_create_template'),
    ]
    
    operations = [
        migrations.RunPython(create_sectors, remove_sectors),
    ]

     




