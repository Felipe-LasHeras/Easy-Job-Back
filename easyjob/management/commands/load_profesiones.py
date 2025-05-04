# jobs/management/commands/load_profesiones.py
from django.core.management.base import BaseCommand
from jobs.models import Profesion

class Command(BaseCommand):
    help = 'Carga las profesiones iniciales en la base de datos'

    def handle(self, *args, **kwargs):
        profesiones = [
            {'nombre': 'Programador', 'descripcion': 'Desarrollo de aplicaciones web y móviles utilizando tecnologías HTML, CSS, JavaScript, React y Node.js. Experiencia en bases de datos SQL y NoSQL.'},
            {'nombre': 'Diseñador', 'descripcion': 'Diseño gráfico, web y publicitario. Manejo de herramientas Adobe y experiencia en UI/UX.'},
            {'nombre': 'Contador', 'descripcion': 'Servicios contables y tributarios. Declaración de impuestos, contabilidad para empresas y personas.'},
            {'nombre': 'Abogado', 'descripcion': 'Asesoría legal en diversas áreas como civil, laboral, comercial y tributario.'},
            {'nombre': 'Electricista', 'descripcion': 'Instalaciones eléctricas domiciliarias e industriales. Reparaciones y mantenimiento.'},
        ]
        
        for prof in profesiones:
            Profesion.objects.get_or_create(
                nombre=prof['nombre'],
                defaults={'descripcion': prof['descripcion']}
            )
            
        self.stdout.write(self.style.SUCCESS('Profesiones cargadas correctamente'))