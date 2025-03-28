# Generated by Django 5.1.6 on 2025-02-20 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='centro_custo',
            old_name='descricao_lancamento',
            new_name='Estabelecimento',
        ),
        migrations.RenameField(
            model_name='lancamentos',
            old_name='centro_custo',
            new_name='Centro_Custo',
        ),
        migrations.RenameField(
            model_name='lancamentos',
            old_name='data',
            new_name='Data',
        ),
        migrations.RenameField(
            model_name='lancamentos',
            old_name='descricao',
            new_name='Estabelecimento',
        ),
        migrations.RenameField(
            model_name='lancamentos',
            old_name='parcelas',
            new_name='Mes',
        ),
        migrations.RemoveField(
            model_name='lancamentos',
            name='tipo_lancamento',
        ),
        migrations.RemoveField(
            model_name='lancamentos',
            name='total',
        ),
        migrations.RemoveField(
            model_name='lancamentos',
            name='valor',
        ),
        migrations.AddField(
            model_name='centro_custo',
            name='Tipo_Lancamento',
            field=models.CharField(default='S', max_length=1),
        ),
        migrations.AddField(
            model_name='centro_custo',
            name='fixo_variavel',
            field=models.CharField(choices=[('F', 'Fixo'), ('V', 'Variavel')], default='V', max_length=1),
        ),
        migrations.AddField(
            model_name='lancamentos',
            name='Despesa_fv',
            field=models.CharField(choices=[('F', 'Fixo'), ('V', 'Variavel')], default='V', max_length=1),
        ),
        migrations.AddField(
            model_name='lancamentos',
            name='Parcelas',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='lancamentos',
            name='Tipo_Lancamento',
            field=models.CharField(default='S', max_length=1),
        ),
        migrations.AddField(
            model_name='lancamentos',
            name='Total',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='lancamentos',
            name='Valor',
            field=models.FloatField(default=0),
        ),
    ]
