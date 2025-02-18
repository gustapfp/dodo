from django.db import migrations

def create_sectors(apps, schema_editor):
    Sector = apps.get_model('data_management', 'Sector')
    sectors = [
        ("004.005", "Process. de Roupas"),
        ("004.004", "Process. de produtos"),
        ("004.003", "Limpeza e Desinf. de superf"),
        ("004.002", "Gestão de Infraestrutura"),
        ("004.001", "Gestão de equipamentos"),
        ("003.007", "Mét. endoscópicos e vid."),
        ("003.006", "Radiologia Interv."),
        ("003.005", "Medicina Nuclear"),
        ("003.004", "Diagósticos por imagem"),
        ("003.003", "Met. Diagósticos. e Terap."),
        ("003.002", "Anatomia Patológica e Citop"),
        ("003.001", "Análises clínicas"),
        ("002.020", "Atenção Domiciliar"),
        ("002.019", "Atenção Primária"),
        ("002.018", "Telemedicina"),
        ("002.017", "Odontologia"),
        ("002.016", "Atend. Pré Hospitalar"),
        ("002.015", "Atendimento Oftalmológico"),
        ("002.014", "Assistência Nutricional"),
        ("002.013", "Assistência Farmacêutica"),
        ("002.012", "Med. Hiperbárica"),
        ("002.011", "Radioterapia"),
        ("002.010", "Assistência Oncológica"),
        ("002.009", "Assistência Nefrológica"),
        ("002.008", "Assistência Hemoterápica"),
        ("002.007", "Cuidados Intensivos"),
        ("002.006", "Atendimento Neonatal"),
        ("002.005", "Atendimento Obstétrico"),
        ("002.004", "Atendimento Cirúrgico"),
        ("002.003", "Atendimento Emergencial"),
        ("002.002", "Atendimento Ambulatorial"),
        ("002.001", "Internação"),
        ("001.010", "Gestão Da Comunicação"),
        ("001.009", "Gestão Da Segurança"),
        ("001.008", "Gestão Do Acesso"),
        ("001.007", "Gestão Da Tec. Da Inf."),
        ("001.006", "Gestão De Suprimentos"),
        ("001.005", "Gestão De Pessoas"),
        ("001.004", "Gestão Adm Financeira"),
        ("001.003", "Prev. Controle De Infecção"),
        ("001.002", "Gestão Da Qualidade"),
        ("001.001", "Liderança Organizacional"),
    
    ]
    
    for id, description in sectors:
        # Store only the description as the Sector's name.
        Sector.objects.create(name=description)

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

     




