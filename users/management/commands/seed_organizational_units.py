from django.core.management.base import BaseCommand
from users.models import OrganizationalUnit
import json
from datetime import datetime


class Command(BaseCommand):
    help = 'Seed organizational units data'

    def handle(self, *args, **options):
        # Data from the user's request
        org_units_data = [
            {
                "id": 5,
                "user_id": 1,
                "core_service_id": None,
                "name": "Direcção de Informações Policias",
                "slug": "DINFOP",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-07T15:40:14.000Z",
                "updated_at": "2025-11-07T15:40:14.000Z",
                "createdAt": "07/11/2025 15:40:14",
                "updatedAt": "07/11/2025 15:40:14"
            },
            {
                "id": 6,
                "user_id": 1,
                "core_service_id": None,
                "name": "Direcção de Investigação de Ilícitos Penais",
                "slug": "DIIP",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-07T15:40:15.000Z",
                "updated_at": "2025-11-07T15:40:15.000Z",
                "createdAt": "07/11/2025 15:40:15",
                "updatedAt": "07/11/2025 15:40:15"
            },
            {
                "id": 68,
                "user_id": 1,
                "core_service_id": None,
                "name": "Pureza",
                "slug": "PRZ",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-18T14:40:15.000Z",
                "updated_at": "2025-11-18T14:40:15.000Z"
            },
            {
                "id": 67,
                "user_id": 1,
                "core_service_id": None,
                "name": "Unidade Portuária",
                "slug": "UP",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-17T05:27:45.000Z",
                "updated_at": "2025-11-17T05:27:45.000Z"
            },
            {
                "id": 66,
                "user_id": 1,
                "core_service_id": None,
                "name": "Unidade De Policia De Segurança Portuária",
                "slug": "UPSP",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-17T05:27:45.000Z",
                "updated_at": "2025-11-17T05:27:45.000Z"
            },
            {
                "id": 65,
                "user_id": 1,
                "core_service_id": None,
                "name": "Unidade De Aviação",
                "slug": "UAv",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-17T05:27:45.000Z",
                "updated_at": "2025-11-17T05:27:45.000Z"
            },
            {
                "id": 64,
                "user_id": 1,
                "core_service_id": None,
                "name": "Unidade Aeroportuaria António Agostinho Neto",
                "slug": "UAAAN",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-17T05:27:45.000Z",
                "updated_at": "2025-11-17T05:27:45.000Z"
            },
            {
                "id": 63,
                "user_id": 1,
                "core_service_id": None,
                "name": "Unidade Aeroportuária",
                "slug": "UA",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-17T05:27:45.000Z",
                "updated_at": "2025-11-17T05:27:45.000Z"
            },
            {
                "id": 62,
                "user_id": 1,
                "core_service_id": None,
                "name": "Polícia Fiscal Aduaneira",
                "slug": "PFA",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-17T05:27:45.000Z",
                "updated_at": "2025-11-17T05:27:45.000Z"
            },
            {
                "id": 52,
                "user_id": 1,
                "core_service_id": None,
                "name": "Gabinete Do 2.º Comandante Geral I",
                "slug": "GAB. 2.º CMDTE GERAL I",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-17T05:27:44.000Z",
                "updated_at": "2025-11-17T05:27:44.000Z"
            },
            {
                "id": 53,
                "user_id": 1,
                "core_service_id": None,
                "name": "Gabinete Do 2.º Comandante Geral Ii",
                "slug": "GAB. 2.º CMDTE GERAL II",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-17T05:27:44.000Z",
                "updated_at": "2025-11-17T05:27:44.000Z"
            },
            {
                "id": 54,
                "user_id": 1,
                "core_service_id": None,
                "name": "Gabinete Do Comandante Geral",
                "slug": "GAB.CMDTE GERAL",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-17T05:27:44.000Z",
                "updated_at": "2025-11-17T05:27:44.000Z"
            },
            {
                "id": 55,
                "user_id": 1,
                "core_service_id": None,
                "name": "Inspecção Da PNA",
                "slug": "IPNA",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-17T05:27:44.000Z",
                "updated_at": "2025-11-17T05:27:44.000Z"
            },
            {
                "id": 56,
                "user_id": 1,
                "core_service_id": None,
                "name": "Instituto Médio De Ciências Policiais",
                "slug": "IMCP",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-17T05:27:44.000Z",
                "updated_at": "2025-11-17T05:27:44.000Z"
            },
            {
                "id": 58,
                "user_id": 1,
                "core_service_id": None,
                "name": "Polícia De Guarda Fronteiras",
                "slug": "PGF",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-17T05:27:44.000Z",
                "updated_at": "2025-11-17T05:27:44.000Z"
            },
            {
                "id": 59,
                "user_id": 1,
                "core_service_id": None,
                "name": "Polícia De Intervenção Rápida",
                "slug": "PIR",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-17T05:27:44.000Z",
                "updated_at": "2025-11-17T05:27:44.000Z"
            },
            {
                "id": 60,
                "user_id": 1,
                "core_service_id": None,
                "name": "Polícia De Segurança De Objectivos Estratégicos",
                "slug": "PSOE",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-17T05:27:44.000Z",
                "updated_at": "2025-11-17T05:27:44.000Z"
            },
            {
                "id": 61,
                "user_id": 1,
                "core_service_id": None,
                "name": "Polícia De Segurança Pessoal E De Entidades Protocolares",
                "slug": "PSPEP",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-17T05:27:44.000Z",
                "updated_at": "2025-11-17T05:27:44.000Z"
            },
            {
                "id": 57,
                "user_id": 1,
                "core_service_id": None,
                "name": "Instituto Superior De Ciências Policiais E Criminais",
                "slug": "ISCPC",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-17T05:27:44.000Z",
                "updated_at": "2025-11-17T05:27:44.000Z"
            },
            {
                "id": 46,
                "user_id": 1,
                "core_service_id": None,
                "name": "Direcçâo De Telecomunicações E Tecnologias De Informação",
                "slug": "DTTI",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-17T05:27:43.000Z",
                "updated_at": "2025-11-17T05:27:43.000Z"
            },
            {
                "id": 43,
                "user_id": 1,
                "core_service_id": None,
                "name": "Direcçâo De Pessoal E Quadros",
                "slug": "DPQ",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-17T05:27:43.000Z",
                "updated_at": "2025-11-17T05:27:43.000Z"
            },
            {
                "id": 44,
                "user_id": 1,
                "core_service_id": None,
                "name": "Direcção De Segurança Pública E Operações",
                "slug": "DISPO",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-17T05:27:43.000Z",
                "updated_at": "2025-11-17T05:27:43.000Z"
            },
            {
                "id": 45,
                "user_id": 1,
                "core_service_id": None,
                "name": "Direcção De Serviços De Saúde",
                "slug": "DSS",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-17T05:27:43.000Z",
                "updated_at": "2025-11-17T05:27:43.000Z"
            },
            {
                "id": 47,
                "user_id": 1,
                "core_service_id": None,
                "name": "Direcção De Trânsito E Segurança Rodoviária",
                "slug": "DTSER",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-17T05:27:43.000Z",
                "updated_at": "2025-11-17T05:27:43.000Z"
            },
            {
                "id": 48,
                "user_id": 1,
                "core_service_id": None,
                "name": "Direcção De Transportes",
                "slug": "DT",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-17T05:27:43.000Z",
                "updated_at": "2025-11-17T05:27:43.000Z"
            },
            {
                "id": 49,
                "user_id": 1,
                "core_service_id": None,
                "name": "Direcção Nacional De Recursos Humanos",
                "slug": "DNRH",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-17T05:27:43.000Z",
                "updated_at": "2025-11-17T05:27:43.000Z"
            },
            {
                "id": 50,
                "user_id": 1,
                "core_service_id": None,
                "name": "Escola Prática De Polícia",
                "slug": "EPP",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-17T05:27:43.000Z",
                "updated_at": "2025-11-17T05:27:43.000Z"
            },
            {
                "id": 51,
                "user_id": 1,
                "core_service_id": None,
                "name": "Gabinete De Estudo E Informação E Análise",
                "slug": "GEIA",
                "description": "Criado automaticamente pelo sistema.",
                "active": 1,
                "deleted_at": None,
                "created_at": "2025-11-17T05:27:43.000Z",
                "updated_at": "2025-11-17T05:27:43.000Z"
            }
        ]

        # Seed the data
        created_count = 0
        for unit_data in org_units_data:
            # Parse datetime strings
            created_at = datetime.strptime(
                unit_data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
            updated_at = datetime.strptime(
                unit_data['updated_at'], '%Y-%m-%dT%H:%M:%S.%fZ')

            # Create or update the organizational unit
            org_unit, created = OrganizationalUnit.objects.update_or_create(
                id=unit_data['id'],
                defaults={
                    'user_id': unit_data['user_id'],
                    'core_service_id': unit_data['core_service_id'],
                    'name': unit_data['name'],
                    'slug': unit_data['slug'],
                    'description': unit_data['description'],
                    'active': bool(unit_data['active']),
                    'deleted_at': unit_data['deleted_at'],
                    'created_at': created_at,
                    'updated_at': updated_at,
                }
            )

            if created:
                created_count += 1
                self.stdout.write(
                    f'Created organizational unit: {org_unit.name}')
            else:
                self.stdout.write(
                    f'Updated organizational unit: {org_unit.name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded {created_count} new organizational units '
                f'and updated {len(org_units_data) - created_count} existing ones.'
            )
        )
